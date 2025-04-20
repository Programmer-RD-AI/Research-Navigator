from crewai import TaskOutput
from fastapi import HTTPException, status
from langsmith import traceable


@traceable(run_type="callback")
def question_relevancy_callback(task_output: TaskOutput) -> None:
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
