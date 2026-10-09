import subprocess
from pathlib import Path
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI


class VersionReleaseNotes(BaseModel):
    """Structured release documentation for a polarity-engine version milestone."""

    version_title: str = Field(
        description="e.g. Version 1.0: Core Physics & Topology Baseline"
    )
    executive_summary: str = Field(
        description="2-3 sentence overview of what this milestone achieves"
    )
    new_features: list[str] = Field(
        description="High-level capabilities added to the engine"
    )
    refactors_and_optimizations: list[str] = Field(
        description="Performance or code quality improvements"
    )
    breaking_changes: list[str] = Field(
        description="API or schema handshake changes", default=[]
    )


def generate_release_notes(
    repo_path: Path, from_ref: str = "HEAD~20", to_ref: str = "HEAD"
) -> VersionReleaseNotes:
    """Parses raw git commits between two references and synthesizes a structured changelog."""

    # 1. Extract raw git commit messages from the target repo path
    cmd = [
        "git",
        "-C",
        str(repo_path),
        "log",
        f"{from_ref}..{to_ref}",
        "--pretty=format:%s",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    raw_commits = result.stdout.strip()

    if not raw_commits:
        raise ValueError(f"No git commits found between {from_ref} and {to_ref}")

    # 2. Use Instructor to summarize granular commits into structured release notes
    client = instructor.from_openai(OpenAI())

    release_notes = client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=VersionReleaseNotes,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a lead software architect writing public release notes for a "
                    "production-grade computational biophysics engine (polarity-engine). "
                    "Group granular commits into clear, professional scientific capabilities."
                ),
            },
            {
                "role": "user",
                "content": f"Synthesize these raw git commits into release notes:\n{raw_commits}",
            },
        ],
    )
    return release_notes
