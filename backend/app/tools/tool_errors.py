import logging

logger = logging.getLogger(__name__)


def tool_error_response(
    tool_name: str,
    error_message: str,
    reference_id: int | None = None
) -> str:
    import json

    logger.warning(
        "%s failed: %s | Reference ID: %s",
        tool_name,
        error_message,
        reference_id
    )

    return json.dumps({
        "success": False,
        "error": error_message,
        "reference_id": reference_id
    })


def tool_success_response(data: dict) -> str:
    import json

    return json.dumps({
        "success": True,
        "data": data
    })