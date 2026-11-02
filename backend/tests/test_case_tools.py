import json
import pytest

from app.tools.case_tools import (
    get_case_details,
    get_case_suspects
)


@pytest.mark.asyncio
async def test_get_existing_case():
    result = await get_case_details.ainvoke({
        "case_id": 1
    })

    data = json.loads(result)

    assert data["success"] is True
    assert data["data"]["id"] == 1


@pytest.mark.asyncio
async def test_get_invalid_case():
    result = await get_case_details.ainvoke({
        "case_id": -1
    })

    data = json.loads(result)

    assert data["success"] is False
    assert "Invalid case ID" in data["error"]


@pytest.mark.asyncio
async def test_get_nonexistent_case():
    result = await get_case_details.ainvoke({
        "case_id": 999999
    })

    data = json.loads(result)

    assert data["success"] is False
    assert data["error"] == "Case not found"