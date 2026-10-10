"""Converts a plain text .yaml file into strongly-typed, validated Python objects"""

from pathlib import Path
from typing import Any
from pydantic import BaseModel, Field, DirectoryPath
import yaml

CONFIG_PATH = Path("~/.lab-ops.yaml").expanduser()


class RepoConfig(BaseModel):
    """Schema for an individual repository registered with lab-ops."""

    name: str = Field(description="Human-readable name of the project")
    path: DirectoryPath = Field(description="Absolute path to the repository root.")
    type: str = Field(
        default="sandbox", description="Project role: 'production' or 'sandbox'"
    )
    docs_path: str = Field(
        default="docs", description="Relative path where docs are kept"
    )
    benchmark_dir: str = Field(
        default="benchmarks", description="Relative path to benchmark outputs"
    )


class GlobalConfig(BaseModel):
    """Schema for global lab-ops settings."""

    output_dir: Path = Field(default=Path("~/lab_ops_reports"))
    default_llm_model: str = Field(default="gpt-4o-mini")


class LabOpsConfig(BaseModel):
    """The root configuration object aggregating all repos and global settings."""

    global_settings: GlobalConfig = Field(alias="global")
    repositories: dict[str, RepoConfig]

    @classmethod
    def load_from_yaml(cls, yaml_path: Path) -> "LabOpsConfig":
        """Loads, expands tildes (~), and validates configuration from a YAML file."""
        expanded_yaml_path = yaml_path.expanduser()

        if not expanded_yaml_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found at: {expanded_yaml_path}"
            )

        with open(expanded_yaml_path, "r") as f:
            raw_data = yaml.safe_load(f)

        # Pre-process raw dictionary to expand tildes (~) in repository paths
        if "repositories" in raw_data and isinstance(raw_data["repositories"], dict):
            for repo_key, repo_info in raw_data["repositories"].items():
                if isinstance(repo_info, dict) and "path" in repo_info:
                    # Expand ~ to full path string e.g. /Users/chiharugraybill/...
                    repo_info["path"] = str(Path(repo_info["path"]).expanduser())

        # Expand ~ in global settings output_dir if present
        if "global" in raw_data and "output_dir" in raw_data["global"]:
            raw_data["global"]["output_dir"] = str(
                Path(raw_data["global"]["output_dir"]).expanduser()
            )

        # Now Pydantic receives fully resolved absolute paths!
        return cls(**raw_data)
