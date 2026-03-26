from langchain.tools import tool
from ..mcp.client import mcp_client
from ..rag.retriever import retriever
from ..utils.logger import logger

@tool
async def search_web(query: str) -> str:
    """搜索网络获取最新信息
    
    Args:
        query: 搜索查询字符串
    
    Returns:
        搜索结果的文本摘要
    """
    try:
        response = await mcp_client.search_web(query)
        results = response.results
        if not results:
            return "未找到相关信息"
        
        # 格式化搜索结果
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. {result.title}\n"  
                f"URL: {result.url}\n"  
                f"内容: {result.content[:300]}...\n"
            )
        
        return "\n".join(formatted_results)
    except Exception as e:
        logger.error(f"搜索工具执行失败: {e}")
        return f"搜索失败: {str(e)}"

@tool
async def search_knowledge_base(query: str) -> str:
    """搜索本地知识库获取相关信息
    
    Args:
        query: 搜索查询字符串
    
    Returns:
        知识库中相关文档的内容摘要
    """
    try:
        results = retriever.search_knowledge_base(query)
        if not results:
            return "知识库中未找到相关信息"
        
        # 格式化检索结果
        formatted_results = []
        for i, doc in enumerate(results, 1):
            formatted_results.append(
                f"{i}. 来源: {doc.metadata.get('source', '未知')}\n"  
                f"内容: {doc.page_content[:300]}...\n"
            )
        
        return "\n".join(formatted_results)
    except Exception as e:
        logger.error(f"知识库搜索工具执行失败: {e}")
        return f"知识库搜索失败: {str(e)}"
