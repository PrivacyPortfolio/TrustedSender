TrustedSenderRegistry.md

The following table contains event records pertaining to a Sender: 
{
  "table": "registry",
  "primary_key": "sender_key",
  "records": [
    {
      "sender_key": "jane@example.com",
      "trust_status": "Unsubscribed",
      "party_role": "counter_party",
      "sender_class": "MarketingSender",
      "campaign_tags": [
        "newsletter"
      ],
      "last_action": "unsubscribe",
      "last_scope": {
        "sender_email": "jane@example.com",
        "sender_domain": "example.com",
        "extend_to_domain": false,
        "intermediary_parties": [],
        "transports": [],
        "cached_paubox_subscriber_uuid": "123e4567-e89b-12d3-a456-426614174000"
      },
      "last_audit_log_id": "0a1b2c3d-1111-2222-3333-444455556666",
      "updated_at": "2026-10-22T17:05:00+00:00"
    }
  ]
}


The following table contains properties pertaining to a Sender: 

{
  "table": "subscribers",
  "primary_key": "internal_id",
  "records": [
    {
      "internal_id": "usr_1001",
      "email": "jane@example.com",
      "phone": "",
      "name": "Jane Doe",
      "paubox_subscriber_uuid": "123e4567-e89b-12d3-a456-426614174000",
      "resolved_at": "2026-10-22T17:00:00+00:00"
    }
  ]
}


The following table contains a list of Senders mapped to Paubox subscribers: 

{
  "subscribers": {
    "source": "SUBSCRIBERS_TABLE_NAME (trustedsender_subscribers)",
    "primary_key": "internal_id",
    "description": "Your internal ID <-> contact details <-> cached Paubox subscriber UUID.",
    "columns": [
      {
        "name": "internal_id",
        "type": "string",
        "key": "PK",
        "notes": "Your own subscriber ID",
        "paubox_mapping": "(none - your system's key)"
      },
      {
        "name": "email",
        "type": "string",
        "key": null,
        "notes": "Subscriber email",
        "paubox_mapping": "subscriber.attributes.email"
      },
      {
        "name": "phone",
        "type": "string|null",
        "key": null,
        "notes": "Optional",
        "paubox_mapping": "not used by this code against Paubox - verify in Paubox docs"
      },
      {
        "name": "name",
        "type": "string|null",
        "key": null,
        "notes": "Optional",
        "paubox_mapping": "not used by this code against Paubox - verify in Paubox docs"
      },
      {
        "name": "paubox_subscriber_uuid",
        "type": "string",
        "key": null,
        "notes": "Paubox subscriber ID",
        "paubox_mapping": "subscriber.id (the Paubox UUID)"
      },
      {
        "name": "resolved_at",
        "type": "string (ISO 8601 UTC)",
        "key": null,
        "notes": "When the UUID was resolved/cached",
        "paubox_mapping": "(none)"
      }
    ],
    "sample_row": {
      "internal_id": "usr_1001",
      "email": "jane@example.com",
      "phone": "",
      "name": "Jane Doe",
      "paubox_subscriber_uuid": "123e4567-e89b-12d3-a456-426614174000",
      "resolved_at": "2026-10-22T17:00:00+00:00"
    }
  }

The following table contains properties embedded in a customized token used to unsubscribe Senders from Paubox subscribers: 

  "tokens": {
    "source": "TOKENS_TABLE_NAME (trustedsender_tokens)",
    "primary_key": "token_id",
    "description": "Opaque unsubscribe tokens minted at send time. Ephemeral; TTL on expires_at.",
    "columns": [
      {
        "name": "token_id",
        "type": "string (uuid4)",
        "key": "PK",
        "notes": "Public token = token_id + '.' + HMAC signature (signature is NOT stored)",
        "paubox_mapping": "(none)"
      },
      {
        "name": "paubox_message_id",
        "type": "string",
        "key": null,
        "notes": "Paubox Message-ID from the send call",
        "paubox_mapping": "(none)"
      },
      {
        "name": "sender_email",
        "type": "string",
        "key": null,
        "notes": "Address the action applies to",
        "paubox_mapping": "subscriber.attributes.email (lookup key)"
      },
      {
        "name": "sender_domain",
        "type": "string",
        "key": null,
        "notes": "Domain of sender_email",
        "paubox_mapping": "(none)"
      },
      {
        "name": "internal_id",
        "type": "string|null",
        "key": null,
        "notes": "FK -> subscribers.internal_id",
        "paubox_mapping": "(none)"
      },
      {
        "name": "paubox_subscriber_uuid",
        "type": "string|null",
        "key": null,
        "notes": "FK -> Paubox subscriber",
        "paubox_mapping": "subscriber.id"
      },
      {
        "name": "party_role",
        "type": "enum",
        "key": null,
        "notes": "intermediary_party|controlling_party|counter_party|stakeholder",
        "paubox_mapping": "(none)"
      },
      {
        "name": "sender_class",
        "type": "enum",
        "key": null,
        "notes": "Trusted|Untrusted|PHI|Marketing|Operational|DualUse|Sponsored|Visiting|Unknown",
        "paubox_mapping": "(none)"
      },
      {
        "name": "campaign_tags",
        "type": "array<string>",
        "key": null,
        "notes": "CSV: JSON array string",
        "paubox_mapping": "(none)"
      },
      {
        "name": "minted_at",
        "type": "string (ISO 8601 UTC)",
        "key": null,
        "notes": "",
        "paubox_mapping": "(none)"
      },
      {
        "name": "expires_at",
        "type": "integer (epoch seconds)",
        "key": null,
        "notes": "TTL attribute",
        "paubox_mapping": "(none)"
      },
      {
        "name": "consumed_count",
        "type": "integer",
        "key": null,
        "notes": "Click counter, starts at 0",
        "paubox_mapping": "(none)"
      }
    ],
    "sample_row": {
      "token_id": "b7c1f2a0-5d3e-4c1a-9e0b-2f6a8d4c7e11",
      "paubox_message_id": "<msg-id@paubox.com>",
      "sender_email": "jane@example.com",
      "sender_domain": "example.com",
      "internal_id": "usr_1001",
      "paubox_subscriber_uuid": "123e4567-e89b-12d3-a456-426614174000",
      "party_role": "counter_party",
      "sender_class": "MarketingSender",
      "campaign_tags": [
        "newsletter",
        "oct-2026"
      ],
      "minted_at": "2026-10-22T17:00:00+00:00",
      "expires_at": 1792688400,
      "consumed_count": 0
    }
  }

The following table contains event log records for the custom unsubscribe method,
which can be mapped to Paubox subscribers, 
setting unsubscribed:true for the subscriptions matching a Message-ID AND the Template-ID.

{
  "table": "audit",
  "primary_key": "audit_log_id",
  "records": [
    {
      "audit_log_id": "0a1b2c3d-1111-2222-3333-444455556666",
      "sender_key": "jane@example.com",
      "action": "unsubscribe",
      "scope": {
        "sender_email": "jane@example.com",
        "sender_domain": "example.com",
        "extend_to_domain": false,
        "intermediary_parties": [],
        "transports": [],
        "cached_paubox_subscriber_uuid": "123e4567-e89b-12d3-a456-426614174000"
      },
      "reason": "token_click",
      "requester": {
        "platform": "yo-ai.ai",
        "requester_id": "b7c1f2a0-5d3e-4c1a-9e0b-2f6a8d4c7e11",
        "submitted_by": "human"
      },
      "signature": null,
      "party_role": "counter_party",
      "sender_class": "MarketingSender",
      "campaign_tags": [
        "newsletter"
      ],
      "paubox_message_id": "<msg-id@paubox.com>",
      "apply_result": {
        "paubox_applied": true,
        "matched_subscriber_count": 1,
        "unenforceable_scope_elements": []
      },
      "trust_status": "Unsubscribed",
      "event_timestamp": "2026-10-22T17:05:00+00:00",
      "recorded_at": "2026-10-22T17:05:01+00:00"
    }
  ]
}

