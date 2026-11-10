import asyncio

from sqlalchemy import select

from app.database.connection import AsyncSessionLocal
from app.models.witness import Witness


async def seed_witnesses():
    async with AsyncSessionLocal() as session:

        result = await session.execute(
            select(Witness).where(Witness.case_id == 1)
        )

        existing_witnesses = result.scalars().all()

        if existing_witnesses:
            print("Witnesses already exist.")
            return

        witnesses = [
            Witness(
                case_id=1,
                name="Sarah",
                role="Project Manager",
                knowledge_profile=(
                    "Sarah was the project manager. "
                    "She knows about the project laptop and "
                    "the office access procedures. "
                    "She does not know who physically removed the laptop."
                ),
                original_statement=(
                    "I left the office around 6 PM. "
                    "I did not see anyone taking the laptop."
                )
            ),
            Witness(
                case_id=1,
                name="David",
                role="IT Administrator",
                knowledge_profile=(
                    "David manages IT equipment and access logs. "
                    "He claims he saw Alex carrying a bag that evening. "
                    "He cannot confirm what was inside the bag."
                ),
                original_statement=(
                    "I saw Alex carrying a bag near the office exit."
                )
            )
        ]

        session.add_all(witnesses)
        await session.commit()

        print("Sample witnesses added successfully.")


if __name__ == "__main__":
    asyncio.run(seed_witnesses())