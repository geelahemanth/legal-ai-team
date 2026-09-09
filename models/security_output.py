from typing import Literal
from pydantic import BaseModel, Field

class SecurityOutput(BaseModel):
    is_attack: bool = Field(
        description="True if the input attempts to manipulate or override the AI application's instructions."
    )

    attack_type: Literal[
        "prompt_injection",
        "system_prompt_extraction",
        "jailbreak",
        "none",
    ] = Field(
        description="The detected attack category."
    )

    reason: str = Field(
        description="Short explanation for the classification."
    )
