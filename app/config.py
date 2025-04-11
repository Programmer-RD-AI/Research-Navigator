from .utils import get_env_variable

serper_dev_tool_config = {"save_file": True, "n_results": 5}
qdrant_vector_search_tool_config = {
    "collection_name": "research",
    "limit": 5,
    "score_threshold": 0.5,
    "qdrant_url": get_env_variable("QDRANT_URL"),
    "qdrant_api_key": get_env_variable("QDRANT_API_KEY"),
}
AGENT_VERBOSE = True
CREW_VERBOSE = True
