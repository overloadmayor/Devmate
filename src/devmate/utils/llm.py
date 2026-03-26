from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from .config import config
from .logger import logger

def get_llm():
    """获取 LLM 实例"""
    try:
        model_config = config.model
        llm = ChatOpenAI(
            base_url=model_config.get("ai_base_url"),
            api_key=model_config.get("api_key"),
            model=model_config.get("model_name"),
            temperature=0.7
        )
        logger.info(f"LLM 初始化成功: {model_config.get('model_name')}")
        return llm
    except Exception as e:
        logger.error(f"LLM 初始化失败: {e}")
        raise

def get_embeddings():
    """获取 Embedding 实例"""
    try:
        embedding_config = config.embedding
        embeddings = OpenAIEmbeddings(
            base_url=embedding_config.get("ai_base_url"),
            api_key=embedding_config.get("api_key"),
            model=embedding_config.get("model_name")
        )
        logger.info(f"Embedding 初始化成功: {embedding_config.get('model_name')}")
        return embeddings
    except Exception as e:
        logger.error(f"Embedding 初始化失败: {e}")
        raise
