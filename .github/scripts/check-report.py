# Copyright 2026 Vivian Voss. Code by Vivian Voss. Licensed under the Tinkerbox Licence 1.0.
# SPDX-License-Identifier: LicenseRef-Tinkerbox-1.0
# Scope: Recompute the report key of a beta report and close the report when it is missing, wrong for its text or older than seven days ({K0198}).
import datetime
import hashlib
import hmac
import os
import re
import subprocess

KEY = re.compile(r"^Report key: TB1-([0-9a-f]+)-([0-9a-f]{16})\s*$", re.MULTILINE)
WEEK = 7 * 24 * 3600
REFUSAL = (
    "Diese Meldung trägt keinen gültigen Meldeschlüssel und wird geschlossen. "
    "Bitte melde direkt aus Tinkerbox: Einstellungen → Debug-Log → »Fehler melden«, oder füge das dort kopierte Log unverändert ein.\n\n"
    "This report carries no valid report key and is closed. "
    "Please report from Tinkerbox itself: »Einstellungen« → »Debug-Log« → »Fehler melden«, or paste the log copied there unchanged."
)


def read_log(body):
    section = re.search(r"### Debug-Log\s*\n(.*?)(?=\n### |\Z)", body, re.DOTALL)
    if not section:
        return ""
    text = section.group(1).strip()
    fenced = re.match(r"^```[a-z]*\n(.*?)\n```$", text, re.DOTALL)
    return fenced.group(1) if fenced else text


def parse_report_text(text):
    lines = [line.rstrip("\r") for line in text.split("\n")]
    return "\n".join(line for line in lines if not line.startswith("Report key: ")).strip()


def check_report(body, created, secret):
    log = read_log(body)
    found = KEY.search(log)
    if not found or not secret:
        return False
    stamp, tag = found.group(1), found.group(2)
    signed = hmac.new(secret.encode(), (stamp + "\n" + parse_report_text(log)).encode(), hashlib.sha256).hexdigest()[:16]
    age = created.timestamp() - int(stamp, 16)
    return hmac.compare_digest(signed, tag) and -3600 <= age <= WEEK


def write_refusal(repository, number):
    subprocess.run(["gh", "issue", "comment", number, "-R", repository, "-b", REFUSAL], check=True)
    subprocess.run(["gh", "issue", "close", number, "-R", repository, "--reason", "not planned"], check=True)


created = datetime.datetime.fromisoformat(os.environ["ISSUE_CREATED"].replace("Z", "+00:00"))
valid = check_report(os.environ.get("ISSUE_BODY", ""), created, os.environ.get("REPORT_SECRET", ""))
print("report key valid" if valid else "report key missing or invalid")
if not valid and os.environ.get("ISSUE_STATE") == "open":
    write_refusal(os.environ["REPOSITORY"], os.environ["ISSUE_NUMBER"])
