from crewai_tools.tools import SerperDevTool
from ..temp.qdrant_search_tool import QdrantVectorSearchTool
from ..config import serper_dev_tool_config, qdrant_vector_search_tool_config
from langsmith import traceable


@traceable(run_type="tool")
def get_server_dev_tool() -> SerperDevTool:
    return SerperDevTool(**serper_dev_tool_config)


@traceable(run_type="tool")
def get_qdrant_vector_search_tool() -> QdrantVectorSearchTool:
    return QdrantVectorSearchTool(**qdrant_vector_search_tool_config)
