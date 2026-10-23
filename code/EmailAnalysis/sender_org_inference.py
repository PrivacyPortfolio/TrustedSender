"""
sender_org_inference.py

Given a sender_report.csv (from mbox_sender_analysis.py), produces a
suggested organization name and an "is this domain the actual
organization, or just an intermediary/ESP relaying on their behalf"
guess for each sender — meant to speed up the manual review you were
already doing, not replace it. Every row is a SUGGESTION with a
confidence flag, not a final answer.

METHOD (transparent, editable — this is not a black box):
  1. Strip known infrastructure/tracking subdomain prefixes (e.g.
     "email.", "engage.", "px.", "notifications.") to get closer to the
     core domain.
  2. Check the resulting root domain against a curated list of KNOWN
     INTERMEDIARY domains (ATS platforms, ESPs, marketing/notification
     vendors) — companies whose domain shows up as a sender, but who are
     relaying on behalf of someone else, not the organization you
     actually have a relationship with.
  3. If not a known intermediary, extract the domain's core token
     (the part before the TLD, with common corporate suffixes like
     "inc"/"group"/"llc" stripped) as the organization name guess.
  4. If IS a known intermediary, look for an organization-identifying
     token elsewhere — usually a subdomain prefix (e.g.
     "acmecorp.wd5.myworkday.com" -> "acmecorp") — since ATS/HR platforms
     commonly put the client organization's name in a subdomain.

BOTH LISTS BELOW ARE STARTER SETS BASED ON WHAT SHOWED UP IN YOUR OWN
REPORT — extend them as you find more. This is meant to be edited by you
over time, not treated as complete or authoritative out of the box.

USAGE:
    python sender_org_inference.py report.csv --out report_with_org.csv
"""

import argparse
import csv
import re


# Domains that are relaying/hosting on behalf of a SPECIFIC OTHER
# organization, where that organization's name is typically findable in
# a subdomain prefix (e.g. "acmecorp.wd5.myworkday.com" -> "acmecorp").
# Extend as you find more ATS/HR platforms with this pattern.
SUBDOMAIN_CARRIES_ORG_NAME = {
    "myworkday.com", "wd5.myworkday.com",
    "teamtailor-mail.com", "comeet-notifications.com",
}

# Domains that ARE a recognizable organization/platform in their own
# right, but which also commonly relay content on behalf of third
# parties (e.g. Indeed sends its own account emails AND relays job
# postings from individual employers — headers alone can't reliably
# tell you which). Org guess falls back to the platform's own name;
# the note flags the ambiguity for manual review rather than guessing
# wrong silently.
KNOWN_DUAL_ROLE_PLATFORMS = {
    "indeed.com": "Indeed",
    "jobalert.indeed.com": "Indeed",
    "linkedin.com": "LinkedIn",
    "e.linkedin.com": "LinkedIn",
    "cs.linkedin.com": "LinkedIn",
    "engage.microsoft.com": "Microsoft",
    "promomail.microsoft.com": "Microsoft",
}

# Pure infrastructure/relay domains with no organization identity of
# their own worth surfacing — always low confidence, no subdomain logic.
PURE_INFRASTRUCTURE_DOMAINS = {
    "amazonses.com", "sendgrid.net", "mailgun.org", "postmarkapp.com",
    "sparkpostmail.com", "mandrillapp.com", "sendinblue.com",
    "klaviyomail.com", "mcsv.net", "bounces.amazon.com",
    "greenhouse.io", "lever.co", "icims.com", "jobvite.com",
    "bamboohr.com", "careerplug.com", "fountain.com", "smartrecruiters.com",
    "px.innovaccerinc.com",
}

KNOWN_INTERMEDIARY_DOMAINS = SUBDOMAIN_CARRIES_ORG_NAME | set(KNOWN_DUAL_ROLE_PLATFORMS) | PURE_INFRASTRUCTURE_DOMAINS

# Subdomain prefixes that are infrastructure/purpose labels, not part of
# an organization's identity — stripped before attempting to extract an
# org name token.
NOISE_SUBDOMAIN_PREFIXES = {
    "email", "mail", "e", "engage", "px", "app", "careers", "jobs", "hr",
    "notifications", "notify", "news", "support", "cs", "no-reply",
    "noreply", "donotreply", "do-notreply", "alert", "alerts",
    "account", "accounts", "security", "login", "register", "registrar",
    "bounces", "postmaster", "info", "updates", "digest",
}

CORPORATE_SUFFIXES_TO_STRIP = {
    "inc", "incorporated", "llc", "ltd", "limited", "corp", "corporation",
    "group", "co", "company", "holdings", "global", "worldwide",
}


def strip_noise_prefixes(domain_parts: list) -> list:
    """Remove leading subdomain labels that are known noise (email.,
    notifications., etc.), stopping at the first label that isn't noise."""
    result = list(domain_parts)
    while len(result) > 2 and result[0].lower() in NOISE_SUBDOMAIN_PREFIXES:
        result = result[1:]
    return result


def registrable_domain(full_domain: str) -> str:
    """Best-effort extraction of the 'core' domain (SLD + TLD), without
    an external public-suffix-list dependency. Handles the common
    two-part TLD cases seen in practice (co.uk, com.au) with a small
    hardcoded list; not exhaustive for every ccTLD, but covers the
    overwhelming majority of business email domains."""
    parts = full_domain.lower().split(".")
    two_part_tlds = {"co.uk", "com.au", "co.jp", "com.br", "co.nz", "com.mx"}
    if len(parts) >= 3 and ".".join(parts[-2:]) in two_part_tlds:
        return ".".join(parts[-3:])
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return full_domain


def guess_org_name(core_token: str) -> str:
    """Clean up a domain's core token into a readable org name guess:
    strip common corporate suffixes, title-case it."""
    token = core_token
    for suffix in CORPORATE_SUFFIXES_TO_STRIP:
        if token.endswith(suffix) and len(token) > len(suffix) + 2:
            token = token[: -len(suffix)]
    return token.strip("-_").title() if token else core_token.title()


def infer_organization(domain: str):
    """Returns (org_name_guess, is_likely_intermediary, confidence, note)."""
    domain = domain.lower().strip()
    root = registrable_domain(domain)

    if domain in KNOWN_DUAL_ROLE_PLATFORMS or root in KNOWN_DUAL_ROLE_PLATFORMS:
        platform_name = KNOWN_DUAL_ROLE_PLATFORMS.get(domain) or KNOWN_DUAL_ROLE_PLATFORMS.get(root)
        return (
            platform_name,
            True,
            "medium",
            f"{platform_name} is both a real organization AND relays mail on behalf of "
            f"third parties (e.g. employers posting jobs) — verify which applies here.",
        )

    if domain in SUBDOMAIN_CARRIES_ORG_NAME or root in SUBDOMAIN_CARRIES_ORG_NAME:
        parts = domain.split(".")
        if len(parts) > 2:
            prefix_candidate = parts[0]
            if prefix_candidate.lower() not in NOISE_SUBDOMAIN_PREFIXES:
                return (
                    guess_org_name(prefix_candidate),
                    True,
                    "medium",
                    f"Known ATS/platform domain ({root}); org guess taken from subdomain prefix '{prefix_candidate}' — verify manually.",
                )
        return (
            None,
            True,
            "low",
            f"Known ATS/platform domain ({root}); no org-identifying subdomain token found.",
        )

    if domain in PURE_INFRASTRUCTURE_DOMAINS or root in PURE_INFRASTRUCTURE_DOMAINS:
        return (
            None,
            True,
            "low",
            f"Pure infrastructure/relay domain ({root}) — no organization identity of its own.",
        )

    # Not a known intermediary — treat root domain's core token as the
    # organization name candidate.
    root_parts = root.split(".")
    core_token = root_parts[0] if root_parts else root
    return (
        guess_org_name(core_token),
        False,
        "medium",
        f"Domain not in known-intermediary list; treating '{core_token}' as the likely organization name — verify manually, especially for uncommon TLDs.",
    )


def main():
    parser = argparse.ArgumentParser(description="Add organization-guess columns to a sender_report.csv")
    parser.add_argument("report_csv", help="Path to sender_report.csv from mbox_sender_analysis.py")
    parser.add_argument("--out", default="report_with_org.csv", help="Output CSV path")
    args = parser.parse_args()

    with open(args.report_csv, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames + ["org_guess", "is_likely_intermediary", "org_guess_confidence", "org_guess_note"]

    for row in rows:
        org_guess, is_intermediary, confidence, note = infer_organization(row.get("domain", ""))
        row["org_guess"] = org_guess or ""
        row["is_likely_intermediary"] = is_intermediary
        row["org_guess_confidence"] = confidence
        row["org_guess_note"] = note

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows with organization guesses to {args.out}")
    print("Every row is a SUGGESTION for manual review — not a final answer.")
    print("Extend KNOWN_INTERMEDIARY_DOMAINS and NOISE_SUBDOMAIN_PREFIXES in this script as you find gaps.")


if __name__ == "__main__":
    main()
