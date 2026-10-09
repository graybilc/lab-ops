from pathlib import Path
from lab_ops.adapters.base import BaseRepoAdapter


class MechanicsSandboxAdapter(BaseRepoAdapter):
    """Adapter specifically tailored for aPKC-mechanics-analysis sandbox repo."""

    def get_benchmark_files(self) -> list[Path]:
        benchmark_dir = self.repo_path / self.config.benchmark_dir
        if not benchmark_dir.exists():
            return []
        # Finds all JSON benchmark run files in your sandbox
        return list(benchmark_dir.glob("*.json"))

    def get_source_files(self) -> list[Path]:
        # Finds exploratory notebooks and scripts
        return list((self.repo_path / "notebooks").glob("*.ipynb"))
