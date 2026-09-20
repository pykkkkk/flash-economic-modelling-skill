#!/usr/bin/env python3
"""Self-update helper for the econ-modeling-flash skill.

Subcommands:
  check   Compare the local VERSION against the latest GitHub Release tag.
  update  Download the latest Release tarball, back up the current skill, and sync.

Source of truth for updates: the GitHub Release tags of the repo below.
This script uses only the Python standard library (no third-party dependencies),
so it runs in the same managed Python environment as the rest of the skill.

NOTE: after `update`, restart the session for the new code to take effect.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

# ---- configuration -------------------------------------------------------
REPO_URL = "https://github.com/pykkkkk/flash-economic-modelling-skill"
UA = {"User-Agent": "econ-modeling-flash-updater"}

SKILL_DIR = Path(__file__).resolve().parent.parent  # scripts/ -> skill root
VERSION_FILE = SKILL_DIR / "VERSION"
BACKUP_ROOT = SKILL_DIR.parent / "_backups"          # outside the skill dir


# ---- helpers -------------------------------------------------------------
def parse_repo(url: str) -> str:
    """Accept 'https://github.com/owner/repo' or 'owner/repo'."""
    url = url.rstrip("/")
    if url.startswith("https://github.com/"):
        url = url[len("https://github.com/"):]
    return url.strip("/")


def get_local_version() -> str:
    try:
        return VERSION_FILE.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return "0.0.0"


def parse_semver(v: str):
    v = v.lstrip("vV")
    parts = []
    for p in v.split(".")[:3]:
        try:
            parts.append(int(p))
        except ValueError:
            parts.append(0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)


def latest_release(repo: str):
    """Return (tag_name, tarball_url).

    Special return values:
      (None, None)   -> no releases exist yet (HTTP 404)
      ("ERROR", None) -> API rejected the request (e.g. rate limited)
      ("NETERR", None) -> network failure
    """
    api = f"https://api.github.com/repos/{repo}/releases/latest"
    req = urllib.request.Request(api, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode("utf-8"))
        return data.get("tag_name"), data.get("tarball_url")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, None
        return "ERROR", None
    except Exception:
        return "NETERR", None


# ---- subcommands ---------------------------------------------------------
def cmd_check(_args) -> int:
    local = get_local_version()
    repo = parse_repo(REPO_URL)
    tag, _ = latest_release(repo)
    if tag is None:
        print(f"[check] local version v{local}")
        print(f"[check] No GitHub Release found yet. Create a 'v{local}' "
              f"Release on the repo to enable auto-update.")
        return 0
    if tag == "ERROR":
        print("[check] GitHub API rejected the request (rate limited or blocked). "
              "Retry later.")
        return 1
    if tag == "NETERR":
        print("[check] Network connection failed. Check connectivity and retry.")
        return 1
    remote = tag.lstrip("vV")
    if parse_semver(remote) > parse_semver(local):
        print(f"[check] local v{local} -> remote v{remote}: update available.")
        print("        Run: python scripts/update_skill.py update")
    else:
        print(f"[check] Up to date (local v{local}, remote v{remote}).")
    return 0


def cmd_update(_args) -> int:
    local = get_local_version()
    repo = parse_repo(REPO_URL)
    tag, tarball = latest_release(repo)
    if tag is None:
        print("[update] No GitHub Release exists yet. Create one before updating.")
        return 1
    if tag in ("ERROR", "NETERR") or not tarball:
        print("[update] Could not fetch a usable Release. Aborting (no files changed).")
        return 1

    # 1) back up the current skill (outside the skill dir, safe from the sync)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = BACKUP_ROOT / f"econ-modeling-flash_{ts}"
    backup_dir.parent.mkdir(parents=True, exist_ok=True)
    print(f"[update] Backing up current skill -> {backup_dir}")
    shutil.copytree(SKILL_DIR, backup_dir)

    # 2) download the release tarball
    print(f"[update] Downloading {tag} ...")
    req = urllib.request.Request(tarball, headers=UA)
    with tempfile.TemporaryDirectory() as td:
        td_p = Path(td)
        tar_path = td_p / "release.tar.gz"
        try:
            with urllib.request.urlopen(req, timeout=60) as r, open(tar_path, "wb") as f:
                shutil.copyfileobj(r, f)
        except Exception as e:
            print(f"[update] Download failed: {e}. No files changed; backup preserved.")
            return 1
        with tarfile.open(tar_path) as tf:
            tf.extractall(td_p)
        # GitHub tarballs nest content under '<repo>-<tag>/'
        inner = [p for p in td_p.iterdir() if p.is_dir() and p.name != "release.tar.gz"]
        src = inner[0] if inner else td_p

        # 3) sync: overwrite existing files, add new ones, keep local extras
        count = 0
        for item in src.rglob("*"):
            rel = item.relative_to(src)
            dest = SKILL_DIR / rel
            if item.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest)
                count += 1

    print(f"[update] Synced {count} files to v{tag.lstrip('vV')}.")
    print("[update] Restart the session to load the update.")
    print(f"[update] To roll back: restore {backup_dir}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="econ-modeling-flash self-updater")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("check", help="compare local version with the latest GitHub Release")
    sub.add_parser("update", help="download and apply the latest GitHub Release")
    args = ap.parse_args()
    if args.cmd == "check":
        return cmd_check(args)
    if args.cmd == "update":
        return cmd_update(args)
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
