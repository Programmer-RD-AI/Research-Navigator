from typing import Any

from pydantic import BaseModel, computed_field


class ResearchQuery(BaseModel):
    query: str
    context: str | None = None
    additional_params: dict | None = None

    def __hash__(self) -> int:
        dict_items = tuple(frozenset(self.dict(exclude_none=True).items()))
        return hash(dict_items)

    def __eq__(self, other: "ResearchQuery") -> bool:
        if not isinstance(other, ResearchQuery):
            return False
        return self.dict(exclude_none=True) == other.dict(exclude_none=True)

    @computed_field
    @property
    def context_info(self) -> str:
        return f"\nAdditional Context: {self.query.context}" if self.query.context else ""


class ResearchResponse(BaseModel):
    query: str
    findings: str
    sources: list[dict[str, Any]] = []
    confidence_score: float
    related_topics: list[str]
    processing_time: float | None
    metadata: dict[str, Any] | None
