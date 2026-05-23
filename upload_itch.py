#!/usr/bin/env python3
"""Upload a new build of Chaotic Suns to itch.io via butler.

Requires:
    - butler CLI installed (from itch.io)
    - ITCH_API_KEY environment variable or .itch-api-key file
    - Your itch.io project already created at: https://itch.io/create

Usage:
    # Set your API key (from https://itch.io/user/settings/api-keys)
    export ITCH_API_KEY=your-key-here
    python3 upload_itch.py

    # Or create a .itch-api-key file in the repo root
    echo "your-key-here" > .itch-api-key
    python3 upload_itch.py
"""

import os
import sys
import subprocess
from pathlib import Path

# ── Configuration ───────────────────────────────────────────
ITCH_USER = "armstrongsam25"        # ← CHANGE THIS
ITCH_GAME = "chaotic-suns"              # Your itch.io project slug
VERSION = "0.2.0-beta"
CHANNEL = "linux-beta"

# Find the game directory
GAME_DIR = Path(__file__).parent  # Root of the repo
DIST_DIR = GAME_DIR / "dist" / f"ChaoticSuns_{VERSION}"

# ── API Key ─────────────────────────────────────────────────
api_key = os.environ.get("ITCH_API_KEY")
if not api_key:
    key_file = GAME_DIR / ".itch-api-key"
    if key_file.exists():
        api_key = key_file.read_text().strip()
if not api_key:
    print("ERROR: No ITCH_API_KEY found.")
    print("  Set via: export ITCH_API_KEY=your-key")
    print("  Or create: .itch-api-key file in repo root")
    print("  Get your key: https://itch.io/user/settings/api-keys")
    sys.exit(1)

# ── Verify butler exists ────────────────────────────────────
butler = "butler"
try:
    subprocess.run([butler, "--version"], capture_output=True, check=True)
except (subprocess.CalledProcessError, FileNotFoundError):
    # Try local path
    for p in [Path.home() / ".local/bin/butler", Path.home() / "bin/butler"]:
        if p.exists():
            butler = str(p)
            break
    else:
        print("ERROR: butler not found. Install from: https://itch.io/docs/butler/installing.html")
        sys.exit(1)

# ── Build the package if needed ─────────────────────────────
if not DIST_DIR.exists():
    print(f"Building package...")
    subprocess.run([sys.executable, str(GAME_DIR / "package.py")], cwd=str(GAME_DIR))

if not DIST_DIR.exists():
    print(f"ERROR: Build directory not found: {DIST_DIR}")
    sys.exit(1)

# ── Upload ─────────────────────────────────────────────────
target = f"{ITCH_USER}/{ITCH_GAME}:{CHANNEL}"
print(f"Uploading to: {target}")
print(f"From: {DIST_DIR}")
print()

cmd = [butler, "push", str(DIST_DIR), target, f"--userversion={VERSION}"]
print(f"Running: {' '.join(cmd)}")
print()

env = os.environ.copy()
env["BUTLER_API_KEY"] = api_key

result = subprocess.run(cmd, cwd=str(GAME_DIR), env=env)
if result.returncode == 0:
    print(f"\n✓ Uploaded successfully!")
    print(f"  View at: https://{ITCH_USER}.itch.io/{ITCH_GAME}")
else:
    print(f"\n✗ Upload failed with code {result.returncode}")
    sys.exit(result.returncode)