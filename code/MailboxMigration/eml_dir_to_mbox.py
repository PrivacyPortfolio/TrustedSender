"""
eml_dir_to_mbox.py

Converts a directory of individual .eml files (as produced by Proton's
official proton-mail-export-cli tool) into a single mbox file, so
mbox_sender_analysis.py can be run against it unchanged.

Proton's export structure is typically:
  <username>/
    mail_<timestamp>/
      <message-id-or-similar>.eml
      <message-id-or-similar>.json   <- metadata sidecar (labels, etc.)
      ...

This script:
  1. Recursively finds all .eml files under the given root directory.
  2. For each, looks for a same-named .json sidecar and best-effort
     extracts a label/folder name from it, if present — tries several
     common key names since the exact sidecar schema isn't something
     I have documented with certainty; falls back gracefully if the
     structure doesn't match any of them.
  3. Tags each message with X-Source-Folder (same header
     mbox_sender_analysis.py already knows how to read for sent/received
     detection) using whatever label was found, or the .eml file's
     immediate parent directory name as a fallback.
  4. Writes everything into one output mbox file.

USAGE:
    python eml_dir_to_mbox.py --root "C:\\path\\to\\username\\mail_20260816_092917" --out proton_export.mbox

If your Proton username folder contains multiple mail_<timestamp> export
runs, point --root at the specific one you want, or at the username
folder to include all of them (duplicates across repeated exports are
possible in that case — not deduplicated here).
"""

import argparse
import json
import mailbox
import os
import sys


def find_eml_files(root: str):
    for dirpath, _dirnames, filenames in os.walk(root):
        for fname in filenames:
            if fname.lower().endswith(".eml"):
                yield os.path.join(dirpath, fname)


def guess_folder_label(eml_path: str) -> str:
    """Best-effort folder/label extraction. Tries the JSON sidecar first
    (several plausible key names, since the exact schema isn't confirmed),
    falls back to the parent directory name if nothing usable is found."""
    # Proton's actual sidecar naming: <id>.eml -> <id>.metadata.json
    # (not <id>.json — confirmed from a real export directory listing)
    base = eml_path[:-4] if eml_path.lower().endswith(".eml") else os.path.splitext(eml_path)[0]
    json_path = base + ".metadata.json"
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            # Try a handful of plausible key names/shapes. Adjust this
            # list once you've seen your actual sidecar structure — see
            # the --inspect-sample flag below to print one for reference.
            for key in ("labels", "label", "folder", "folders", "labelIDs", "LabelIDs"):
                if key in meta:
                    value = meta[key]
                    if isinstance(value, list) and value:
                        return str(value[0])
                    if isinstance(value, str) and value:
                        return value
        except Exception:
            pass  # fall through to directory-based fallback

    # Fallback: immediate parent directory name
    return os.path.basename(os.path.dirname(eml_path)) or "unknown"


def convert(root: str, out_path: str, inspect_sample: bool = False):
    eml_files = list(find_eml_files(root))
    print(f"Found {len(eml_files)} .eml files under {root}")

    if not eml_files:
        print("No .eml files found — check the --root path.")
        sys.exit(1)

    if inspect_sample:
        sample_json = eml_files[0][:-4] + ".metadata.json" if eml_files[0].lower().endswith(".eml") else os.path.splitext(eml_files[0])[0] + ".metadata.json"
        if os.path.exists(sample_json):
            print(f"\nSample sidecar ({sample_json}):")
            with open(sample_json, "r", encoding="utf-8") as f:
                print(f.read()[:2000])
            print("\n(Use this to confirm/adjust the key names in guess_folder_label() if labels aren't being detected correctly.)")
        else:
            print(f"No sidecar found next to {eml_files[0]} — folder detection will use directory names only.")
        return

    out_mbox = mailbox.mbox(out_path, create=True)
    out_mbox.lock()

    count = 0
    errors = 0
    try:
        for eml_path in eml_files:
            try:
                with open(eml_path, "rb") as f:
                    raw_bytes = f.read()
                import email
                parsed = email.message_from_bytes(raw_bytes)

                folder_label = guess_folder_label(eml_path)
                if "X-Source-Folder" in parsed:
                    del parsed["X-Source-Folder"]
                parsed["X-Source-Folder"] = folder_label

                out_mbox.add(parsed)
                count += 1
                if count % 500 == 0:
                    print(f"  ...{count}/{len(eml_files)}", end="\r", flush=True)
                    out_mbox.flush()
            except Exception as e:
                errors += 1
                print(f"\n  WARNING: failed to convert {eml_path}: {e}")
    finally:
        out_mbox.flush()
        out_mbox.unlock()
        out_mbox.close()

    print(f"\nDone. {count} messages written to {out_path}, {errors} failed to convert.")


def main():
    parser = argparse.ArgumentParser(description="Convert a directory of .eml files (Proton export) into a single mbox.")
    parser.add_argument("--root", required=True, help="Root directory to search for .eml files (recursive)")
    parser.add_argument("--out", default="proton_export.mbox", help="Output mbox path")
    parser.add_argument("--inspect-sample", action="store_true",
                         help="Print the first .json sidecar found, then exit, without converting anything. "
                              "Use this first to see your actual sidecar structure if folder/label detection "
                              "isn't working as expected.")
    args = parser.parse_args()
    convert(args.root, args.out, args.inspect_sample)


if __name__ == "__main__":
    main()
