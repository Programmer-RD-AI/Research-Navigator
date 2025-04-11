from crewai import Task, Agent
from typing import Optional, List, Type
from crewai.tools import BaseTool
from langsmith import traceable
from ..models import ResearchQuery, ResearchResponse, QuestionRelevancyResponse
from pydantic import BaseModel
import os
from fastapi import HTTPException, status


@traceable(run_type="task")
def question_relevancy_callback(task_output):
    """
    Callback for the question relevancy task.
    If the question is deemed irrelevant, routes feedback to the user.

    Args:
        task_output: TaskOutput object containing the result of the question relevancy task
    """
    if hasattr(task_output, "pydantic") and task_output.pydantic:
        relevancy_response = task_output.pydantic
        if not relevancy_response.relevant:
            # Raise a custom exception that can be caught by the router
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=relevancy_response.model_dump_json()
                or "The question is irrelevant.",  # Use the reason or a default message
            )


@traceable(run_type="task")
def get_question_relevancy_task(
    agent: Agent,
    query: ResearchQuery,
    tools: Optional[List[BaseTool]] = None,
    context: Optional[List[Task]] = None,
    output_file: Optional[str] = None,
    output_json: Optional[Type[BaseModel]] = None,
) -> Task:
    context_info = (
        f" Consider this additional context: {query.context}" if query.context else ""
    )

    if output_file is None:
        output_file = os.path.join("out", "question_relevancy.txt")

    return Task(
        agent=agent,
        description=f"Evaluate if the question '{query.query}' is relevant for research. Consider factors such as clarity, specificity, research potential, and whether it is answerable through research. Flag questions that are too vague, nonsensical, or impossible to research effectively.{context_info}",
        expected_output=f"A detailed assessment of the question's relevance with a clear YES/NO verdict for '{query.query}'. If deemed irrelevant, provide specific reasons and suggestions for improvement. If relevant, explain why it's a good research question.",
        name="Question Relevancy Assessment",
        async_execution=False,
        human_input=False,
        tools=tools or [],
        context=context or [],
        output_pydantic=QuestionRelevancyResponse,
        output_file=output_file,
        output_json=output_json,
        callback=question_relevancy_callback,  # Add our custom callback
    )


@traceable(run_type="task")
def get_research_approach_creation_task(
    agent: Agent,
    query: ResearchQuery,
    tools: Optional[List[BaseTool]] = None,
    context: Optional[List[Task]] = None,
    output_file: Optional[str] = None,
    output_json: Optional[Type[BaseModel]] = None,
) -> Task:
    context_info = (
        f" Take into account this additional context: {query.context}"
        if query.context
        else ""
    )

    if output_file is None:
        output_file = os.path.join("out", "research_approach.txt")

    return Task(
        agent=agent,
        description=f"Create a comprehensive research approach for the question: '{query.query}'. Outline the key areas to investigate, potential sources of information, and methodologies to employ. Consider different angles and perspectives that might provide valuable insights.{context_info}",
        expected_output=f"A structured research plan for '{query.query}' with clearly defined research areas, methodological approaches, and a step-by-step strategy for information gathering. Include potential challenges and how to address them.",
        name="Research Approach Creation",
        async_execution=False,
        human_input=False,
        tools=tools or [],
        context=context or [],
        output_file=output_file,
        output_json=output_json,
    )


@traceable(run_type="task")
def get_search_query_generation_task(
    agent: Agent,
    query: ResearchQuery,
    tools: Optional[List[BaseTool]] = None,
    context: Optional[List[Task]] = None,
    output_file: Optional[str] = None,
    output_json: Optional[Type[BaseModel]] = None,
) -> Task:
    context_info = (
        f" Consider this additional context: {query.context}" if query.context else ""
    )

    if output_file is None:
        output_file = os.path.join("out", "search_queries.txt")

    return Task(
        agent=agent,
        description=f"Generate a diverse set of search queries related to the research question: '{query.query}'. Create at least 5 distinct search queries that will help gather comprehensive information. Queries should target different aspects of the question and use varying keywords to maximize relevant results.{context_info}",
        expected_output=f"A list of at least 5 carefully crafted search queries for '{query.query}', each addressing different aspects or using different terminology. Each query should be accompanied by a brief explanation of what specific information it aims to retrieve.",
        name="Search Query Generation",
        async_execution=False,
        human_input=False,
        tools=tools or [],
        context=context or [],
        output_file=output_file,
        output_json=output_json,
    )


@traceable(run_type="task")
def get_rag_retrieval_results_task(
    agent: Agent,
    query: ResearchQuery,
    tools: Optional[List[BaseTool]] = None,
    context: Optional[List[Task]] = None,
    output_file: Optional[str] = None,
    output_json: Optional[Type[BaseModel]] = None,
) -> Task:
    context_info = (
        f" Take into account this additional context: {query.context}"
        if query.context
        else ""
    )

    if output_file is None:
        output_file = os.path.join("out", "rag_retrieval_results.txt")

    return Task(
        agent=agent,
        description=f"Using Retrieval Augmented Generation (RAG), retrieve relevant information from the knowledge base to answer the research question: '{query.query}'. Focus on finding high-quality, accurate information that directly addresses the question and provides context.{context_info}",
        expected_output=f"A comprehensive collection of retrieved information about '{query.query}' from the knowledge base, organized by relevance. Include direct quotes, key facts, and insights that help answer the research question. Provide source references where applicable.",
        name="RAG Retrieval",
        async_execution=True,
        human_input=False,
        tools=tools or [],
        context=context or [],
        output_file=output_file,
        output_json=output_json,
    )


@traceable(run_type="task")
def get_web_search_results_task(
    agent: Agent,
    query: ResearchQuery,
    tools: Optional[List[BaseTool]] = None,
    context: Optional[List[Task]] = None,
    output_file: Optional[str] = None,
    output_json: Optional[Type[BaseModel]] = None,
) -> Task:
    context_info = (
        f" Consider this additional context: {query.context}" if query.context else ""
    )

    if output_file is None:
        output_file = os.path.join("out", "web_search_results.txt")

    return Task(
        agent=agent,
        description=f"Conduct comprehensive web searches using the generated queries to find the most relevant and up-to-date information related to the research question: '{query.query}'. Focus on authoritative sources, recent publications, and diverse perspectives.{context_info}",
        expected_output=f"A collection of search results for '{query.query}' organized by query, including URLs, key snippets, publication dates, and source credibility assessment. Highlight the most valuable findings for each query and note any contradictory information.",
        name="Web Search Results",
        async_execution=True,
        human_input=False,
        tools=tools or [],
        context=context or [],
        output_file=output_file,
        output_json=output_json,
    )


@traceable(run_type="task")
def get_keep_relevant_data_task(
    agent: Agent,
    query: ResearchQuery,
    tools: Optional[List[BaseTool]] = None,
    context: Optional[List[Task]] = None,
    output_file: Optional[str] = None,
    output_json: Optional[Type[BaseModel]] = None,
) -> Task:
    context_info = (
        f" Take into account this additional context: {query.context}"
        if query.context
        else ""
    )

    if output_file is None:
        output_file = os.path.join("out", "relevant_data.txt")

    return Task(
        agent=agent,
        description=f"Critically evaluate all gathered information (from RAG and web searches) based on its direct relevance to the research question: '{query.query}'. Apply a strict filter, discarding any information that is tangential, low-quality, or lacks credible sourcing. Retain only the most pertinent and verifiable data points.{context_info}",
        expected_output=f"A curated dataset containing *only* the strictly relevant information for '{query.query}'. Each piece of retained data must be accompanied by its original source attribution. Clearly state if no relevant data was found after filtering. The output should be organized logically, ready for synthesis.",
        name="Strict Relevance Filtering and Data Curation",
        async_execution=False,
        human_input=False,
        tools=tools or [],
        context=context or [],
        output_file=output_file,
        output_json=output_json,
    )


@traceable(run_type="task")
def get_summarizing_task(
    agent: Agent,
    query: ResearchQuery,
    tools: Optional[List[BaseTool]] = None,
    context: Optional[List[Task]] = None,
    response_pydantic: BaseModel = ResearchResponse,
    output_file: Optional[str] = None,
    output_json: Optional[Type[BaseModel]] = None,
) -> Task:
    context_info = (
        f" Consider this additional context: {query.context}" if query.context else ""
    )

    if output_file is None:
        output_file = os.path.join("out", "research_synthesis.txt")

    return Task(
        agent=agent,
        description=f"Synthesize the curated, relevant information into a final, comprehensive, and coherent report answering the research question: '{query.query}'. Integrate the verified data points, ensuring a logical flow and addressing the core aspects of the query. *Crucially, every statement or piece of information presented must be accurately attributed to its source* based on the curated data provided in the context.{context_info}",
        expected_output=f"A well-structured, comprehensive report that directly answers '{query.query}', based *solely* on the provided relevant and sourced information. The report must include key findings, integrate different data points smoothly, and explicitly cite the source for *every* piece of information included. If no relevant data was provided, the report should state that a conclusive answer cannot be generated due to lack of information.",
        name="Final Report Synthesis with Citations",
        async_execution=False,
        human_input=False,
        tools=tools or [],
        context=context or [],
        output_pydantic=response_pydantic,
        output_file=output_file,
        output_json=output_json,
    )
