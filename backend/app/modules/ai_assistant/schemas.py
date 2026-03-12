from __future__ import annotations

from pydantic import BaseModel


class AiInsightRead(BaseModel):
    summary: str
    risks: list[str]

    model_config = {"from_attributes": True}
