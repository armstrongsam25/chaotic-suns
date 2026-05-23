#!/usr/bin/env python3
"""Send beta test invitation email via Gmail SMTP.

You'll need a Gmail App Password (not your regular password).
Generate one at: https://myaccount.google.com/apppasswords

Usage:
    python3 send_beta_email.py
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# ── Configuration ───────────────────────────────────────────
FROM_EMAIL = "armstrongsam25@gmail.com"
FROM_NAME = "Sam Armstrong"
TO_EMAIL = "armstrongsam25@gmail.com"
TO_NAME = "Sam"

# Get app password (DON'T commit this to git)
APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
if not APP_PASSWORD:
    pw_file = Path(__file__).parent / ".gmail-app-password"
    if pw_file.exists():
        APP_PASSWORD = pw_file.read_text().strip()
if not APP_PASSWORD:
    print("ERROR: Set GMAIL_APP_PASSWORD environment variable or create .gmail-app-password file")
    print("Generate an App Password at: https://myaccount.google.com/apppasswords")
    exit(1)

# ── Read email template ─────────────────────────────────────
template_path = Path(__file__).parent / "dist" / "beta_cold_email.txt"
with open(template_path) as f:
    raw = f.read()

# Split subject and body
lines = raw.strip().split("\n")
subject = lines[0].replace("Subject: ", "")
body = "\n".join(lines[2:])  # Skip subject + blank line

# Personalize
body = body.replace("Hi Sam,", f"Hi {TO_NAME},")
body = body.replace("— Sam", f"— {FROM_NAME}")

# ── Build email ─────────────────────────────────────────────
msg = MIMEMultipart()
msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
msg["To"] = TO_EMAIL
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

# ── Send ────────────────────────────────────────────────────
print(f"From: {FROM_EMAIL}")
print(f"To: {TO_EMAIL}")
print(f"Subject: {subject}")
print()
print("Connecting to Gmail SMTP...")

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(FROM_EMAIL, APP_PASSWORD)
        server.send_message(msg)
    print("✓ Email sent successfully!")
except smtplib.SMTPAuthenticationError:
    print("✗ Authentication failed. Check your App Password.")
    print("  Generate one at: https://myaccount.google.com/apppasswords")
    exit(1)
except Exception as e:
    print(f"✗ Failed: {e}")
    exit(1)