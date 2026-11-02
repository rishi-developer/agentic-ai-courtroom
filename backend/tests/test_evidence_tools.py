import json
import pytest

from app.tools.tool_errors import tool_success_response
from app.tools.tool_errors import tool_error_response

from app.tools.evidence_tools import (
    get_case_evidence,
    search_case_evidence,
    get_evidence_details
)


@pytest.mark.asyncio
async def test_get_case_evidence():
    result = await get_case_evidence.ainvoke({
        "case_id": 1
    })

    data = json.loads(result)

    assert data["success"] is True
    assert data["data"]["case_id"] == 1


@pytest.mark.asyncio
async def test_search_empty_keyword():
    result = await search_case_evidence.ainvoke({
        "case_id": 1,
        "keyword": "   "
    })

    data = json.loads(result)

    assert data["success"] is False


@pytest.mark.asyncio
async def test_evidence_case_ownership():
    result = await get_evidence_details.ainvoke({
        "case_id": 2,
        "evidence_id": 1
    })

    data = json.loads(result)

    assert data["success"] is False
    assert data["error"] == "Evidence not found for this case"