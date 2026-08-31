import os
import hashlib
import time
import random
import string
from pathlib import Path

import requests


# ==============================
# Configuration
# ==============================

HANDLE = os.environ["CF_HANDLE"]
API_KEY = os.environ["CF_API_KEY"]
API_SECRET = os.environ["CF_API_SECRET"]

OUTPUT_DIR = Path("solutions")
OUTPUT_DIR.mkdir(exist_ok=True)


# ==============================
# Codeforces API signature
# ==============================

def create_signature(method, params):
    rand = "".join(
        random.choices(
            string.ascii_lowercase + string.digits,
            k=6
        )
    )

    query = "&".join(
        f"{key}={value}"
        for key, value in sorted(params.items())
    )

    signature_string = (
        f"{rand}/{method}?{query}#{API_SECRET}"
    )

    hashed = hashlib.sha512(
        signature_string.encode("utf-8")
    ).hexdigest()

    return rand + hashed


# ==============================
# Get submissions
# ==============================

def get_submissions():

    method = "user.status"

    params = {
        "apiKey": API_KEY,
        "handle": HANDLE,
        "includeSources": "true",
        "time": int(time.time()),
        "from": 1,
        "count": 1000,
    }

    params["apiSig"] = create_signature(
        method,
        params
    )

    response = requests.get(
        "https://codeforces.com/api/user.status",
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if data.get("status") != "OK":
        raise RuntimeError(
            f"Codeforces API error: {data}"
        )

    return data["result"]


# ==============================
# File extension
# ==============================

def get_extension(language):

    language = language.lower()

    if "c++" in language:
        return ".cpp"

    if "python" in language:
        return ".py"

    if "java" in language:
        return ".java"

    if "kotlin" in language:
        return ".kt"

    if "javascript" in language:
        return ".js"

    if "typescript" in language:
        return ".ts"

    if "go" in language:
        return ".go"

    if "rust" in language:
        return ".rs"

    if "c#" in language:
        return ".cs"

    if "php" in language:
        return ".php"

    return ".txt"


# ==============================
# Safe filename
# ==============================

def clean_name(text):

    allowed = (
        string.ascii_letters
        + string.digits
        + "_-"
    )

    return "".join(
        c if c in allowed else "_"
        for c in text
    )


# ==============================
# Main
# ==============================

def main():

    print(f"Checking Codeforces submissions for {HANDLE}...")

    submissions = get_submissions()

    print(f"Total submissions found: {len(submissions)}")

    accepted = [
        s for s in submissions
        if s.get("verdict") == "OK"
    ]

    print(f"Accepted submissions found: {len(accepted)}")

    with_source = [
        s for s in accepted
        if s.get("sourceCode")
    ]

    print(
        f"Accepted submissions with source code: "
        f"{len(with_source)}"
    )

    added = 0

    for submission in with_source:

        problem = submission["problem"]

        contest_id = problem.get(
            "contestId",
            "unknown"
        )

        problem_index = problem.get(
            "index",
            "unknown"
        )

        problem_name = clean_name(
            problem.get(
                "name",
                "solution"
            )
        )

        language = submission.get(
            "programmingLanguage",
            "unknown"
        )

        extension = get_extension(language)

        filename = (
            f"{contest_id}_"
            f"{problem_index}_"
            f"{problem_name}"
            f"{extension}"
        )

        file_path = OUTPUT_DIR / filename

        if file_path.exists():
            continue

        file_path.write_text(
            submission["sourceCode"],
            encoding="utf-8"
        )

        print(f"Added: {file_path}")

        added += 1

    print(f"Finished. Added {added} new solution(s).")


if __name__ == "__main__":
    main()
