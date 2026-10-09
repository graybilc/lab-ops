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


@app.command()
def changelog(
    repo_key: str = typer.Option(
        "polarity", "--repo", "-r", help="Target repository key"
    ),
    from_ref: str = typer.Option(
        "HEAD~15", "--from", help="Git reference start (e.g. v0.1.0 or HEAD~10)"
    ),
):
    """Generate high-level release notes from raw git commits."""
    config = LabOpsConfig.load_from_yaml(CONFIG_PATH)
    repo_cfg = config.repositories[repo_key]

    typer.echo(f"Analyzing git log for {repo_cfg.name}...")
    notes = generate_release_notes(Path(repo_cfg.path), from_ref=from_ref)

    typer.secho(f"\n🚀 {notes.version_title}\n", fg=typer.colors.GREEN, bold=True)
    typer.echo(notes.executive_summary + "\n")

    typer.secho("New Capabilities:", fg=typer.colors.CYAN, bold=True)
    for feat in notes.new_features:
        typer.echo(f"  • {feat}")

    typer.secho("\nOptimizations & Architecture:", fg=typer.colors.YELLOW, bold=True)
    for ref in notes.refactors_and_optimizations:
        typer.echo(f"  • {ref}")


if __name__ == "__main__":
    app()
