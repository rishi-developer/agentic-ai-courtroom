import json
import pytest

from app.tools.witness_tools import (
    get_case_witnesses,
    get_witness_details
)


@pytest.mark.asyncio
async def test_get_case_witnesses():
    result = await get_case_witnesses.ainvoke({
        "case_id": 1
    })

    data = json.loads(result)

    assert data["success"] is True
    assert data["data"]["case_id"] == 1


@pytest.mark.asyncio
async def test_invalid_witness_id():
    result = await get_witness_details.ainvoke({
        "witness_id": -1
    })

    data = json.loads(result)

    assert data["success"] is False
    assert "Invalid witness ID" in data["error"]