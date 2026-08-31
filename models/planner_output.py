from typing import Literal
from pydantic import BaseModel


class PlannerOutput(BaseModel):

    analysis_type: Literal[
        "Contract Review",
        "Compliance Check",
        "Risk Assessment",
        "Legal Research",
    ]

    requires_research: bool

    search_query: str