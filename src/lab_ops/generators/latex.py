import ast
from pathlib import Path


def extract_docstrings_from_file(python_file: Path) -> dict[str, str]:
    """Extracts function and class docstrings using Python's AST parser."""
    with open(python_file, "r") as f:
        tree = ast.parse(f.read())

    docstrings = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            doc = ast.get_docstring(node)
            if doc:
                docstrings[node.name] = doc
    return docstrings
