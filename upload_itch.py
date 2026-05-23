#!/usr/bin/env python3
"""One-click upload of Chaotic Suns to itch.io via butler.

Prerequisite: Create the project page first!
    1. Go to https://itch.io/game/new
    2. Set URL slug: chaotic-suns
    3. Title: Chaotic Suns
    4. Classification: Games
    5. Kind: Downloadable
    6. Save the page (you can fill details later)

Then run this script. It reads the API key from .itch-api-key.

Usage:
    echo "YOUR_ITCH_API_KEY" > .itch-api-key
    python3 upload_itch.py
"""

import os
import sys
import subprocess
from pathlib import Path

ITCH_USER = "armstrongsam25"
ITCH_GAME = "chaotic-suns"
VERSION = "0.2.0-beta"
CHANNEL = "linux-beta"

GAME_DIR = Path(__file__).parent
DIST_DIR = GAME_DIR / "dist" / f"ChaoticSuns_{VERSION}"

# API Key
api_key = os.environ.get("BUTLER_API_KEY")
if not api_key:
    kf = GAME_DIR / ".itch-api-key"
    if kf.exists():
        api_key = kf.read_text().strip()
if not api_key:
    print("ERROR: Set BUTLER_API_KEY or create .itch-api-key")
    sys.exit(1)

# Find butler
butler = None
for p in [Path.home() / ".local/bin/butler", Path.home() / "bin/butler", "butler"]:
    try:
        subprocess.run([str(p), "--version"], capture_output=True, check=True)
        butler = str(p)
        break
    except (subprocess.CalledProcessError, FileNotFoundError):
        continue

if not butler:
    print("ERROR: butler not found. Install from https://itch.io/docs/butler/installing.html")
    sys.exit(1)

# Build package if needed
if not DIST_DIR.exists():
    subprocess.run([sys.executable, str(GAME_DIR / "package.py")], cwd=str(GAME_DIR))

# Upload
target = f"{ITCH_USER}/{ITCH_GAME}:{CHANNEL}"
print(f"Uploading to: {target}")
print(f"Version: {VERSION}")

env = os.environ.copy()
env["BUTLER_API_KEY"] = api_key
result = subprocess.run([butler, "push", str(DIST_DIR), target, f"--userversion={VERSION}"],
                        cwd=str(GAME_DIR), env=env)

if result.returncode == 0:
    print(f"\n✓ Live at: https://{ITCH_USER}.itch.io/{ITCH_GAME}")
else:
    print(f"\n✗ Failed (exit {result.returncode})")
    sys.exit(result.returncode)