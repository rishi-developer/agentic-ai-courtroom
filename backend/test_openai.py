import asyncio

from app.llm.openai_client import llm
from langchain_core.messages import SystemMessage, HumanMessage

from app.config.settings import settings



from pathlib import Path

env_path = Path(".env")



async def main():

    messages = [
        SystemMessage(
            content="You are an assistant in a fictional courtroom."
        ),
        HumanMessage(
            content="What is the difference between evidence and an assumption?"
        )
    ]

    response = await llm.ainvoke(messages)

    print("\nOpenAI Response:\n")
    print(response.content)






if __name__ == "__main__":
    asyncio.run(main())