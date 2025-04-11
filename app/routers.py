from fastapi import APIRouter
from .crew.crew import get_crew
from .models import ResearchQuery, ResearchResponse
import time

router = APIRouter(prefix="/api/v1", tags=["api"])


@router.post("/research-navigator", response_model=ResearchResponse)
async def research_navigator(query_data: ResearchQuery) -> ResearchResponse:
    """
    Endpoint to get the research navigator crew.
    """
    # Pass the query_data directly to get_crew instead of the hashable key
    start_time = time.time()
    crew = get_crew(query_data.dict(exclude_none=True))
    response = await crew.kickoff_async(
        inputs=query_data.dict(exclude_none=True),
    )
    end_time = time.time()
    print(response)
    response.pydantic.processing_time = end_time - start_time
    return response.pydantic
