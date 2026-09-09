from pydantic import BaseModel, Field, ConfigDict


class WebSearchArguments(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    query: str = Field(
        min_length=3,
        max_length=300,
    )