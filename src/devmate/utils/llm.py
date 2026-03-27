from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.embeddings import Embeddings
import requests
from .config import config
from .logger import logger

class DashscopeEmbeddings(Embeddings):
    """Dashscope Embeddings implementation"""
    def __init__(self, base_url, api_key, model_name):
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model_name
    
    def embed_documents(self, texts):
        """Embed multiple documents"""
        try:
            # Ensure texts is a list of strings
            if not isinstance(texts, list):
                texts = [texts]
            
            # Dashscope API requires input in a specific format
            response = requests.post(
                self.base_url + "/embeddings",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                json={
                    "model": self.model_name,
                    "input": texts
                }
            )
            
            response.raise_for_status()
            result = response.json()
            return [item["embedding"] for item in result["data"]]
        except Exception as e:
            logger.error(f"Error embedding documents: {e}")
            raise
    
    def embed_query(self, text):
        """Embed a single query"""
        return self.embed_documents([text])[0]

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
        # Use custom DashscopeEmbeddings for Dashscope API
        if "dashscope" in embedding_config.get("ai_base_url", "").lower():
            embeddings = DashscopeEmbeddings(
                base_url=embedding_config.get("ai_base_url"),
                api_key=embedding_config.get("api_key"),
                model_name=embedding_config.get("model_name")
            )
        else:
            # Use OpenAIEmbeddings for other APIs
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