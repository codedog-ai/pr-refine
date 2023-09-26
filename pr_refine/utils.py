from dashscope import Generation
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import Tongyi
from langchain.schema.language_model import BaseLanguageModel

import pr_refine.config as cfg


def load_gpt35_llm(temperature: float = 0.0) -> BaseLanguageModel:
    """Load GPT 3.5 Model"""
    if cfg.qwen_enabled:
        llm = Tongyi(
            client=Generation(),
            model_name="qwen-turbo",
        )
    elif cfg.azure_openai_enabled:
        llm = AzureChatOpenAI(
            openai_api_type="azure",
            openai_api_key=cfg.azure_openai_api_key,
            openai_api_base=cfg.azure_openai_api_base,
            openai_api_version=cfg.azure_openai_api_version,
            deployment_name=cfg.azure_openai_gpt35_dep_id,
            model="gpt-3.5-turbo",
            temperature=temperature,
        )
    else:
        llm = ChatOpenAI(
            openai_api_key=cfg.openai_api_key,
            model="gpt-3.5-turbo",
            temperature=temperature,
        )
    return llm


def load_gpt4_llm(temperature: float = 0.0):
    """Load GPT 4 Model. Make sure your key have access to GPT 4 API. call this function won't check it."""
    if cfg.azure_openai_enabled:
        llm = AzureChatOpenAI(
            openai_api_type="azure",
            openai_api_key=cfg.azure_openai_api_key,
            openai_api_base=cfg.azure_openai_api_base,
            openai_api_version=cfg.azure_openai_api_version,
            deployment_name=cfg.azure_openai_gpt4_dep_id,
            model="gpt-4",
            temperature=temperature,
        )
    else:
        llm = ChatOpenAI(
            openai_api_key=cfg.openai_api_key, model="gpt-4", temperature=temperature
        )
    return llm


def load_embeddings():
    if cfg.azure_openai_enabled:
        embeddings = OpenAIEmbeddings(
            client=None,
            openai_api_type="azure",
            openai_api_key=cfg.azure_openai_api_key,
            openai_api_base=cfg.azure_openai_api_base,
            openai_api_version=cfg.azure_openai_api_version,
            deployment=cfg.azure_openai_embedding_dep_id,
        )
    else:
        embeddings = OpenAIEmbeddings(
            client=None,
            openai_api_key=cfg.openai_api_key,
        )

    return embeddings


def load_tongyi():
    llm = Tongyi(client=Generation(), model_name="qwen-turbo")

    return llm
