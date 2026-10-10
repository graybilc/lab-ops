from pathlib import Path
import typer
from lab_ops.adapters.generic import GenericRepoAdapter
from lab_ops.rag.store import ingest_pdf
from lab_ops.extractors.kinetics import extract_kinetic_parameters
from lab_ops.config import LabOpsConfig, CONFIG_PATH
from lab_ops.reporting.changelog import generate_release_notes
from lab_ops.reporting.benchmarks import analyze_sandbox_notebook

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
def ingest(
    pdf_path: Path = typer.Argument(
        ..., help="Path to PDF research paper to ingest into local database"
    )
):
    """Ingest a PDF research paper into local LanceDB literature store."""
    typer.echo(f"Ingesting paper: {pdf_path.name}...")
    num_chunks = ingest_pdf(pdf_path)
    typer.secho(
        f"Successfully indexed {num_chunks} text chunks into local DB!",
        fg=typer.colors.GREEN,
        bold=True,
    )


@app.command()
def extract(
    query: str = typer.Argument(
        ..., help="Kinetic search query (e.g. 'aPKC phosphorylation rate of Lgl')"
    )
):
    """Query local literature store and extract structured kinetic parameters for ODE bounds."""
    typer.echo(f"Searching literature for: '{query}'...\n")
    result = extract_kinetic_parameters(query)

    if not result.parameters:
        typer.secho("No matching kinetic parameters found.", fg=typer.colors.YELLOW)
        if result.confidence_notes:
            typer.echo(f"Note: {result.confidence_notes}")
        return

    typer.secho(
        f"Results for target: {result.query_target}\n", fg=typer.colors.CYAN, bold=True
    )
    for p in result.parameters:
        typer.echo(
            f"  • {p.enzyme} + {p.substrate}: {p.parameter_type} = {p.value} {p.unit}"
        )
        if p.experimental_conditions:
            typer.echo(f"    Conditions: {p.experimental_conditions}")
        typer.echo(f"    Source: {p.source_citation}\n")


@app.command()
def changelog(
    repo_key: str = typer.Option(
        "polarity", "--repo", "-r", help="Target repository key in config"
    ),
    from_ref: str = typer.Option(
        "HEAD~15", "--from", help="Git ref start (e.g., HEAD~15 or v0.1.0)"
    ),
    to_ref: str = typer.Option("HEAD", "--to", help="Git ref end (defaults to HEAD)"),
):
    """Synthesize raw Git commits into structured version release notes."""
    config = LabOpsConfig.load_from_yaml(CONFIG_PATH)

    if repo_key not in config.repositories:
        typer.secho(
            f"Error: Repository '{repo_key}' not found in ~/.lab-ops.yaml config.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    repo_cfg = config.repositories[repo_key]
    repo_path = Path(repo_cfg.path)

    typer.echo(f"Analyzing commits in {repo_cfg.name} ({from_ref} .. {to_ref})...\n")

    try:
        notes = generate_release_notes(repo_path, from_ref=from_ref, to_ref=to_ref)
    except Exception as e:
        typer.secho(f"Failed to generate release notes: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho(f"🚀 {notes.version_title}", fg=typer.colors.GREEN, bold=True)
    typer.echo(f"\n{notes.executive_summary}\n")

    if notes.new_features:
        typer.secho("New Capabilities:", fg=typer.colors.CYAN, bold=True)
        for feat in notes.new_features:
            typer.echo(f"  • {feat}")

    if notes.refactors_and_optimizations:
        typer.secho("\nRefactors & Optimizations:", fg=typer.colors.YELLOW, bold=True)
        for ref in notes.refactors_and_optimizations:
            typer.echo(f"  • {ref}")

    if notes.breaking_changes:
        typer.secho(
            "\n⚠️ Breaking Changes & Schema Updates:", fg=typer.colors.RED, bold=True
        )
        for break_change in notes.breaking_changes:
            typer.echo(f"  • {break_change}")

@app.command()
def analyze_notebook(
    notebook_path: Path = typer.Argument(..., help="Path to executed .ipynb file")
):
    """Analyze cell outputs of a sandbox notebook and extract key findings."""
    typer.echo(f"Analyzing {notebook_path.name}...")
    report = analyze_sandbox_notebook(notebook_path)
    
    typer.secho(f"\n📊 Summary for {report.notebook_name}", fg=typer.colors.GREEN, bold=True)
    typer.echo(f"\nCore Takeaway:\n{report.core_finding}\n")
    
    if report.performance_notes:
        typer.secho("Performance Metrics:", fg=typer.colors.CYAN)
        for note in report.performance_notes:
            typer.echo(f"  • {note}")
            
    if report.action_items:
        typer.secho("\nAction Items for polarity-engine:", fg=typer.colors.YELLOW)
        for item in report.action_items:
            typer.echo(f"  • {item}")

if __name__ == "__main__":
    app()
