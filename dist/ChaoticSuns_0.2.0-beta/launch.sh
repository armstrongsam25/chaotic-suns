#!/bin/bash
# Chaotic Suns Launcher
cd "$(dirname "$0")"
echo "Setting up virtual environment..."
python3 -m venv venv 2>/dev/null
source venv/bin/activate
pip install -q -r requirements.txt
echo "Launching Chaotic Suns..."
python3 main.py
