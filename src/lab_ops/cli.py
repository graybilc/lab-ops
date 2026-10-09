from pathlib import Path
import typer
from lab_ops.config import LabOpsConfig
from lab_ops.adapters.generic import GenericRepoAdapter

app = typer.Typer(help="lab-ops: Autonomous Scientific Intelligence OS")

CONFIG_PATH = Path("~/.lab-ops.yaml")


@app.command()
def status():
    """Inspect registered repositories and verify their paths on disk."""
    config = LabOpsConfig.load_from_yaml(CONFIG_PATH)
    typer.echo(
        f"\n🚀 lab-ops is operational! Registered projects ({len(config.repositories)}):\n"
    )

    for key, repo in config.repositories.items():
        adapter = GenericRepoAdapter(repo)
        benchmarks = adapter.list_benchmark_files()
        notebooks = adapter.list_notebooks()

        typer.secho(f"• [{key.upper()}] {repo.name}", fg=typer.colors.CYAN, bold=True)
        typer.echo(f"  Path: {repo.path}")
        typer.echo(f"  Role: {repo.type}")
        typer.echo(f"  Benchmarks Found: {len(benchmarks)}")
        typer.echo(f"  Notebooks Found: {len(notebooks)}\n")


@app.command()
def report(
    repo_key: str = typer.Option(
        ..., "--repo", "-r", help="Target repo key from config (e.g. 'mechanics')"
    )
):
    """Summarize execution metrics and benchmark results for a target repo."""
    config = LabOpsConfig.load_from_yaml(CONFIG_PATH)

    if repo_key not in config.repositories:
        typer.secho(
            f"Error: Repository '{repo_key}' not found in configuration!",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    repo_cfg = config.repositories[repo_key]
    adapter = MechanicsSandboxAdapter(repo_cfg)

    benchmarks = adapter.get_benchmark_files()
    typer.echo(f"Found {len(benchmarks)} benchmark log files in {repo_cfg.name}.")

    # Next step: Pass these benchmark files to an LLM agent for automatic summary!


if __name__ == "__main__":
    app()
