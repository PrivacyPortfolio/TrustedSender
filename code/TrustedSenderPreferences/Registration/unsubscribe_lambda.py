"""
TrustedSender action Lambda.

Handles two API Gateway routes (see trustedsender-preferences-api.yaml):
  POST /unsubscribe            legacy Paubox Forms flat payload (one-click)
  POST /trusted-sender/action  fine-grained payload (domain / intermediary
                                parties / transports)

Identity model: this function never tries to identify *who* clicked an
unsubscribe link (no IP/cookie/pixel fingerprinting -- see the token
design note below for why). Instead, at send time the caller mints an
opaque token via mint_unsubscribe_token() and embeds it in the outbound
message's unsubscribe URL. That token is the only thing the click needs
to carry; the handler resolves it against this function's own token
registry to recover the Paubox Message-ID, sender identity, and this
org's taxonomy (party_role / sender_class / campaign_tags) *before* ever
calling Paubox. Paubox is only ever the last-mile executor -- the token
registry is the actual identity system. A direct fine-grained call from
an authenticated agent (POST /trusted-sender/action with a scope object,
no token) skips token resolution entirely, since the agent is already an
authenticated principal identifying its own target.

For each request this function:
  1. Resolves identity: either a token (?t=... on GET, or "token" in a
     POST body) is looked up in the token registry, or a direct
     scope-bearing payload is used as-is (legacy Paubox Forms payloads
     are normalized onto the same internal shape first).
  2. Validates required fields.
  3. Resolves which email address(es) the action actually applies to
     (a single sender, or every known subscriber at sender_domain when
     extend_to_domain is set).
  4. Calls the real Paubox Marketing API to apply the action, for the
     "email" transport only -- Paubox has no concept of Intermediary
     Parties or non-email transports, so those are recorded in the
     registry/audit log for accountability but are not something this
     function can enforce anywhere. Say so explicitly in the response
     rather than silently dropping them.
  5. Writes one row to a DynamoDB "registry" table (current state per
     sender, including party_role / sender_class / campaign_tags) and
     one immutable row to a DynamoDB "audit" table (append-only event
     log), and emits a structured CloudWatch log line.
  6. Returns a TrustedSenderActionResponse-shaped JSON body.

Environment variables (see README section at the bottom of this file):
  PAUBOX_API_KEY_SECRET_ARN   Secrets Manager ARN holding the Paubox API key
  PAUBOX_API_KEY              Fallback: raw API key (dev/test only)
  PAUBOX_BASE_URL             Default: https://api.paubox.com/v1/marketing
  REGISTRY_TABLE_NAME         DynamoDB table for current sender state
  AUDIT_TABLE_NAME            DynamoDB table for the append-only audit log
  TOKENS_TABLE_NAME           DynamoDB table for minted unsubscribe tokens
  SUBSCRIBERS_TABLE_NAME      DynamoDB table mapping internal_id <-> email/
                               phone/name <-> cached Paubox subscriber UUID
  TOKEN_SIGNING_SECRET_ARN    Secrets Manager ARN holding the HMAC signing key
  TOKEN_SIGNING_SECRET        Fallback: raw signing key (dev/test only)
  TOKEN_TTL_DAYS              Token lifetime in days (default 90)
  CATEGORY_LIST_ID_MAP        Optional JSON string mapping
                               unsubscribe_categories -> Paubox
                               subscription_list_id, e.g.
                               '{"newsletter": "123e4567-..."}'
                               Omitted categories fall back to a global
                               opt-out rather than a per-list one.
"""

import hashlib
import hmac
import json
import logging
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
secrets_client = boto3.client("secretsmanager")

PAUBOX_BASE_URL = os.environ.get("PAUBOX_BASE_URL", "https://api.paubox.com/v1/marketing")
REGISTRY_TABLE_NAME = os.environ.get("REGISTRY_TABLE_NAME", "trustedsender_registry")
AUDIT_TABLE_NAME = os.environ.get("AUDIT_TABLE_NAME", "trustedsender_audit")
TOKENS_TABLE_NAME = os.environ.get("TOKENS_TABLE_NAME", "trustedsender_tokens")
SUBSCRIBERS_TABLE_NAME = os.environ.get("SUBSCRIBERS_TABLE_NAME", "trustedsender_subscribers")
TOKEN_TTL_DAYS = int(os.environ.get("TOKEN_TTL_DAYS", "90"))
CATEGORY_LIST_ID_MAP = json.loads(os.environ.get("CATEGORY_LIST_ID_MAP", "{}"))

VALID_ACTIONS = {"unsubscribe", "limit", "block", "resubscribe"}
VALID_TRANSPORT_TYPES = {"email", "voice", "sms", "chat", "social_media", "push"}

# Your organizational taxonomy. party_role describes the relationship type;
# sender_class is your Decision-Factors outcome (extended with
# OperationalSender for non-marketing transactional senders -- e.g. a
# password-reset or receipt sender that isn't "Marketing" but also isn't a
# named accountable correspondent). Both are set at mint time (i.e. by you,
# when you send/classify the original message) and carried through
# unchanged -- this function never infers or guesses either one.
VALID_PARTY_ROLES = {"intermediary_party", "controlling_party", "counter_party", "stakeholder"}
VALID_SENDER_CLASSES = {
    "TrustedSender", "UntrustedSender", "PHISender", "MarketingSender",
    "OperationalSender", "DualUseVendor", "UnknownVendor",
}

# Actions that suppress Paubox marketing email when the email transport is
# in scope. "limit" has no Paubox equivalent -- Paubox cannot restrict what
# an org shares with a named third party -- so it is recorded but never
# calls the Paubox API.
PAUBOX_ENFORCEABLE_ACTIONS = {"unsubscribe", "block", "resubscribe"}


class ValidationError(Exception):
    """Raised for malformed input. Mapped to HTTP 400."""


class ScopeConflictError(Exception):
    """Raised when the requested scope exceeds what the requester may set. Mapped to HTTP 409."""


# --------------------------------------------------------------------------
# Paubox Marketing API client
# --------------------------------------------------------------------------

class PauboxClient:
    """
    Thin wrapper around the handful of Paubox Marketing API endpoints this
    function needs. Uses only the standard library (urllib) so the Lambda
    has zero third-party dependencies to package.

    Reference: https://docs.paubox.com/marketing.md
    """

    def __init__(self, api_key: str, base_url: str = PAUBOX_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def _request(self, method: str, path: str, body: dict | None = None, query: dict | None = None) -> dict:
        url = f"{self.base_url}{path}"
        if query:
            url += "?" + urllib.parse.urlencode(query)

        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("authorization", f"Token token={self.api_key}")
        req.add_header("content-type", "application/json")

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw = resp.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            raw = e.read()
            logger.error("Paubox API error %s on %s %s: %s", e.code, method, path, raw)
            try:
                parsed = json.loads(raw)
            except (json.JSONDecodeError, ValueError):
                parsed = {"error": raw.decode("utf-8", errors="replace")}
            parsed["_http_status"] = e.code
            return parsed
        except urllib.error.URLError as e:
            logger.error("Paubox API unreachable on %s %s: %s", method, path, e)
            return {"error": str(e), "_http_status": 0}

    def find_subscriber_id_by_email(self, email: str) -> str | None:
        """
        Paubox has no GET-by-email endpoint, so this uses the search param
        on the list endpoint and confirms an exact (case-insensitive) match
        rather than trusting the first search hit.
        """
        result = self._request("GET", "/subscribers", query={"search": email, "items": 50})
        for record in result.get("data", []):
            attrs = record.get("attributes", {})
            if attrs.get("email", "").lower() == email.lower():
                return record.get("id")
        return None

    def find_subscriber_ids_by_domain(self, domain: str) -> list[str]:
        """
        Best-effort domain sweep: searches for '@domain' and filters to
        exact domain matches. Paubox does not support server-side domain
        filtering, so this pages through search results client-side.
        """
        matches = []
        page = 1
        while True:
            result = self._request(
                "GET", "/subscribers",
                query={"search": f"@{domain}", "items": 200, "page": page},
            )
            records = result.get("data", [])
            if not records:
                break
            for record in records:
                email = record.get("attributes", {}).get("email", "")
                if email.lower().endswith(f"@{domain.lower()}"):
                    matches.append(record["id"])
            if len(records) < 200:
                break
            page += 1
        return matches

    def create_subscriber(self, email: str) -> str | None:
        result = self._request("POST", "/subscribers", body={"subscriber": {"email": email}})
        return result.get("data", {}).get("id")

    def unsubscribe(self, subscriber_ids: list[str], subscription_list_ids: list[str] | None = None) -> dict:
        """
        With subscription_list_ids: per-list opt-out (subscriber stays
        subscribed to everything else).
        Without: global opt-out via opted_out_on, suppressing all future
        marketing email -- this is the closest lever Paubox exposes to
        "block."
        """
        body = {"subscriber_ids": subscriber_ids}
        if subscription_list_ids:
            body["subscription_list_ids"] = subscription_list_ids
        return self._request("POST", "/subscriptions/unsubscribe", body=body)

    def subscribe(self, subscriber_ids: list[str], subscription_list_ids: list[str] | None = None) -> dict:
        body = {"subscriber_ids": subscriber_ids}
        if subscription_list_ids:
            body["subscription_list_ids"] = subscription_list_ids
        return self._request("POST", "/subscriptions/subscribe", body=body)


def get_paubox_api_key() -> str:
    secret_arn = os.environ.get("PAUBOX_API_KEY_SECRET_ARN")
    if secret_arn:
        resp = secrets_client.get_secret_value(SecretId=secret_arn)
        return resp["SecretString"]
    # Dev/test fallback only -- prefer Secrets Manager in production so the
    # key never sits in plaintext Lambda environment config.
    return os.environ["PAUBOX_API_KEY"]


# --------------------------------------------------------------------------
# Unsubscribe token minting + resolution
#
# Identity model: an unsubscribe click (browser or agent) never needs to
# authenticate *who* clicked -- only *which subscription relationship* is
# being acted on. IP address, geolocation, cookies, and tracking pixels are
# deliberately not used for this: they're unreliable (shared NAT, VPNs,
# security-scanner link pre-fetching, forwarded mail) and, more to the
# point, building a click-fingerprinting mechanism into your own
# unsubscribe flow is exactly the "collects information about me which I
# haven't consented to" behavior the Decision-Factors framework flags in
# other senders.
#
# Instead: mint_unsubscribe_token() is called by your send-time code (not
# by this Lambda's HTTP handler) when a message goes out. It stores one row
# server-side keyed by an opaque token and embeds only that token in the
# unsubscribe URL. resolve_token() is the only thing the HTTP handler calls
# when a request comes back in -- it recovers the Paubox Message-ID, sender
# identity, and your taxonomy (party_role / sender_class / campaign_tags)
# before Paubox is ever touched.
# --------------------------------------------------------------------------

def get_token_signing_secret() -> bytes:
    secret_arn = os.environ.get("TOKEN_SIGNING_SECRET_ARN")
    if secret_arn:
        resp = secrets_client.get_secret_value(SecretId=secret_arn)
        return resp["SecretString"].encode("utf-8")
    return os.environ["TOKEN_SIGNING_SECRET"].encode("utf-8")


def _sign(token_id: str) -> str:
    """HMAC-SHA256 over the token id, truncated for a shorter URL. This is
    defense in depth against row-id guessing against the tokens table --
    the actual authority for whether an unsubscribe applies still comes
    from the DynamoDB lookup, not from the signature alone."""
    secret = get_token_signing_secret()
    digest = hmac.new(secret, token_id.encode("utf-8"), hashlib.sha256).hexdigest()
    return digest[:16]


# --------------------------------------------------------------------------
# Subscriber identity mapping: internal_id <-> (email, phone, name) <-> Paubox
# subscriber UUID.
#
# This is the layer Paubox's own guidance describes: an internal ID alone
# is not a substitute for a Paubox subscriber identifier, and Marketing API
# operations need the Paubox UUID, while Mail API sends need the recipient
# email address -- so both must be resolvable from your own internal ID,
# server-side, without ever handing the UUID (or the internal ID) to a
# browser, client, template, or the recipient themselves.
#
# resolve_or_create_subscriber() is the one place that UUID gets resolved
# and then cached. Everything else in this file (mint_unsubscribe_token,
# apply_action) should read the cached UUID from here rather than calling
# PauboxClient.find_subscriber_id_by_email() fresh on every action -- that
# method still exists and is used as the fallback *inside* this function,
# not as a per-request lookup on its own anymore.
# --------------------------------------------------------------------------

def resolve_or_create_subscriber(
    paubox: PauboxClient,
    internal_id: str,
    email: str,
    phone: str | None = None,
    name: str | None = None,
) -> dict:
    """
    Looks up internal_id in your own subscribers table. If it already has
    a cached paubox_subscriber_uuid, returns it as-is -- no Paubox call at
    all. Otherwise resolves via Paubox search (or creates a new Paubox
    subscriber if none exists), then persists the mapping so this is a
    one-time cost per subscriber, not a per-action one.

    This is the function your outbound-mail pipeline should call when
    composing a send: pass your internal_id and the subscriber's current
    email/phone/name, get back a record containing the Paubox UUID for
    Marketing API operations -- and use the plain `email` field, not the
    UUID, when building the Mail API request itself.
    """
    subscribers_table = dynamodb.Table(SUBSCRIBERS_TABLE_NAME)
    existing = subscribers_table.get_item(Key={"internal_id": internal_id}).get("Item")

    if existing and existing.get("paubox_subscriber_uuid") and existing.get("email", "").lower() == email.lower():
        return existing

    paubox_subscriber_uuid = paubox.find_subscriber_id_by_email(email)
    if not paubox_subscriber_uuid:
        paubox_subscriber_uuid = paubox.create_subscriber(email)

    record = {
        "internal_id": internal_id,
        "email": email,
        "phone": phone,
        "name": name,
        "paubox_subscriber_uuid": paubox_subscriber_uuid,
        "resolved_at": _now_iso(),
    }
    subscribers_table.put_item(Item=record)
    return record


def mint_unsubscribe_token(
    paubox_message_id: str,
    sender_email: str,
    sender_domain: str,
    party_role: str,
    sender_class: str,
    campaign_tags: list[str] | None = None,
    ttl_days: int = TOKEN_TTL_DAYS,
    internal_id: str | None = None,
    paubox_subscriber_uuid: str | None = None,
) -> str:
    """
    Call this at send time (from your outbound-mail pipeline, not from the
    unsubscribe HTTP handler) to mint the token embedded in that message's
    unsubscribe URL, e.g. https://yo-ai.ai/unsubscribe?t=<returned value>.

    Pass internal_id and paubox_subscriber_uuid when you have them (i.e.
    you already called resolve_or_create_subscriber() to build this send)
    so the click-time handler can act on the cached UUID directly instead
    of re-resolving it via Paubox search. Both are optional so this still
    works for a one-off action with no prior subscriber record.

    Raises ValueError if party_role or sender_class aren't in your
    taxonomy -- fails loudly at send time rather than minting a token this
    function won't be able to make sense of later.
    """
    if party_role not in VALID_PARTY_ROLES:
        raise ValueError(f"party_role must be one of {sorted(VALID_PARTY_ROLES)}, got {party_role!r}")
    if sender_class not in VALID_SENDER_CLASSES:
        raise ValueError(f"sender_class must be one of {sorted(VALID_SENDER_CLASSES)}, got {sender_class!r}")

    token_id = str(uuid.uuid4())
    signature = _sign(token_id)
    token = f"{token_id}.{signature}"

    now = _now_iso()
    expires_at = int((datetime.now(timezone.utc) + timedelta(days=ttl_days)).timestamp())

    tokens_table = dynamodb.Table(TOKENS_TABLE_NAME)
    tokens_table.put_item(Item={
        "token_id": token_id,
        "paubox_message_id": paubox_message_id,
        "sender_email": sender_email,
        "sender_domain": sender_domain,
        "internal_id": internal_id,
        "paubox_subscriber_uuid": paubox_subscriber_uuid,
        "party_role": party_role,
        "sender_class": sender_class,
        "campaign_tags": campaign_tags or [],
        "minted_at": now,
        "expires_at": expires_at,  # DynamoDB TTL attribute -- configure TTL on this table for this field
        "consumed_count": 0,
    })

    return token


class TokenError(Exception):
    """Raised when an incoming token is missing, malformed, expired, or unknown. Mapped to HTTP 400."""


def resolve_token(token: str) -> dict:
    """
    Looks up an incoming token against the token registry and returns the
    stored record. Called by the HTTP handler before any Paubox call.
    Increments consumed_count for visibility (e.g. spotting a token that's
    been hit an unusual number of times) -- it does NOT reject repeat use,
    since an unsubscribe link being clicked more than once (or hit by both
    a human and, separately, their agent) should stay idempotent rather
    than erroring.
    """
    if not token or "." not in token:
        raise TokenError("Malformed or missing unsubscribe token")

    token_id, _, signature = token.partition(".")
    expected_signature = _sign(token_id)
    if not hmac.compare_digest(signature, expected_signature):
        raise TokenError("Token signature does not match")

    tokens_table = dynamodb.Table(TOKENS_TABLE_NAME)
    resp = tokens_table.get_item(Key={"token_id": token_id})
    record = resp.get("Item")
    if not record:
        raise TokenError("Unknown or expired unsubscribe token")

    if int(record["expires_at"]) < int(time.time()):
        raise TokenError("Unsubscribe token has expired")

    tokens_table.update_item(
        Key={"token_id": token_id},
        UpdateExpression="SET consumed_count = consumed_count + :one",
        ExpressionAttributeValues={":one": 1},
    )

    return record


# --------------------------------------------------------------------------
# Payload normalization + validation
# --------------------------------------------------------------------------

def normalize_legacy_payload(body: dict) -> dict:
    """Maps the flat Paubox Forms shape onto the internal TrustedSenderAction shape."""
    email = body.get("CTP_identifier")
    if not email:
        raise ValidationError("CTP_identifier (email) is required")

    return {
        "action": "unsubscribe",
        "scope": {
            "sender_email": email,
            "extend_to_domain": False,
            "intermediary_parties": [],
            "transports": [],
        },
        "unsubscribe_categories": body.get("unsubscribe_categories", []),
        "reason": body.get("unsubscribe_reason"),
        "signature": body.get("signature"),
        "requester": {
            "platform": "yo-ai.ai",
            "requester_id": body.get("CTP_identifier", "unknown"),
            "submitted_by": "human",
        },
        "event_timestamp": body.get("M_event_date") or _now_iso(),
    }


def validate_action(body: dict) -> dict:
    """Validates a (post-normalization) TrustedSenderAction payload. Returns it unchanged if valid."""
    action = body.get("action")
    if action not in VALID_ACTIONS:
        raise ValidationError(f"action must be one of {sorted(VALID_ACTIONS)}, got {action!r}")

    scope = body.get("scope")
    if not isinstance(scope, dict):
        raise ValidationError("scope object is required")

    sender_email = scope.get("sender_email")
    sender_domain = scope.get("sender_domain")
    if not sender_email and not sender_domain:
        raise ValidationError("scope.sender_email or scope.sender_domain is required")

    if sender_email and "@" not in sender_email:
        raise ValidationError(f"scope.sender_email is not a valid email: {sender_email!r}")

    for transport in scope.get("transports", []):
        if transport.get("type") not in VALID_TRANSPORT_TYPES:
            raise ValidationError(f"invalid transport type: {transport.get('type')!r}")
        if transport.get("action") not in VALID_ACTIONS:
            raise ValidationError(f"invalid transport action: {transport.get('action')!r}")

    requester = body.get("requester")
    if not isinstance(requester, dict) or "platform" not in requester or "submitted_by" not in requester:
        raise ValidationError("requester.platform and requester.submitted_by are required")

    if requester["submitted_by"] not in ("human", "agent"):
        raise ValidationError("requester.submitted_by must be 'human' or 'agent'")

    return body


def check_scope_authority(body: dict) -> None:
    """
    Placeholder authority check for domain-wide actions. In production this
    should confirm the requester actually controls sender_domain (e.g. via
    a verified-domain table) before allowing extend_to_domain=true. Wired
    as a hard stop here so the behavior is explicit rather than silently
    permissive; replace the condition below with a real ownership lookup.
    """
    scope = body["scope"]
    if scope.get("extend_to_domain") and not scope.get("sender_domain"):
        raise ScopeConflictError("extend_to_domain=true requires scope.sender_domain to be set")
    # TODO: verify requester authority over scope["sender_domain"] here.


# --------------------------------------------------------------------------
# Action application
# --------------------------------------------------------------------------

def resolve_targets(paubox: PauboxClient, scope: dict) -> list[str]:
    """
    Returns the list of Paubox subscriber UUIDs the Paubox-enforceable part
    of this action applies to. Prefers a cached UUID (threaded through from
    a resolved token -- see _action_body_from_token) over a fresh Paubox
    search, since the whole point of resolve_or_create_subscriber() is to
    make that search a one-time cost rather than a per-action one.
    """
    if scope.get("cached_paubox_subscriber_uuid"):
        return [scope["cached_paubox_subscriber_uuid"]]
    if scope.get("extend_to_domain") and scope.get("sender_domain"):
        targets = paubox.find_subscriber_ids_by_domain(scope["sender_domain"])
        return targets  # list of subscriber_ids, already resolved
    if scope.get("sender_email"):
        subscriber_id = paubox.find_subscriber_id_by_email(scope["sender_email"])
        return [subscriber_id] if subscriber_id else []
    return []


def resolve_list_ids(unsubscribe_categories: list[str]) -> list[str] | None:
    if not unsubscribe_categories:
        return None
    list_ids = [CATEGORY_LIST_ID_MAP[c] for c in unsubscribe_categories if c in CATEGORY_LIST_ID_MAP]
    return list_ids or None


def apply_action(paubox: PauboxClient, body: dict) -> dict:
    """
    Applies the action against Paubox for the email transport, and reports
    what happened for every other requested scope element that Paubox has
    no way to enforce.
    """
    action = body["action"]
    scope = body["scope"]

    email_in_scope = True
    transports = scope.get("transports", [])
    if transports:
        # If transports were explicitly specified, only apply to Paubox
        # when "email" is one of them.
        email_in_scope = any(t["type"] == "email" for t in transports)

    result = {
        "paubox_applied": False,
        "paubox_response": None,
        "matched_subscriber_count": 0,
        "unenforceable_scope_elements": [],
    }

    if scope.get("intermediary_parties"):
        result["unenforceable_scope_elements"].append(
            f"{len(scope['intermediary_parties'])} intermediary_parties recorded for audit only "
            "-- Paubox has no mechanism to restrict a third party's own data handling."
        )
    for t in transports:
        if t["type"] != "email":
            result["unenforceable_scope_elements"].append(
                f"transport '{t['type']}' recorded for audit only -- not a Paubox-managed channel."
            )

    if action not in PAUBOX_ENFORCEABLE_ACTIONS:
        result["unenforceable_scope_elements"].append(
            f"action '{action}' has no Paubox equivalent -- recorded for audit only."
        )
        return result

    if not email_in_scope:
        return result

    subscriber_ids = resolve_targets(paubox, scope)
    result["matched_subscriber_count"] = len(subscriber_ids)

    if not subscriber_ids:
        # unsubscribe/block on someone who isn't a known Paubox subscriber
        # is a no-op there's nothing to suppress. resubscribe with no
        # match is also a no-op. Both are recorded, neither is an error.
        return result

    list_ids = resolve_list_ids(body.get("unsubscribe_categories", []))

    if action in ("unsubscribe", "block"):
        response = paubox.unsubscribe(subscriber_ids, subscription_list_ids=list_ids)
    else:  # resubscribe
        response = paubox.subscribe(subscriber_ids, subscription_list_ids=list_ids)

    result["paubox_response"] = response
    result["paubox_applied"] = "errors" not in response
    return result


# --------------------------------------------------------------------------
# Storage + logging
# --------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def compute_trust_status(action: str, apply_result: dict) -> str:
    if action == "block":
        return "Blocked"
    if action == "unsubscribe":
        return "Unsubscribed"
    if action == "limit":
        return "DualUseVendor" if apply_result["unenforceable_scope_elements"] else "MarketingSender"
    if action == "resubscribe":
        return "MarketingSender"
    return "UnknownVendor"


def store_registry_and_audit(
    body: dict,
    apply_result: dict,
    trust_status: str,
    audit_log_id: str,
    token_record: dict | None = None,
) -> None:
    scope = body["scope"]
    sender_key = scope.get("sender_email") or f"domain:{scope.get('sender_domain')}"
    now = _now_iso()

    # party_role / sender_class / campaign_tags come from the token minted
    # at send time, if this request arrived via a token. Direct agent calls
    # with no token have no send-time taxonomy to inherit -- those fields
    # are simply absent, not guessed at.
    party_role = token_record.get("party_role") if token_record else None
    sender_class = token_record.get("sender_class") if token_record else None
    campaign_tags = token_record.get("campaign_tags", []) if token_record else []
    paubox_message_id = token_record.get("paubox_message_id") if token_record else None

    registry_table = dynamodb.Table(REGISTRY_TABLE_NAME)
    registry_table.put_item(Item={
        "sender_key": sender_key,
        "trust_status": trust_status,
        "party_role": party_role,
        "sender_class": sender_class,
        "campaign_tags": campaign_tags,
        "last_action": body["action"],
        "last_scope": json.dumps(scope),
        "last_audit_log_id": audit_log_id,
        "updated_at": now,
    })

    audit_table = dynamodb.Table(AUDIT_TABLE_NAME)
    audit_table.put_item(Item={
        "audit_log_id": audit_log_id,
        "sender_key": sender_key,
        "action": body["action"],
        "scope": json.dumps(scope),
        "reason": body.get("reason"),
        "requester": json.dumps(body["requester"]),
        "signature": body.get("signature"),
        "party_role": party_role,
        "sender_class": sender_class,
        "campaign_tags": campaign_tags,
        "paubox_message_id": paubox_message_id,
        "apply_result": json.dumps({
            k: v for k, v in apply_result.items() if k != "paubox_response"
        } | ({"paubox_response": apply_result["paubox_response"]} if apply_result["paubox_response"] else {})),
        "trust_status": trust_status,
        "event_timestamp": body.get("event_timestamp", now),
        "recorded_at": now,
    })

    logger.info(json.dumps({
        "event": "trusted_sender_action",
        "audit_log_id": audit_log_id,
        "sender_key": sender_key,
        "action": body["action"],
        "trust_status": trust_status,
        "party_role": party_role,
        "sender_class": sender_class,
        "campaign_tags": campaign_tags,
        "matched_subscriber_count": apply_result["matched_subscriber_count"],
        "paubox_applied": apply_result["paubox_applied"],
    }))


# --------------------------------------------------------------------------
# Lambda entry point
# --------------------------------------------------------------------------

def _response(status_code: int, payload: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(payload),
    }


def _extract_incoming_token(event: dict, body: dict) -> str | None:
    """
    A token can arrive two ways: as a query string param on a plain GET
    click (?t=...), or as a "token" field in a POST body (agent calls, or
    a richer landing page that lets someone pick LIMIT/BLOCK before
    submitting). Query string takes precedence since it's the simple
    one-click case this whole design is built around.
    """
    query_params = event.get("queryStringParameters") or {}
    if query_params.get("t"):
        return query_params["t"]
    if isinstance(body, dict) and body.get("token"):
        return body["token"]
    return None


def _action_body_from_token(token_record: dict, requested_action: str | None) -> dict:
    """
    Builds a scope-bearing action payload from a resolved token. Defaults
    to a global "unsubscribe" -- the one-click case -- unless the request
    explicitly asked for something else (e.g. a landing page where the
    sender picked LIMIT or BLOCK; still keyed off the same token so the
    Message-ID / sender / taxonomy linkage is identical either way).
    """
    action = requested_action if requested_action in VALID_ACTIONS else "unsubscribe"
    return {
        "action": action,
        "scope": {
            "sender_email": token_record["sender_email"],
            "sender_domain": token_record.get("sender_domain"),
            "extend_to_domain": False,
            "intermediary_parties": [],
            "transports": [],
            # Cached from resolve_or_create_subscriber() at mint time, if
            # available -- lets resolve_targets() skip a fresh Paubox
            # search entirely. Falls back to search (via sender_email)
            # when a token was minted before a subscriber record existed.
            "cached_paubox_subscriber_uuid": token_record.get("paubox_subscriber_uuid"),
        },
        "reason": "token_click",
        "requester": {
            "platform": "yo-ai.ai",
            "requester_id": token_record["token_id"],
            "submitted_by": "human",
        },
        "event_timestamp": _now_iso(),
    }


def lambda_handler(event, context):
    route = event.get("rawPath") or event.get("path", "")
    http_method = (event.get("requestContext", {}).get("http", {}).get("method")
                   or event.get("httpMethod", "GET"))

    try:
        body = json.loads(event.get("body") or "{}") if event.get("body") else {}
    except json.JSONDecodeError:
        return _response(400, {"status": "error", "message": "Body is not valid JSON", "code": "invalid_json"})

    token_record = None
    incoming_token = _extract_incoming_token(event, body)

    try:
        if incoming_token:
            # Token path: resolve identity server-side before Paubox is
            # ever touched. No IP/cookie/pixel/UUID-from-Paubox needed --
            # the token is the only identifier this flow relies on.
            token_record = resolve_token(incoming_token)
            requested_action = (event.get("queryStringParameters") or {}).get("action") or body.get("action")
            action_body = _action_body_from_token(token_record, requested_action)
        elif route.endswith("/unsubscribe"):
            action_body = normalize_legacy_payload(body)
        else:
            # Direct fine-grained call, no token -- the caller (an
            # authenticated agent) is identifying its own target directly.
            action_body = body

        action_body = validate_action(action_body)
        check_scope_authority(action_body)

    except TokenError as e:
        return _response(400, {"status": "error", "message": str(e), "code": "invalid_token"})
    except ValidationError as e:
        return _response(400, {"status": "error", "message": str(e), "code": "validation_error"})
    except ScopeConflictError as e:
        return _response(409, {"status": "error", "message": str(e), "code": "scope_conflict"})

    try:
        api_key = get_paubox_api_key()
    except Exception:
        logger.exception("Unable to retrieve Paubox API key")
        return _response(500, {"status": "error", "message": "Server configuration error", "code": "config_error"})

    paubox = PauboxClient(api_key)

    try:
        apply_result = apply_action(paubox, action_body)
    except Exception:
        logger.exception("Error applying action against Paubox")
        return _response(500, {"status": "error", "message": "Upstream error applying action", "code": "upstream_error"})

    trust_status = compute_trust_status(action_body["action"], apply_result)
    audit_log_id = str(uuid.uuid4())

    try:
        store_registry_and_audit(action_body, apply_result, trust_status, audit_log_id, token_record=token_record)
    except Exception:
        # The Paubox-side action already happened; a storage failure here
        # should not report "error" to the caller, but it must be loud in
        # CloudWatch so it gets investigated -- an audit gap is a real
        # problem for this use case specifically.
        logger.exception("CRITICAL: Paubox action applied but registry/audit write failed. audit_log_id=%s", audit_log_id)

    status = "success" if not apply_result["unenforceable_scope_elements"] else "partial"
    message_parts = []
    if apply_result["matched_subscriber_count"]:
        message_parts.append(f"Applied to {apply_result['matched_subscriber_count']} matched subscriber(s).")
    elif action_body["action"] in PAUBOX_ENFORCEABLE_ACTIONS:
        message_parts.append("No matching Paubox subscriber found; nothing to suppress there.")
    message_parts.extend(apply_result["unenforceable_scope_elements"])

    return _response(200, {
        "status": status,
        "message": " ".join(message_parts) or "Recorded.",
        "trust_status": trust_status,
        "effective_scope": action_body["scope"],
        "audit_log_id": audit_log_id,
        "event_date": _now_iso(),
    })


# --------------------------------------------------------------------------
# README (deployment notes)
# --------------------------------------------------------------------------
#
# Runtime: Python 3.10+ (uses PEP 604 `str | None` unions).
#
# Dependencies: none beyond boto3, which ships with the Lambda runtime --
# no layer or requirements.txt needed for this file as-is.
#
# IAM permissions needed by the execution role:
#   - dynamodb:PutItem on REGISTRY_TABLE_NAME and AUDIT_TABLE_NAME
#   - dynamodb:PutItem, GetItem, UpdateItem on TOKENS_TABLE_NAME
#   - dynamodb:PutItem, GetItem on SUBSCRIBERS_TABLE_NAME
#   - secretsmanager:GetSecretValue on PAUBOX_API_KEY_SECRET_ARN and
#     TOKEN_SIGNING_SECRET_ARN
#
# DynamoDB tables (on-demand billing is fine at this volume):
#   trustedsender_registry:  partition key "sender_key" (String)
#   trustedsender_audit:     partition key "audit_log_id" (String)
#     Consider a GSI on sender_key + event_timestamp for "show me this
#     sender's full history" queries later.
#   trustedsender_tokens:    partition key "token_id" (String)
#     Enable DynamoDB TTL on the "expires_at" attribute so spent/expired
#     tokens age out automatically instead of accumulating forever.
#   trustedsender_subscribers: partition key "internal_id" (String)
#     The mapping layer Paubox's own guidance describes: internal_id ->
#     email/phone/name -> cached paubox_subscriber_uuid. Call
#     resolve_or_create_subscriber() from your send-time pipeline, not
#     from this Lambda's HTTP handler, and reuse its result across sends
#     rather than re-resolving the UUID from Paubox each time.
#
# API Gateway: route GET+POST /unsubscribe and POST /trusted-sender/action
# to this same function; the handler distinguishes them by path and method.
# The one-click link in an outbound message should be a plain GET to
# /unsubscribe?t=<token> -- no JSON body needed for the default case.
#
# Send-time integration: call mint_unsubscribe_token(...) from whatever
# code composes and sends the original message (not from this Lambda),
# using the Paubox Message-ID you get back from the send call, and embed
# the returned token in that message's unsubscribe URL.
#
# Things this implementation deliberately does NOT do yet:
#   - Signature verification on the *action payload's* `signature` field
#     (separate from token-signature verification, which IS implemented).
#     `signature` on a submitted action is stored, not cryptographically
#     checked. Wire in verification before treating it as non-repudiation
#     evidence.
#   - Domain-ownership check for extend_to_domain (see check_scope_authority).
#     Right now any request with sender_domain set can sweep every known
#     subscriber at that domain; add a verified-domain lookup before this
#     goes anywhere near production.
#   - Non-email transports (voice/SMS/chat/social) and Intermediary Party
#     scoping have no enforcement path at all -- there's no third-party API
#     to call. They're recorded for the audit trail and surfaced in the
#     response's unenforceable_scope_elements, nothing more.
#   - Rate limiting / abuse protection on token resolution. resolve_token()
#     intentionally never rejects a repeat click (idempotent by design),
#     but that also means nothing currently stops rapid brute-force
#     guessing against /unsubscribe?t=... beyond the HMAC signature check.
#     Put this behind API Gateway throttling at minimum.
