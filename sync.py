import os
import hashlib
import time
import random
import string
from pathlib import Path

import requests
from bs4 import BeautifulSoup


# ==============================
# Configuration
# ==============================

HANDLE = os.environ["CF_HANDLE"]
API_KEY = os.environ["CF_API_KEY"]
API_SECRET = os.environ["CF_API_SECRET"]

OUTPUT_DIR = Path("solutions")
OUTPUT_DIR.mkdir(exist_ok=True)

BASE_URL = "https://codeforces.com"


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
        f"{BASE_URL}/api/user.status",
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
# Get source code from submission
# page
# ==============================

def get_source_code(submission):

    contest_id = submission.get("contestId")
    submission_id = submission.get("id")

    if not contest_id or not submission_id:
        print(
            f"Skipping submission {submission_id}: "
            "missing contest ID"
        )
        return None

    url = (
        f"{BASE_URL}/contest/"
        f"{contest_id}/submission/"
        f"{submission_id}"
    )

    print(f"Fetching source: {url}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/131.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

    except requests.RequestException as e:
        print(
            f"Could not fetch submission "
            f"{submission_id}: {e}"
        )
        return None

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    source_element = soup.select_one(
        "pre#program-source-text"
    )

    if source_element is None:
        print(
            f"Source code not found for "
            f"submission {submission_id}"
        )
        return None

    source_code = source_element.get_text()

    if not source_code.strip():
        print(
            f"Source code is empty for "
            f"submission {submission_id}"
        )
        return None

    return source_code


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

    if language == "c":
        return ".c"

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

    print(
        f"Checking Codeforces submissions "
        f"for {HANDLE}..."
    )

    submissions = get_submissions()

    print(
        f"Total submissions found: "
        f"{len(submissions)}"
    )

    accepted = [
        s for s in submissions
        if s.get("verdict") == "OK"
    ]

    print(
        f"Accepted submissions found: "
        f"{len(accepted)}"
    )

    added = 0

    for submission in accepted:

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

        extension = get_extension(
            language
        )

        filename = (
            f"{contest_id}_"
            f"{problem_index}_"
            f"{problem_name}"
            f"{extension}"
        )

        file_path = OUTPUT_DIR / filename

        if file_path.exists():
            print(
                f"Already exists: {file_path}"
            )
            continue

        # Try API source first
        source_code = submission.get(
            "sourceCode"
        )

        # If API didn't provide source,
        # fetch it from the submission page.
        if not source_code:
            source_code = get_source_code(
                submission
            )

        if not source_code:
            print(
                f"Could not get source for "
                f"submission {submission.get('id')}"
            )
            continue

        file_path.write_text(
            source_code,
            encoding="utf-8"
        )

        print(
            f"Added: {file_path}"
        )

        added += 1

        # Avoid sending requests too quickly.
        time.sleep(2)

    print(
        f"Finished. Added "
        f"{added} new solution(s)."
    )


if __name__ == "__main__":
    main()
