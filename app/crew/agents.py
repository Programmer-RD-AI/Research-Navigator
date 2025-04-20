from crewai import Agent
from crewai.tools import BaseTool
from typing import List, Optional
from ..config import AGENT_VERBOSE
from langsmith import traceable
from ..models import ResearchQuery


@traceable(run_type="agent")
def get_relevancy_agent(
    query: ResearchQuery, tools: Optional[List[BaseTool]] = None
) -> Agent:
    # Add context at the end
    context_info = f"\nAdditional Context: {query.context}" if query.context else ""

    return Agent(
        role="Critical Relevancy Assessor",
        goal=f"Accurately assess if provided information *directly* answers or supports the research query: '{query.query}', applying a strict relevancy threshold. Filter out irrelevant or tangential content.",
        backstory=f"""You are a meticulous Relevancy Assessor specializing in information verification and filtering. 
        Your core function is to determine if content strictly pertains to the specific research query '{query.query}'{context_info}. 
        You are uncompromising in discarding information that does not meet the required relevancy threshold, ensuring only the most pertinent data proceeds.""",
        verbose=AGENT_VERBOSE,
        allow_delegation=False,
        tools=tools or [],
    )


@traceable(run_type="agent")
def get_research_agent(
    query: ResearchQuery, tools: Optional[List[BaseTool]] = None
) -> Agent:
    # Add context at the end
    context_info = f"\nAdditional Context: {query.context}" if query.context else ""

    return Agent(
        role="Diligent Research Specialist",
        goal=f"Conduct comprehensive and accurate research to find information directly addressing the query: '{query.query}'. Prioritize credible sources and ensure all findings are verifiable and properly sourced.",
        backstory=f"""You are a highly skilled Research Specialist dedicated to uncovering factual and relevant information. 
        Your methodology involves exploring diverse, credible sources to build a thorough understanding of the research topic: '{query.query}'{context_info}. 
        You meticulously document sources for all gathered information. You are allowed to delegate tasks like searching and retrieving information.""",
        verbose=AGENT_VERBOSE,
        allow_delegation=True,  # Research agent can delegate searching/retrieving
        tools=tools or [],
    )


@traceable(run_type="agent")
def get_query_agent(
    query: ResearchQuery, tools: Optional[List[BaseTool]] = None
) -> Agent:
    # Add context at the end
    context_info = f"\nAdditional Context: {query.context}" if query.context else ""

    return Agent(
        role="Strategic Query Architect",
        goal=f"Generate a diverse set of precise and effective search queries specifically designed to uncover information relevant to the research question: '{query.query}'.",
        backstory=f"""You are a Strategic Query Architect with expertise in translating complex research questions into optimal search terms. 
        You understand search engine nuances and information retrieval techniques. 
        Your task is to formulate multiple, targeted queries for the question: '{query.query}'{context_info}, maximizing the chances of retrieving relevant and comprehensive results.""",
        verbose=AGENT_VERBOSE,
        allow_delegation=False,
        tools=tools or [],
    )


@traceable(run_type="agent")
def get_retrieval_agent(
    query: ResearchQuery, tools: Optional[List[BaseTool]] = None
) -> Agent:
    # Add context at the end
    context_info = f"\nAdditional Context: {query.context}" if query.context else ""

    return Agent(
        role="Precision Information Retriever",
        goal=f"Execute search queries to retrieve specific, relevant information for the query: '{query.query}'. Retrieve content accurately and ensure proper source attribution. If no relevant information is found for a query, report that clearly without fabricating results.",
        backstory=f"""You are a Precision Information Retriever adept at using search tools and databases. 
        Your mission is to fetch information pertinent to the research query: '{query.query}'{context_info}. 
        You prioritize accuracy and source integrity. Critically, if a search yields no relevant results, you report this outcome truthfully and do *not* generate or hallucinate information. 
        All retrieved data *must* be accompanied by its source.""",
        verbose=AGENT_VERBOSE,
        allow_delegation=False,  # Should execute specific retrieval tasks based on queries
        tools=tools or [],
    )


@traceable(run_type="agent")
def get_synthesizer_agent(
    query: ResearchQuery, tools: Optional[List[BaseTool]] = None
) -> Agent:
    # Add context at the end
    context_info = f"\nAdditional Context: {query.context}" if query.context else ""

    return Agent(
        role="Insightful Research Synthesizer",
        goal=f"Synthesize the collected, relevant findings about '{query.query}' into a cohesive, well-structured, and insightful narrative. Ensure all claims are supported by evidence and properly cited with sources.",
        backstory=f"""You are an Insightful Research Synthesizer skilled at weaving together disparate pieces of verified information into a coherent and comprehensive summary. 
        You excel at identifying key themes, drawing connections, and presenting findings clearly and accurately. 
        Your task is to create a final report for the query: '{query.query}'{context_info}, ensuring all information is accurately represented and *properly attributed* to its original source. Do not include information without a source.""",
        verbose=AGENT_VERBOSE,
        allow_delegation=False,
        tools=tools or [],
    )
