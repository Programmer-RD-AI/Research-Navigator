from crewai import Crew

from .agents import (
    get_relevancy_agent,
    get_research_agent,
    get_query_agent,
    get_retrieval_agent,
    get_synthesizer_agent,
)
from .tasks import (
    get_question_relevancy_task,
    get_research_approach_creation_task,
    get_search_query_generation_task,
    get_rag_retrieval_results_task,
    get_web_search_results_task,
    get_keep_relevant_data_task,
    get_summarizing_task,
)
from .tools import get_server_dev_tool, get_qdrant_vector_search_tool
from ..config import CREW_VERBOSE
from ..models import ResearchQuery
from langsmith import traceable


@traceable(run_type="crew")
def get_research_crew(query: ResearchQuery) -> Crew:
    """
    Create and configure the Research Navigator crew.

    This crew coordinates multiple specialized agents to process research questions,
    gather relevant information, and synthesize comprehensive answers.

    Returns:
        Crew: A configured crew instance ready for research tasks.
    """
    # Initialize tools
    serper_tool = get_server_dev_tool()
    qdrant_tool = get_qdrant_vector_search_tool()

    # Initialize agents with appropriate tools
    relevancy_agent = get_relevancy_agent(query)
    research_agent = get_research_agent(query, [serper_tool])
    query_agent = get_query_agent(query)
    retrieval_agent = get_retrieval_agent(query, [serper_tool, qdrant_tool])
    synthesizer_agent = get_synthesizer_agent(query)

    # Initialize tasks with assigned agents
    question_relevancy_task = get_question_relevancy_task(relevancy_agent, query)
    research_approach_task = get_research_approach_creation_task(
        research_agent, query, [serper_tool]
    )
    search_query_task = get_search_query_generation_task(query_agent, query)
    rag_retrieval_task = get_rag_retrieval_results_task(
        retrieval_agent, query, [qdrant_tool], [search_query_task]
    )
    web_search_task = get_web_search_results_task(
        retrieval_agent, query, [serper_tool], [search_query_task]
    )
    keep_relevant_data_task = get_keep_relevant_data_task(
        relevancy_agent, query, [], [rag_retrieval_task, web_search_task]
    )
    summarizing_task = get_summarizing_task(
        synthesizer_agent,
        query,
        [],
        [
            question_relevancy_task,
            research_approach_task,
            search_query_task,
            rag_retrieval_task,
            web_search_task,
            keep_relevant_data_task,
        ],
    )

    # Create the crew with sequential workflow
    research_crew = Crew(
        agents=[
            relevancy_agent,
            research_agent,
            query_agent,
            retrieval_agent,
            synthesizer_agent,
        ],
        tasks=[
            question_relevancy_task,
            research_approach_task,
            search_query_task,
            rag_retrieval_task,
            web_search_task,
            keep_relevant_data_task,
            summarizing_task,
        ],
        verbose=CREW_VERBOSE,
        memory=True,
        cache=True,
        name="Research Navigator Crew",
    )

    return research_crew


def get_crew(query_dict: dict) -> Crew:
    """
    Legacy function to maintain compatibility with existing code.

    Returns:
        Crew: A research navigator crew.
    """
    # Convert the dict back to ResearchQuery
    query = ResearchQuery(**query_dict)
    return get_research_crew(query)
