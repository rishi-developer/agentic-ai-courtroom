from langchain_openai import ChatOpenAI

from app.config.settings import settings


llm = ChatOpenAI(
    model=settings.OPENAI_MODEL,
    api_key=settings.OPENAI_API_KEY,
    temperature=0.2,
    max_retries=2,
    timeout=30
)