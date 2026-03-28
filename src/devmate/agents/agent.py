from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import trim_messages
from ..utils.llm import get_llm
from ..tools.tools import (
    search_web,
    search_knowledge_base,
    get_weather,
    load_skill,
    write_file,
    read_file,
    list_directory,
    delete_file
)
from ..utils.logger import logger
from ..utils.config import config
from .prompts import SYSTEM_PROMPT
from ..skills.manager import skills_manager


class DevMateAgent:
    def __init__(self):
        self.llm = get_llm()
        self.tools = [
            search_web,
            search_knowledge_base,
            get_weather,
            load_skill,
            write_file,
            read_file,
            list_directory,
            delete_file
        ]
        # 初始化内存检查点存储器
        self.checkpointer = InMemorySaver()
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """创建可执行的 Agent"""
        try:
            skills_prompt = skills_manager.get_skills_prompt()
            
            # 从现有的 SYSTEM_PROMPT 中获取系统消息的模板
            system_message = SYSTEM_PROMPT.messages[0]
            base_system_prompt = system_message.prompt.template
            
            # 如果有技能提示词，需要将其添加到系统提示词中
            if skills_prompt:
                enhanced_system_prompt = base_system_prompt + "\n\n" + skills_prompt
            else:
                enhanced_system_prompt = base_system_prompt
            
            # ====================
            # 使用 LangChain 1.2.13 的 create_agent
            # ====================
            agent = create_agent(
                model=self.llm,
                tools=self.tools,
                system_prompt=enhanced_system_prompt,
                checkpointer=self.checkpointer,
                debug=False
            )
            
            logger.info("Agent 初始化成功")
            return agent
        
        except Exception as e:
            logger.error(f"Agent 初始化失败: {e}")
            raise
    
    async def run(self, query: str, thread_id: str = "default") -> str:
        """运行 Agent
        
        Args:
            query: 用户输入的查询
            thread_id: 线程 ID，用于区分不同的对话会话
        """
        try:
            # 使用消息修剪策略来总结旧消息
            # 保留最后 10 条消息，token 限制为 60000
            trim_strategy = trim_messages(
                strategy="last",
                max_tokens=60000,
                token_counter=len,
                include=["user", "ai", "system", "tool"],
                allow_partial=False,
                start_on="user",
            )
            
            # 使用新的 StateGraph API，并传入 thread_id
            result = await self.agent.ainvoke(
                {"messages": [{"role": "user", "content": query}]},
                {"configurable": {"thread_id": thread_id}}
            )
            
            # 从结果中提取最后的 AI 消息
            messages = result.get("messages", [])
            if messages:
                # 返回最后一条消息的内容
                last_message = messages[-1]
                if hasattr(last_message, 'content'):
                    return last_message.content
                else:
                    return str(last_message)
            return "未获取到结果"
        except Exception as e:
            logger.error(f"Agent 运行失败: {e}")
            return f"运行失败: {str(e)}"


# 创建全局 agent 实例
agent = DevMateAgent()
