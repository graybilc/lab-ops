from pathlib import Path
from pydantic import BaseModel, Field
import nbformat
import instructor
from openai import OpenAI


class NotebookAnalysis(BaseModel):
    """Schema for distilling key findings and performance stats from an exploratory notebook."""

    notebook_name: str = Field(description="Filename of the analyzed notebook")
    core_finding: str = Field(
        description="Summary of the biophysical or algorithmic takeaway"
    )
    performance_notes: list[str] = Field(
        description="Execution times, matrix dimensions, or memory stats mentioned in outputs"
    )
    action_items: list[str] = Field(
        description="Insights or parameter bounds to carry into polarity-engine"
    )


def analyze_sandbox_notebook(notebook_path: Path) -> NotebookAnalysis:
    """Reads an executed Jupyter notebook from aPKC-mechanics-analysis and extracts key stats."""

    # 1. Parse notebook JSON with nbformat
    nb = nbformat.read(notebook_path, as_version=4)

    # 2. Extract code and markdown outputs
    cell_summaries = []
    for idx, cell in enumerate(nb.cells):
        if cell.cell_type == "code" and cell.get("outputs"):
            # Collect cell source and plain text outputs
            output_text = ""
            for out in cell.outputs:
                if "text" in out:
                    output_text += out["text"]
            if output_text:
                cell_summaries.append(
                    f"Cell {idx} Source:\n{cell.source}\nOutput:\n{output_text}\n"
                )

    combined_text = "\n---\n".join(cell_summaries[-5:])  # Focus on final output cells

    # 3. LLM extracts structured insights
    client = instructor.from_openai(OpenAI())

    report = client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=NotebookAnalysis,
        messages=[
            {
                "role": "system",
                "content": "You are a senior computational biophysicist summarizing sandbox research notebooks.",
            },
            {
                "role": "user",
                "content": f"Analyze these execution outputs from notebook {notebook_path.name}:\n{combined_text}",
            },
        ],
    )
    return report
