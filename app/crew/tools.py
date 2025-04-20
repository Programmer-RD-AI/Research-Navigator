from crewai_tools.tools import SerperDevTool
from langsmith import traceable

from ..config import qdrant_vector_search_tool_config, serper_dev_tool_config
from ..temp.qdrant_search_tool import QdrantVectorSearchTool


@traceable(run_type="tool")
def get_server_dev_tool() -> SerperDevTool:
    return SerperDevTool(**serper_dev_tool_config)


@traceable(run_type="tool")
def get_qdrant_vector_search_tool() -> QdrantVectorSearchTool:
    return QdrantVectorSearchTool(**qdrant_vector_search_tool_config)
