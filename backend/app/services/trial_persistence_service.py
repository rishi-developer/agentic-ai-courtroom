
import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trial_argument import TrialArgument
from app.models.witness_testimony import WitnessTestimony


async def save_argument(
    db: AsyncSession,
    trial_id: int,
    argument_data: dict
):
    argument = TrialArgument(
        trial_id=trial_id,
        agent=argument_data["agent"],
        action=argument_data["action"],
        argument=argument_data["argument"],
        supporting_evidence=json.dumps(
            argument_data.get("supporting_evidence", [])
        ),
        challenged_argument=argument_data.get("challenged_argument"),
        reasoning=argument_data["reasoning"]
    )

    db.add(argument)
    await db.commit()
    await db.refresh(argument)

    return argument


async def save_testimony(
    db: AsyncSession,
    trial_id: int,
    testimony_data: dict
):
    testimony = WitnessTestimony(
        trial_id=trial_id,
        witness_id=testimony_data["witness_id"],
        questioner=testimony_data["questioner"],
        question=testimony_data["question"],
        response=testimony_data["response"],
        knowledge_status=testimony_data["knowledge_status"],
        supporting_evidence=json.dumps(
            testimony_data.get("supporting_evidence", [])
        ),
        contradicts_previous_statement=testimony_data.get(
            "contradicts_previous_statement", False
        )
    )

    db.add(testimony)
    await db.commit()
    await db.refresh(testimony)

    return testimony
