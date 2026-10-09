from pathlib import Path
from lab_ops.adapters.base import BaseRepoAdapter


class GenericRepoAdapter(BaseRepoAdapter):
    """Standard adapter that scans a target repository based on its RepoConfig settings."""

    def list_benchmark_files(self) -> list[Path]:
        benchmark_dir = self.repo_path / self.config.benchmark_dir
        if not benchmark_dir.exists():
            return []
        # Find all JSON benchmark files
        return sorted(list(benchmark_dir.glob("*.json")))

    def list_notebooks(self) -> list[Path]:
        notebook_dir = self.repo_path / "notebooks"
        if not notebook_dir.exists():
            # Fallback to checking root if no notebooks directory exists
            return sorted(list(self.repo_path.glob("*.ipynb")))
        return sorted(list(notebook_dir.glob("*.ipynb")))
