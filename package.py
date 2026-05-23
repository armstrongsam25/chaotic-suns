#!/usr/bin/env python3
"""Create a distributable beta package of Chaotic Suns."""

import os
import sys
import shutil
import zipfile
from pathlib import Path

VERSION = "0.2.0-beta"

# What to include
INCLUDE = [
    "main.py",
    "test_all.py",
    "capture.py",
    "requirements.txt",
    "src/",
]

# What to exclude from src/
EXCLUDE = ["__pycache__", "*.pyc", ".git", ".gitignore"]

# Build output
BUILD_DIR = Path(f"dist/ChaoticSuns_{VERSION}")
ZIP_NAME = f"ChaoticSuns_{VERSION}_linux.zip"

def should_exclude(path):
    for pattern in EXCLUDE:
        if pattern in str(path):
            return True
    return False

def create_package():
    print(f"Building Chaotic Suns v{VERSION} package...")
    
    # Clean
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True)
    
    # Copy files
    root = Path(".")
    for item in INCLUDE:
        src = root / item
        dst = BUILD_DIR / item
        if src.is_file():
            shutil.copy2(src, dst)
            print(f"  Copied: {item}")
        elif src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
            for f in src.rglob("*"):
                if not should_exclude(f):
                    rel = f.relative_to(root)
                    target = BUILD_DIR / rel
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if f.is_file():
                        shutil.copy2(f, target)
            print(f"  Copied dir: {item}/")
    
    # Create README
    readme = """Chaotic Suns - Beta v{version}
====================================

A cosmic survival game where you guide a civilization
orbiting multiple chaotic suns.

REQUIREMENTS:
  - Python 3.12+
  - pip install -r requirements.txt

TO RUN:
  python3 main.py

TO TEST:
  python3 test_all.py

CONTROLS:
  Space       Pause/Resume
  E           Prediction Mode
  H           Help
  T           Research Lab (tech tree)
  1-4         Launch probes
  Arrows      Pan view
  +/-         Zoom
  F5/F9       Quick save/load
  Esc         Menu

FEEDBACK:
  Please report bugs and suggestions!

Built: {version}
""".format(version=VERSION)
    
    with open(BUILD_DIR / "README.txt", "w") as f:
        f.write(readme)
    
    # Create launch script
    launch = """#!/bin/bash
# Chaotic Suns Launcher
cd "$(dirname "$0")"
echo "Setting up virtual environment..."
python3 -m venv venv 2>/dev/null
source venv/bin/activate
pip install -q -r requirements.txt
echo "Launching Chaotic Suns..."
python3 main.py
"""
    with open(BUILD_DIR / "launch.sh", "w") as f:
        f.write(launch)
    os.chmod(BUILD_DIR / "launch.sh", 0o755)
    
    # Create zip
    zip_path = Path(f"dist/{ZIP_NAME}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in BUILD_DIR.rglob("*"):
            if f.is_file():
                arcname = f.relative_to(BUILD_DIR.parent)
                zf.write(f, arcname)
    
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"\nPackage created: {zip_path}")
    print(f"Size: {size_mb:.1f} MB")
    print(f"Contents: {BUILD_DIR}")
    
    # Also create a tarball for Linux users who prefer it
    import tarfile
    tar_path = Path(f"dist/ChaoticSuns_{VERSION}_linux.tar.gz")
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(BUILD_DIR, arcname=f"ChaoticSuns_{VERSION}")
    tar_size = tar_path.stat().st_size / (1024 * 1024)
    print(f"Also: {tar_path} ({tar_size:.1f} MB)")
    
    return zip_path

if __name__ == "__main__":
    create_package()
    print("\nReady for distribution!")