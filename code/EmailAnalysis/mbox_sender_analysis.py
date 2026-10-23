#!/usr/bin/env python3
"""
mbox_sender_analysis.py

Parses exported mbox files (Gmail Takeout, ProtonMail export, etc.) and
builds a per-sender decision-factors report, for use BEFORE sending
ChangeOfAddress notifications during domain migration — i.e. the
"Move & Lose" gate: senders who don't clear the bar don't get notified
of your new address.

SCOPE / LIMITATIONS (read before trusting the output)
--------------------------------------------------------
This works ONLY from what's already present in stored headers. It does
NOT and CANNOT do:
  - Live SPF/DKIM/DMARC re-verification (the DNS state at send time is
    gone; you're trusting whatever verdict, if any, was stamped into
    Authentication-Results by the receiving mail system at the time)
  - Live TLS/MTA-STS/DNSSEC checks (no live connection possible)
  - Reputation lookups (Spamhaus/Talos/etc. — those reflect present-day
    state, not historical, and querying them per-sender at export scale
    would need a separate rate-limited pass, not included here)

What it CAN do reliably from static headers:
  - Parse whatever Authentication-Results verdict was stamped, if any
    (different providers stamp this differently or not at all — treat
    absence as "unknown", never as "fail")
  - Detect no-reply patterns, Precedence: bulk, List-Unsubscribe presence
  - Detect Reply-To vs From mismatches
  - Detect whether YOU (the mailbox owner) ever sent a message to this
    address — i.e. actual bidirectional engagement, not just inferred
    reachability. This is the strongest signal available from an export
    and is added specifically because it doesn't require guessing.
  - Aggregate frequency and recency per sender across the whole mailbox

Everything this script outputs is DATA-tier or a simple count-based
aggregate of DATA. It does not generate INFERENCE-tier prose — that's
a separate step you or a downstream process should apply deliberately,
not something to bake into a bulk automated pass silently.

USAGE
-----
    python3 mbox_sender_analysis.py path/to/export.mbox --out report.json --csv report.csv

    Multiple mbox files (e.g. one per provider) can be merged:
    python3 mbox_sender_analysis.py gmail.mbox proton.mbox --out combined.json --csv combined.csv
"""

import argparse
import csv
import datetime
import email.utils
import json
import mailbox
import re
from collections import defaultdict


AUTH_RESULT_RE = {
    "spf": re.compile(r"\bspf\s*=\s*(\w+)", re.IGNORECASE),
    "dkim": re.compile(r"\bdkim\s*=\s*(\w+)", re.IGNORECASE),
    "dmarc": re.compile(r"\bdmarc\s*=\s*(\w+)", re.IGNORECASE),
}

NOREPLY_PATTERN = re.compile(r"no.?reply|do.?not.?reply|donotreply", re.IGNORECASE)


def parse_auth_results(msg) -> dict:
    """Extract whatever SPF/DKIM/DMARC verdicts are present in any
    Authentication-Results header. Providers vary in whether/how they
    stamp this; absence means 'unknown', not 'fail'."""
    results = {"spf": None, "dkim": None, "dmarc": None}
    for header_value in msg.get_all("Authentication-Results", []):
        for key, pattern in AUTH_RESULT_RE.items():
            match = pattern.search(header_value)
            if match and results[key] is None:
                results[key] = match.group(1).lower()
    return results


def get_address(msg, header_name: str):
    raw = msg.get(header_name)
    if not raw:
        return None, None
    _, addr = email.utils.parseaddr(raw)
    addr = addr.lower().strip()
    domain = addr.split("@")[-1] if "@" in addr else None
    return addr or None, domain


def get_date(msg):
    raw = msg.get("Date")
    if not raw:
        return None
    try:
        dt = email.utils.parsedate_to_datetime(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        return dt
    except (TypeError, ValueError):
        return None


def is_sent_message(msg) -> bool:
    """Best-effort detection of whether a message was SENT by the mailbox
    owner rather than received. Checks two independent signals depending
    on the export source:
      - X-Gmail-Labels: stamped by Gmail Takeout exports
      - X-Source-Folder: stamped by imap_to_mbox.py for IMAP exports
        (Comcast, ProtonMail, etc.), set to the actual IMAP folder name
    Falls back to None (unknown) rather than guessing wrong if neither
    signal is present."""
    labels = msg.get("X-Gmail-Labels", "")
    if "Sent" in labels:
        return True
    if "Inbox" in labels or "Received" in labels:
        return False

    source_folder = msg.get("X-Source-Folder", "")
    if source_folder:
        # Case-insensitive match against common "sent" folder naming
        # conventions across providers (Sent, Sent Items, Sent Mail, etc.)
        if re.search(r"sent", source_folder, re.IGNORECASE):
            return True
        # Anything else with an X-Source-Folder value is a real IMAP
        # folder that isn't a sent folder — treat as received.
        return False

    return None  # unknown — neither signal present


def analyze_mbox(paths):
    # sender_key (address) -> aggregate record
    senders = defaultdict(lambda: {
        "address": None,
        "domain": None,
        "message_count": 0,
        "first_seen": None,
        "last_seen": None,
        "auth_spf_seen": set(),
        "auth_dkim_seen": set(),
        "auth_dmarc_seen": set(),
        "reply_to_mismatch_count": 0,
        "precedence_bulk_count": 0,
        "list_unsubscribe_present_count": 0,
        "noreply_address_count": 0,
        "user_replied_to_this_sender": False,  # set True if we ever sent TO this address
        "subjects_sample": [],
    })

    sent_to_addresses = set()  # addresses the mailbox owner sent mail to

    total_messages = 0
    unparsed = 0

    # First pass: build the set of addresses the owner sent mail to,
    # so we can mark engagement regardless of message order in the file.
    for path in paths:
        try:
            mbox = mailbox.mbox(path)
        except Exception as e:
            print(f"WARNING: could not open {path}: {e}")
            continue
        for msg in mbox:
            total_messages += 1
            if is_sent_message(msg):
                to_addr, _ = get_address(msg, "To")
                if to_addr:
                    sent_to_addresses.add(to_addr)

    # Second pass: aggregate per-sender data for received messages.
    for path in paths:
        try:
            mbox = mailbox.mbox(path)
        except Exception as e:
            continue
        for msg in mbox:
            sent_flag = is_sent_message(msg)
            if sent_flag is True:
                continue  # skip the owner's own sent messages for sender stats

            from_addr, from_domain = get_address(msg, "From")
            if not from_addr:
                unparsed += 1
                continue

            rec = senders[from_addr]
            rec["address"] = from_addr
            rec["domain"] = from_domain
            rec["message_count"] += 1

            date = get_date(msg)
            if date:
                if rec["first_seen"] is None or date < rec["first_seen"]:
                    rec["first_seen"] = date
                if rec["last_seen"] is None or date > rec["last_seen"]:
                    rec["last_seen"] = date

            auth = parse_auth_results(msg)
            if auth["spf"]:
                rec["auth_spf_seen"].add(auth["spf"])
            if auth["dkim"]:
                rec["auth_dkim_seen"].add(auth["dkim"])
            if auth["dmarc"]:
                rec["auth_dmarc_seen"].add(auth["dmarc"])

            reply_to_addr, _ = get_address(msg, "Reply-To")
            if reply_to_addr and reply_to_addr != from_addr:
                rec["reply_to_mismatch_count"] += 1

            precedence = (msg.get("Precedence") or "").lower()
            if precedence in ("bulk", "list", "junk"):
                rec["precedence_bulk_count"] += 1

            if msg.get("List-Unsubscribe"):
                rec["list_unsubscribe_present_count"] += 1

            if NOREPLY_PATTERN.search(from_addr):
                rec["noreply_address_count"] += 1

            if from_addr in sent_to_addresses:
                rec["user_replied_to_this_sender"] = True

            subject = msg.get("Subject", "")
            if subject and len(rec["subjects_sample"]) < 3:
                rec["subjects_sample"].append(subject)

    return senders, total_messages, unparsed


def build_report(senders: dict):
    report = []
    for addr, rec in senders.items():
        first_seen = rec["first_seen"].isoformat() if rec["first_seen"] else None
        last_seen = rec["last_seen"].isoformat() if rec["last_seen"] else None

        entry = {
            "address": rec["address"],
            "domain": rec["domain"],
            "message_count": rec["message_count"],
            "first_seen": first_seen,
            "last_seen": last_seen,
            "auth_spf_verdicts_seen": sorted(rec["auth_spf_seen"]) or ["unknown"],
            "auth_dkim_verdicts_seen": sorted(rec["auth_dkim_seen"]) or ["unknown"],
            "auth_dmarc_verdicts_seen": sorted(rec["auth_dmarc_seen"]) or ["unknown"],
            "reply_to_mismatch_count": rec["reply_to_mismatch_count"],
            "precedence_bulk_count": rec["precedence_bulk_count"],
            "list_unsubscribe_present_count": rec["list_unsubscribe_present_count"],
            "noreply_address_count": rec["noreply_address_count"],
            "user_ever_sent_to_this_address": rec["user_replied_to_this_sender"],
            "subjects_sample": rec["subjects_sample"],
        }

        # Simple, transparent heuristic — NOT a trust determination.
        # Surfaces a starting bucket for human/downstream review only.
        no_reply_ratio = rec["noreply_address_count"] / rec["message_count"] if rec["message_count"] else 0
        bulk_ratio = rec["precedence_bulk_count"] / rec["message_count"] if rec["message_count"] else 0

        if rec["user_replied_to_this_sender"]:
            entry["migration_candidate_bucket"] = "notify (bidirectional engagement confirmed)"
        elif no_reply_ratio > 0.5 or bulk_ratio > 0.5:
            entry["migration_candidate_bucket"] = "hold (one-way/bulk pattern — review before notifying)"
        else:
            entry["migration_candidate_bucket"] = "review (no strong signal either way)"

        report.append(entry)

    report.sort(key=lambda x: x["message_count"], reverse=True)
    return report


def write_json(report, path):
    with open(path, "w") as f:
        json.dump(report, f, indent=2, default=str)


def write_csv(report, path):
    if not report:
        return
    fieldnames = [
        "address", "domain", "message_count", "first_seen", "last_seen",
        "auth_spf_verdicts_seen", "auth_dkim_verdicts_seen", "auth_dmarc_verdicts_seen",
        "reply_to_mismatch_count", "precedence_bulk_count", "list_unsubscribe_present_count",
        "noreply_address_count", "user_ever_sent_to_this_address", "migration_candidate_bucket",
    ]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in report:
            row = dict(row)
            for key in ("auth_spf_verdicts_seen", "auth_dkim_verdicts_seen", "auth_dmarc_verdicts_seen"):
                row[key] = ";".join(row[key])
            writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description="Analyze exported mbox mailboxes for pre-migration TrustedSender gating.")
    parser.add_argument("mbox_files", nargs="+", help="One or more mbox files to analyze")
    parser.add_argument("--out", default="sender_report.json", help="JSON output path")
    parser.add_argument("--csv", default=None, help="Optional CSV output path")
    args = parser.parse_args()

    senders, total_messages, unparsed = analyze_mbox(args.mbox_files)
    report = build_report(senders)

    write_json(report, args.out)
    if args.csv:
        write_csv(report, args.csv)

    print(f"Processed {total_messages} messages, {unparsed} had no parseable From address.")
    print(f"Unique senders: {len(report)}")
    print(f"Report written to {args.out}" + (f" and {args.csv}" if args.csv else ""))


if __name__ == "__main__":
    main()
