from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

CHECKPOINT_DATABASE = "./courtroom_checkpoints.db"


async def get_checkpointer():
    async with AsyncSqliteSaver.from_conn_string(
        CHECKPOINT_DATABASE
    ) as checkpointer:
        yield checkpointer