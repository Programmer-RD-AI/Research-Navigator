from crewai import Agent, Task
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from .schemas import ResearchQuery


class AgentInput(BaseModel):
    query: ResearchQuery = Field(
        ...,
        description="The research query to be processed by the agent.",
    )
    tools: list[BaseTool] | None = Field(
        None, description="List of tools available to the agent."
    )


class TaskInput(BaseModel):
    agent: Agent = Field(
        ...,
        description="The agent responsible for executing the task.",
    )
    query: ResearchQuery = Field(
        ...,
        description="The research query to be processed by the task.",
    )
    tools: list[BaseTool] | None = Field(
        None, description="List of tools available to the task."
    )
    context: list[Task] | None = Field(
        None,
        description="List of tasks that are contextually relevant to this task.",
    )
    output_file: str | None = Field(
        None,
        description="The file where the output will be saved.",
    )
    output_json: type[BaseModel] | None = Field(
        None,
        description="The JSON schema for the output of the task.",
    )
    response_pydantic: type[BaseModel] | None = Field(
        None,
        description="The Pydantic model for the response of the task.",
    )


class QuestionRelevancyResponse(BaseModel):
    query: str
    relevant: bool
    reasons: list[str] | None = None
    suggestions: list[str] | None = None
