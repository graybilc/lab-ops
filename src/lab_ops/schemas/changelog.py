from pydantic import BaseModel, Field


class VersionReleaseNotes(BaseModel):
    """Structured release documentation for a polarity-engine version milestone."""

    version_title: str = Field(
        description="Version header, e.g., 'Version 0.1.0: Core Physics & mmCIF Parsing Baseline'"
    )
    executive_summary: str = Field(
        description="2-3 sentence overview of main capabilities and milestone progress"
    )
    new_features: list[str] = Field(
        description="High-level capabilities added to the engine"
    )
    refactors_and_optimizations: list[str] = Field(
        description="Performance enhancements, zero-copy optimization, or code quality updates"
    )
    breaking_changes: list[str] = Field(
        default_factory=list,
        description="API contract or schema handshake breaking changes",
    )
