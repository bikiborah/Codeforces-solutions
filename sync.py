import os
import hashlib
import time
import random
import string
from pathlib import Path

import requests


# -----------------------------
# Configuration
# -----------------------------

HANDLE = os.environ["CF_HANDLE"]
API_KEY = os.environ["CF_API_KEY"]
API_SECRET = os.environ["CF_API_SECRET"]

OUTPUT_DIR = Path("solutions")
OUTPUT_DIR.mkdir(exist_ok=True)


# -----------------------------
# Codeforces API
# -----------------------------

def get_api_signature(method, params):
    """
    Creates the signature required by the Codeforces API.
    """

    rand = "".join(
        random.choices(
            string.ascii_lowercase + string.digits,
            k=6
        )
    )

    sorted_params = sorted(params.items())

    query = "&".join(
        f"{key}={value}"
        for key, value in sorted_params
    )

    signature_base = (
        f"{rand}/{method}?{query}#{API_SECRET}"
    )

    signature = hashlib.sha512(
        signature_base.encode("utf-8")
    ).hexdigest()

    return rand + signature


def get_submissions():
    """
    Gets the user's recent Codeforces submissions.
    """

    method = "user.status"

    params = {
        "apiKey": API_KEY,
        "handle": HANDLE,
        "includeSources": "true",
        "time": int(time.time()),
        "count": 1000,
    }

    params["apiSig"] = get_api_signature(
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


# -----------------------------
# File helpers
# -----------------------------

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


def clean_name(text):
    """
    Makes a safe filename.
    """

    allowed = (
        string.ascii_letters
        + string.digits
        + "_-"
    )

    return "".join(
        character if character in allowed else "_"
        for character in text
    )


# -----------------------------
# Save solutions
# -----------------------------

def save_submission(submission):
    """
    Saves an accepted submission if it
    hasn't already been saved.
    """

    if submission.get("verdict") != "OK":
        return False

    source = submission.get("sourceCode")

    if not source:
        return False

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

    # Don't replace an existing solution.
    if file_path.exists():
        return False

    file_path.write_text(
        source,
        encoding="utf-8"
    )

    print(f"Added: {file_path}")

    return True


# -----------------------------
# Main program
# -----------------------------

def main():

    print(
        f"Checking Codeforces submissions "
        f"for {HANDLE}..."
    )

    submissions = get_submissions()

    added = 0

    for submission in submissions:

        if save_submission(submission):
            added += 1

    print(
        f"Finished. Added {added} new solution(s)."
    )


if __name__ == "__main__":
    main()
