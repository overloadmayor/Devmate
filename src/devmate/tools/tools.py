from langchain.tools import tool
from ..mcp.client import mcp_client
from ..rag.retriever import retriever
from ..utils.logger import logger
from langchain_tavily import TavilySearch
from ..skills.manager import skills_manager
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

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


@tool
def load_skill(skill_name: str) -> str:
    """Load a specialized skill prompt.

    Available skills:
    - create-fastapi-service: 创建 FastAPI 服务的基础结构和文件，包括 main.py、requirements.txt 等必要文件
    - create-python-project: 创建 Python 项目的基础结构和配置文件，包括 src/、tests/、docs/ 等目录

    Returns: skill's prompt and context.
    """
    skill = skills_manager.get_skill(skill_name)
    if not skill:
        return f"技能 {skill_name} 不存在"
    
    if not skill.prompt_template:
        return f"技能 {skill_name} 没有提示词模板"
    
    return f"## {skill.name}\n{skill.description}\n\n{skill.prompt_template}"
