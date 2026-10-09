from abc import ABC, abstractmethod
from pathlib import Path
from lab_ops.config import RepoConfig


class BaseRepoAdapter(ABC):
    """Abstract Base Class establishing the standard interface for repository adapters."""

    def __init__(self, config: RepoConfig):
        self.config = config
        self.repo_path = Path(config.path)

    @abstractmethod
    def list_benchmark_files(self) -> list[Path]:
        """Locate all benchmark JSON or log outputs in this repository."""
        pass

    @abstractmethod
    def list_notebooks(self) -> list[Path]:
        """Locate exploratory Jupyter notebooks."""
        pass
