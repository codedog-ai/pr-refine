from os import environ as env

from dotenv import load_dotenv

load_dotenv(".env")

openai_api_key: str = env.get("OPENAI_API_KEY", "")

azure_openai_enabled: bool = env.get("AZURE_OPENAI_ENABLED") is not None
azure_openai_api_key: str = env.get("AZURE_OPENAI_API_KEY", "")
azure_openai_api_base: str = env.get("AZURE_OPENAI_API_BASE", "")
azure_openai_api_version: str = "2023-08-01-preview"
azure_openai_gpt35_dep_id: str = env.get("AZURE_OPENAI_GPT35_DEP_ID", "gpt-35-turbo")
azure_openai_gpt4_dep_id: str = env.get("AZURE_OPENAI_GPT4_DEP_ID", "gpt-4")
azure_openai_embedding_dep_id: str = env.get(
    "AZURE_OPENAI_EMBEDDING_DEP_ID", "text-embedding-ada-002"
)

qwen_enabled: bool = env.get("QWEN_ENABLED") is not None
