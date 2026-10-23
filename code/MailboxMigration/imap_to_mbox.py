"""
imap_to_mbox.py

Cross-platform (Windows/Mac/Linux) IMAP export to mbox, using ONLY Python
standard library modules (imaplib, email, mailbox) — no fcntl dependency,
unlike getmail6/offlineimap, so this runs natively on Windows with no
extra install beyond Python itself.

READ-ONLY on the source: never deletes or modifies anything on the IMAP
server. Only fetches and writes locally.

USAGE (Windows example):
    python imap_to_mbox.py --host imap.comcast.net --port 993 ^
        --user YOUR_ADDRESS@comcast.net ^
        --out C:\\Data\\2026\\Email_archives\\Comcast\\comcast_export.mbox

    You will be prompted for your password securely (not shown on screen,
    not stored anywhere, not passed as a command-line argument where it
    could be visible in process lists or shell history).

    Add --all-folders to pull every folder, not just INBOX (recommended
    for a full archive export).
"""

import argparse
import email
import getpass
import imaplib
import mailbox
import re
import sys


FOLDER_LIST_RE = re.compile(r'^\((?P<flags>[^)]*)\)\s+"(?P<delim>[^"]*)"\s+(?P<name>.*)$')


def parse_folder_name(raw_entry: bytes) -> str:
    """Correctly parse an IMAP LIST response line to extract just the
    folder name, handling both quoted ("Sent Items") and unquoted (INBOX)
    forms. Previous naive rsplit approach incorrectly grabbed the '/'
    delimiter instead of the folder name — fixed here."""
    decoded = raw_entry.decode(errors="replace")
    match = FOLDER_LIST_RE.match(decoded)
    if not match:
        return None
    name = match.group("name").strip()
    # Strip surrounding quotes if present
    if name.startswith('"') and name.endswith('"'):
        name = name[1:-1]
    return name


def connect(host: str, port: int, user: str, password: str) -> imaplib.IMAP4_SSL:
    print(f"Connecting to {host}:{port} ...")
    conn = imaplib.IMAP4_SSL(host, port)
    conn.login(user, password)
    print("Authenticated successfully.")
    return conn


def list_folders(conn: imaplib.IMAP4_SSL):
    status, folders = conn.list()
    if status != "OK":
        return ["INBOX"]
    names = []
    for entry in folders:
        name = parse_folder_name(entry)
        if name and name not in names:
            names.append(name)
    return names or ["INBOX"]


def export_folder(conn: imaplib.IMAP4_SSL, folder: str, mbox: mailbox.mboxMessage, out_mbox: mailbox.mbox):
    status, _ = conn.select(folder, readonly=True)  # readonly=True: extra safety, never modifies flags on server
    if status != "OK":
        print(f"  Skipping folder {folder!r}: could not select (may be a non-selectable parent folder).")
        return 0

    status, data = conn.search(None, "ALL")
    if status != "OK" or not data or not data[0]:
        print(f"  {folder}: no messages.")
        return 0

    msg_ids = data[0].split()
    print(f"  {folder}: {len(msg_ids)} messages.")

    count = 0
    for msg_id in msg_ids:
        status, msg_data = conn.fetch(msg_id, "(RFC822)")
        if status != "OK" or not msg_data or msg_data[0] is None:
            print(f"    WARNING: could not fetch message {msg_id!r} in {folder}, skipping.")
            continue
        raw_bytes = msg_data[0][1]
        try:
            parsed = email.message_from_bytes(raw_bytes)
        except Exception as e:
            print(f"    WARNING: could not parse message {msg_id!r} in {folder}: {e}")
            continue

        # Tag which folder this came from, since a merged mbox otherwise
        # loses that context.
        if "X-Source-Folder" in parsed:
            del parsed["X-Source-Folder"]
        parsed["X-Source-Folder"] = folder

        out_mbox.add(parsed)
        count += 1

    return count


def main():
    parser = argparse.ArgumentParser(description="Export IMAP mailbox to local mbox file (Windows-compatible, no fcntl).")
    parser.add_argument("--host", required=True, help="IMAP host, e.g. imap.comcast.net")
    parser.add_argument("--port", type=int, default=993, help="IMAP SSL port (default 993)")
    parser.add_argument("--user", required=True, help="Full email address / username")
    parser.add_argument("--out", required=True, help="Path to output mbox file (will be created)")
    parser.add_argument("--all-folders", action="store_true", help="Export all folders, not just INBOX")
    parser.add_argument("--folder", default="INBOX", help="Single folder to export if not using --all-folders")
    args = parser.parse_args()

    password = getpass.getpass(f"Password for {args.user}: ")

    try:
        conn = connect(args.host, args.port, args.user, password)
    except imaplib.IMAP4.error as e:
        print(f"AUTHENTICATION FAILED: {e}")
        print("If 2-step verification is enabled on this account, you likely need")
        print("an app-specific password rather than your regular password.")
        sys.exit(1)
    except Exception as e:
        print(f"CONNECTION FAILED: {e}")
        print("Check host/port, and whether this account has migrated to a")
        print("different mail platform (e.g. Yahoo) with a different IMAP host.")
        sys.exit(1)

    out_mbox = mailbox.mbox(args.out)
    out_mbox.lock()  # mailbox module's own locking — pure-Python, Windows-safe,
                      # unlike fcntl-based locking in getmail/offlineimap

    total = 0
    try:
        if args.all_folders:
            folders = list_folders(conn)
            print(f"Found {len(folders)} folders: {folders}")
            for folder in folders:
                total += export_folder(conn, folder, mailbox.mboxMessage, out_mbox)
        else:
            total += export_folder(conn, args.folder, mailbox.mboxMessage, out_mbox)
    finally:
        out_mbox.flush()
        out_mbox.unlock()
        out_mbox.close()
        conn.logout()

    print(f"\nDone. {total} messages written to {args.out}")
    print("Nothing was deleted or modified on the server (read-only mode).")


if __name__ == "__main__":
    main()
