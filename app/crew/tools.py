from langsmith import traceable

from ..config import (
    qdrant_vector_search_tool_config,
    tavily_extractor_tool_config,
    tavily_search_tool_config,
)
from ..temp.qdrant_search_tool import QdrantVectorSearchTool
from ..temp.tavily_extractor_tool import TavilyExtractorTool
from ..temp.tavily_search_tool import TavilySearchTool


@traceable(run_type="tool")
def get_tavily_extractor_tool() -> TavilyExtractorTool:
    return TavilyExtractorTool(**tavily_extractor_tool_config)


@traceable(run_type="tool")
def get_tavily_search_tool() -> TavilySearchTool:
    return TavilySearchTool(**tavily_search_tool_config)


@traceable(run_type="tool")
def get_qdrant_vector_search_tool() -> QdrantVectorSearchTool:
    return QdrantVectorSearchTool(**qdrant_vector_search_tool_config)
