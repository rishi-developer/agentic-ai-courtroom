import asyncio

from app.database.connection import create_tables


async def main():
    await create_tables()
    print("Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(main())