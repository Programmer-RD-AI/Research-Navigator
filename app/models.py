from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ResearchQuery(BaseModel):
    """
    Model for research query input.
    """

    query: str
    context: Optional[str] = None
    additional_params: Optional[dict] = None

    def __hash__(self):
        # Create a hash based on the immutable attributes
        # Converting dict to tuple of frozensets to make it hashable
        dict_items = tuple(frozenset(self.dict(exclude_none=True).items()))
        return hash(dict_items)

    def __eq__(self, other):
        if not isinstance(other, ResearchQuery):
            return False
        return self.dict(exclude_none=True) == other.dict(exclude_none=True)


class ResearchResponse(BaseModel):
    """
    Model for research query response output.
    """

    query: str
    findings: str
    sources: List[Dict[str, Any]] = []
    confidence_score: float
    related_topics: List[str]
    processing_time: Optional[float]
    metadata: Optional[Dict[str, Any]]


class QuestionRelevancyResponse(BaseModel):
    """
    Model for question relevancy assessment response.
    """

    query: str
    relevant: bool
    reasons: Optional[List[str]] = None
    suggestions: Optional[List[str]] = None
