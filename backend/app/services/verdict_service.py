
import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trial import Trial
from app.models.verdict import Verdict


async def save_verdict(
    db: AsyncSession,
    trial_id: int,
    verdict_data: dict
):
    # Verify that the trial exists
    trial = await db.get(Trial, trial_id)

    if not trial:
        raise ValueError(f"Trial {trial_id} does not exist")

    # Check whether a verdict already exists
    result = await db.execute(
        select(Verdict).where(Verdict.trial_id == trial_id)
    )

    verdict = result.scalar_one_or_none()

    if verdict is None:
        verdict = Verdict(trial_id=trial_id)
        db.add(verdict)

    # Save or update verdict details
    verdict.outcome = verdict_data["outcome"]
    verdict.accused = verdict_data["accused"]
    verdict.prosecution_assessment = verdict_data["prosecution_assessment"]
    verdict.defense_assessment = verdict_data["defense_assessment"]
    verdict.evidence_considered = json.dumps(
        verdict_data.get("evidence_considered", [])
    )
    verdict.reasoning = verdict_data["reasoning"]
    verdict.unresolved_questions = json.dumps(
        verdict_data.get("unresolved_questions", [])
    )
    verdict.limitations = json.dumps(
        verdict_data.get("limitations", [])
    )

    # Mark trial as completed
    trial.status = "completed"

    await db.commit()
    await db.refresh(verdict)

    return verdict
