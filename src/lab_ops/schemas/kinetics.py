from pydantic import BaseModel, Field


class KineticParameter(BaseModel):
    """Schema for a single extracted biophysical or kinetic parameter."""

    enzyme: str = Field(
        description="Enzyme name, e.g., aPKC, PKCzeta, or aPKC-Par6 complex"
    )
    substrate: str = Field(
        description="Substrate protein or peptide target, e.g., Lgl1, Lgl-Ser643, Par6"
    )
    parameter_type: str = Field(
        description="Type of constant: k_cat, K_m, k_obs, K_d, or dissociation_rate"
    )
    value: float = Field(description="Numerical value of the parameter")
    unit: str = Field(description="Measurement units, e.g., 1/s, uM, nM, 1/min")
    experimental_conditions: str | None = Field(
        default=None,
        description="Buffer, pH, temperature, or ATP concentration if specified",
    )
    source_citation: str = Field(
        description="Paper title, author, or figure/table reference"
    )


class ParameterExtractionResult(BaseModel):
    """Container schema for structured extraction results from literature."""

    query_target: str = Field(description="Original search target or question")
    parameters: list[KineticParameter] = Field(
        default_factory=list, description="Extracted parameters found in text"
    )
    confidence_notes: str | None = Field(
        default=None,
        description="Notes on experimental ambiguities or missing conditions",
    )
