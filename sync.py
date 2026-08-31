import os
import base64
import hashlib
import time
import random
import string
from pathlib import Path

import requests


HANDLE = os.environ["CF_HANDLE"]
API_KEY = os.environ["CF_API_KEY"]
API_SECRET = os.environ["CF_API_SECRET"]

OUTPUT_DIR = Path("solutions")
OUTPUT_DIR.mkdir(exist_ok=True)


def create_signature(method, params):
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

    signature_string = (
        f"{rand}/{method}?{query}#{API_SECRET}"
    )

    hashed = hashlib.sha512(
        signature_string.encode("utf-8")
    ).hexdigest()

    return rand + hashed


def get_submissions():

    method = "user.status"

    params = {
        "apiKey": API_KEY,
        "handle": HANDLE,
        "from": "1",
        "count": "1000",
        "includeSources": "true",
        "time": str(int(time.time())),
    }

    params["apiSig"] = create_signature(
        method,
        {
            key: value
            for key, value in params.items()
            if key != "apiSig"
        }
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
            f"Codeforces API error: "
            f"{data.get('comment', data)}"
        )

    return data["result"]


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

    if language == "c":
        return ".c"

    return ".txt"


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

        submission_id = submission.get("id")

        problem = submission.get(
            "problem",
            {}
        )

        contest_id = problem.get(
            "contestId",
            submission.get("contestId", "unknown")
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
            print(
                f"Already exists: {file_path}"
            )
            continue

        # Codeforces provides source code
        # as Base64 when includeSources=true.
        source_base64 = submission.get(
            "sourceBase64"
        )

        print(
            f"Submission {submission_id}: "
            f"sourceBase64 available = "
            f"{bool(source_base64)}"
        )

        if not source_base64:
            print(
                f"No source code returned for "
                f"submission {submission_id}"
            )
            continue

        try:

            source_code = base64.b64decode(
                source_base64
            ).decode(
                "utf-8",
                errors="replace"
            )

        except Exception as e:

            print(
                f"Could not decode source for "
                f"submission {submission_id}: {e}"
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

    print(
        f"Finished. Added "
        f"{added} new solution(s)."
    )


if __name__ == "__main__":
    main()
