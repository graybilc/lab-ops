# src/lab_ops/reporting/changelog.py
from pathlib import Path
import subprocess
import instructor
from openai import OpenAI
from lab_ops.schemas.changelog import VersionReleaseNotes


def extract_git_commits(
    repo_path: Path, from_ref: str = "HEAD~20", to_ref: str = "HEAD"
) -> str:
    """Extracts commit messages between two git references using subprocess."""
    repo_path = repo_path.expanduser().resolve()
    if not (repo_path / ".git").exists():
        raise FileNotFoundError(f"No git repository found at {repo_path}")

    cmd = [
        "git",
        "-C",
        str(repo_path),
        "log",
        f"{from_ref}..{to_ref}",
        "--pretty=format:%h - %s (%an)",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(
            f"Git error checking refs {from_ref}..{to_ref}: {result.stderr.strip()}"
        )

    raw_commits = result.stdout.strip()
    if not raw_commits:
        raise ValueError(f"No git commits found between {from_ref} and {to_ref}")

    return raw_commits


def generate_release_notes(
    repo_path: Path, from_ref: str = "HEAD~20", to_ref: str = "HEAD"
) -> VersionReleaseNotes:
    """Extracts raw git commits and synthesizes them into structured release notes via Instructor."""
    raw_commits = extract_git_commits(repo_path, from_ref=from_ref, to_ref=to_ref)

    client = instructor.from_openai(OpenAI())

    release_notes = client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=VersionReleaseNotes,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a lead software architect writing professional release notes for a "
                    "production computational biophysics engine (polarity-engine). "
                    "Group granular commits into clean scientific and software capabilities. "
                    "Ignore minor mechanical fix commits (like fixing typos or formatting) unless relevant."
                ),
            },
            {
                "role": "user",
                "content": f"Synthesize these raw git commits into release notes:\n\n{raw_commits}",
            },
        ],
    )
    return release_notes
