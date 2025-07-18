import json
import os
from collections.abc import Callable  # Import Callable from collections.abc
from typing import Any, ClassVar  # Import ClassVar

try:
    from qdrant_client import AsyncQdrantClient, QdrantClient
    from qdrant_client.http.models import FieldCondition, Filter, MatchValue

    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False
    QdrantClient = Any  # type placeholder
    Filter = Any
    FieldCondition = Any
    MatchValue = Any

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class QdrantToolSchema(BaseModel):
    """Input for QdrantTool."""

    query: str = Field(
        ...,
        description=(
            "The query to search retrieve relevant information from the Qdrant database. "  # Shorten line
            "Pass only the query, not the question."
        ),
    )
    filter_by: str | None = Field(
        default=None,
        description="Filter by properties. Pass only the properties, not the question.",
    )
    filter_value: str | None = Field(
        default=None,
        description="Filter by value. Pass only the value, not the question.",
    )


class QdrantVectorSearchTool(BaseTool):
    """Tool to query and filter results from a Qdrant database.

    This tool enables vector similarity search on internal documents stored in Qdrant,
    with optional filtering capabilities.

    Attributes:
        client: Configured QdrantClient instance
        collection_name: Name of the Qdrant collection to search
        limit: Maximum number of results to return
        score_threshold: Minimum similarity score threshold
        qdrant_url: Qdrant server URL
        qdrant_api_key: Authentication key for Qdrant
    """

    model_config: ClassVar[dict[str, bool]] = {"arbitrary_types_allowed": True}  # Add ClassVar annotation
    client: QdrantClient = None
    async_client: AsyncQdrantClient = None
    openai_client: Any = None  # Added for lazy initialization
    openai_async_client: Any = None  # Added for lazy initialization
    name: str = "QdrantVectorSearchTool"
    description: str = "A tool to search the Qdrant database for relevant information on internal documents."
    args_schema: type[BaseModel] = QdrantToolSchema
    query: str | None = None
    filter_by: str | None = None
    filter_value: str | None = None
    collection_name: str | None = None
    limit: int | None = Field(default=3)
    score_threshold: float = Field(default=0.35)
    qdrant_url: str = Field(
        ...,
        description="The URL of the Qdrant server",
    )
    qdrant_api_key: str | None = Field(
        default=None,
        description="The API key for the Qdrant server",
    )
    custom_embedding_fn: Callable | None = Field(
        default=None,
        description=(
            "A custom embedding function to use for vectorization. "  # Shorten line
            "If not provided, the default model will be used."
        ),
    )

    def __init__(self, **kwargs: Any) -> None:  # Add type hints for kwargs and return
        """Initialize QdrantVectorSearchTool."""  # Add docstring
        super().__init__(**kwargs)
        if QDRANT_AVAILABLE:
            self.client = QdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_api_key if self.qdrant_api_key else None,
            )
            self.async_client = AsyncQdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_api_key if self.qdrant_api_key else None,
            )
        else:
            import click

            if click.confirm(
                "The 'qdrant-client' package is required to use the QdrantVectorSearchTool. "
                "Would you like to install it?"
            ):
                import subprocess

                subprocess.run(["/usr/bin/uv", "add", "qdrant-client"], check=True)
            else:
                # Define error messages as constants
                qdrant_client_pkg_required_error_msg = (
                    "The 'qdrant-client' package is required to use the QdrantVectorSearchTool. "
                    "Please install it with: uv add qdrant-client"
                )
                raise ImportError(qdrant_client_pkg_required_error_msg)

    def _run(
        self,
        query: str,
        filter_by: str | None = None,
        filter_value: str | None = None,
    ) -> str:
        """Execute vector similarity search on Qdrant.

        Args:
            query: Search query to vectorize and match
            filter_by: Optional metadata field to filter on
            filter_value: Optional value to filter by

        Returns:
            JSON string containing search results with metadata and scores

        Raises:
            ImportError: If qdrant-client is not installed
            ValueError: If Qdrant credentials are missing
        """
        # Define error messages as constants
        qdrant_url_not_set_error_msg = "QDRANT_URL is not set"
        if not self.qdrant_url:
            raise ValueError(qdrant_url_not_set_error_msg)

        # Create filter if filter parameters are provided
        search_filter = None
        if filter_by and filter_value:
            search_filter = Filter(must=[FieldCondition(key=filter_by, match=MatchValue(value=filter_value))])

        # Search in Qdrant using the built-in query method
        query_vector = (
            self._vectorize_query_sync(query, embedding_model="text-embedding-3-large")
            if not self.custom_embedding_fn
            else self.custom_embedding_fn(query)
        )
        search_results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=search_filter,
            limit=self.limit,
            score_threshold=self.score_threshold,
        )

        # Format results similar to storage implementation
        results = []
        # Extract the list of ScoredPoint objects from the tuple
        for point in search_results:
            result = {
                "metadata": point[1][0].payload.get("metadata", {}),
                "context": point[1][0].payload.get("text", ""),
                "distance": point[1][0].score,
            }
            results.append(result)

        return json.dumps(results, indent=2)

    def _vectorize_query_sync(self, query: str, embedding_model: str) -> list[float]:
        """Default sync vectorization function with openai.

        Args:
            query (str): The query to vectorize
            embedding_model (str): The embedding model to use

        Returns:
            list[float]: The vectorized query
        """
        from openai import Client

        # Define error messages as constants
        openai_api_key_not_set_error_msg = "OPENAI_API_KEY environment variable is not set."
        # Lazy initialization of the sync client
        if not self.openai_client:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(openai_api_key_not_set_error_msg)
            self.openai_client = Client(api_key=api_key)

        embedding = (
            self.openai_client.embeddings.create(
                input=[query],
                model=embedding_model,
            )
            .data[0]
            .embedding
        )
        return embedding

    async def _arun(
        self,
        query: str,
        filter_by: str | None = None,
        filter_value: str | None = None,
    ) -> str:
        """Execute vector similarity search on Qdrant.

        Args:
            query: Search query to vectorize and match
            filter_by: Optional metadata field to filter on
            filter_value: Optional value to filter by

        Returns:
            JSON string containing search results with metadata and scores

        Raises:
            ImportError: If qdrant-client is not installed
            ValueError: If Qdrant credentials are missing
        """
        # Define error messages as constants
        qdrant_url_not_set_error_msg = "QDRANT_URL is not set"
        if not self.qdrant_url:
            raise ValueError(qdrant_url_not_set_error_msg)

        # Create filter if filter parameters are provided
        search_filter = None
        if filter_by and filter_value:
            search_filter = Filter(must=[FieldCondition(key=filter_by, match=MatchValue(value=filter_value))])

        # Search in Qdrant using the built-in query method
        query_vector = (
            await self._vectorize_query_async(query, embedding_model="text-embedding-3-large")
            if not self.custom_embedding_fn
            else self.custom_embedding_fn(query)
        )
        search_results = await self.async_client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=search_filter,
            limit=self.limit,
            score_threshold=self.score_threshold,
        )

        # Format results similar to storage implementation
        results = []
        # Extract the list of ScoredPoint objects from the tuple
        for point in search_results:
            result = {
                "metadata": point[1][0].payload.get("metadata", {}),
                "context": point[1][0].payload.get("text", ""),
                "distance": point[1][0].score,
            }
            results.append(result)

        return json.dumps(results, indent=2)

    async def _vectorize_query_async(self, query: str, embedding_model: str) -> list[float]:
        """Default async vectorization function with openai.

        Args:
            query (str): The query to vectorize
            embedding_model (str): The embedding model to use

        Returns:
            list[float]: The vectorized query
        """
        from openai import AsyncClient

        # Define error messages as constants
        openai_api_key_not_set_error_msg = "OPENAI_API_KEY environment variable is not set."
        # Lazy initialization of the async client
        if not self.openai_async_client:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(openai_api_key_not_set_error_msg)
            self.openai_async_client = AsyncClient(api_key=api_key)

        embedding = (
            await self.openai_async_client.embeddings.create(
                input=[query],
                model=embedding_model,
            )
            .data[0]
            .embedding
        )
        return embedding
