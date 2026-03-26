from langchain.agents import create_agent
from ..utils.llm import get_llm
from ..tools.tools import search_web, search_knowledge_base
from ..utils.logger import logger
from ..utils.config import config

class DevMateAgent:
    def __init__(self):
        self.llm = get_llm()
        self.tools = [search_web, search_knowledge_base]
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """创建 Agent"""
        try:
            # 创建 Agent
            agent = create_agent(
                self.llm,
                self.tools
            )
            
            logger.info("Agent 初始化成功")
            return agent
        except Exception as e:
            logger.error(f"Agent 初始化失败: {e}")
            raise
    
    async def run(self, query: str) -> str:
        """运行 Agent 处理用户查询"""
        try:
            result = await self.agent.ainvoke({"messages": [{"role": "user", "content": query}]})
            logger.info(f"Agent 执行完成: {query}")
            return result.get("output", "")
        except Exception as e:
            logger.error(f"Agent 执行失败: {e}")
            return f"执行失败: {str(e)}"

agent = DevMateAgent()