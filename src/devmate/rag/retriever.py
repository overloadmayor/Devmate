from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..utils.config import config
from ..utils.logger import logger
from ..utils.llm import get_embeddings

class RAGRetriever:
    def __init__(self, persist_directory="./vector_db"):
        self.persist_directory = persist_directory
        self.embeddings = get_embeddings()
        self.vector_store = None
    
    def ingest_documents(self, docs_dir="./docs"):
        """摄入文档到向量数据库"""
        try:
            # 加载文档
            loader = DirectoryLoader(
                docs_dir,
                glob="*.md",
                loader_cls=TextLoader
            )
            documents = loader.load()
            logger.info(f"加载了 {len(documents)} 个文档")
            
            # 切分文档
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            splits = text_splitter.split_documents(documents)
            logger.info(f"文档切分为 {len(splits)} 个片段")
            
            # 创建向量存储
            self.vector_store = Chroma.from_documents(
                documents=splits,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            logger.info("文档摄入完成")
        except Exception as e:
            logger.error(f"文档摄入失败: {e}")
            raise
    
    def search_knowledge_base(self, query, k=3):
        """搜索知识库"""
        if not self.vector_store:
            # 如果向量存储未初始化，尝试加载
            try:
                self.vector_store = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
            except Exception as e:
                logger.error(f"加载向量存储失败: {e}")
                return []
        
        try:
            results = self.vector_store.similarity_search(query, k=k)
            logger.info(f"搜索到 {len(results)} 个相关文档")
            return results
        except Exception as e:
            logger.error(f"搜索知识库失败: {e}")
            return []

retriever = RAGRetriever()
