# src/lab_ops/extractors/kinetics.py
import instructor
from openai import OpenAI
from lab_ops.rag.store import get_or_create_table
from lab_ops.schemas.kinetics import ParameterExtractionResult


def extract_kinetic_parameters(query: str, top_k: int = 5) -> ParameterExtractionResult:
    """Searches local literature store for relevant paper chunks and extracts structured parameters."""
    table = get_or_create_table()

    # 1. Search local literature table for top matching text chunks
    # Note: LanceDB provides vector or full-text search across chunks
    results = table.search(query).limit(top_k).to_list()

    if not results:
        return ParameterExtractionResult(
            query_target=query,
            parameters=[],
            confidence_notes="No literature chunks found in local LanceDB store. Try ingesting papers first.",
        )

    context_str = "\n\n---\n\n".join(
        [f"Source: {r['filename']}\n{r['text']}" for r in results]
    )

    # 2. Pass retrieved context to instructor for structured schema extraction
    client = instructor.from_openai(OpenAI())

    extraction = client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=ParameterExtractionResult,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a computational biophysicist extracting precise kinetic parameters "
                    "for kinase-substrate interactions (aPKC, Lgl, Par6) from paper snippets. "
                    "Only extract parameters explicitly supported by the text."
                ),
            },
            {
                "role": "user",
                "content": f"Target Query: {query}\n\nRetrieved Literature Snippets:\n{context_str}",
            },
        ],
    )
    return extraction
