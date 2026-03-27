import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from devmate.agents.agent import DevMateAgent
from devmate.utils.logger import logger


async def test_skill_tool():
    logger.info("开始测试技能工具调用")
    
    agent = DevMateAgent()
    
    # 测试用例
    test_cases = [
        "我想创建一个 FastAPI 服务，请使用相关技能",
        "帮我创建一个 Python 项目，使用技能来完成"
    ]
    
    for query in test_cases:
        logger.info(f"测试查询: {query}")
        
        try:
            result = await agent.run(query)
            logger.info(f"Agent 响应: {result}")
        except Exception as e:
            logger.error(f"测试失败: {e}")
        
        logger.info("-" * 80)


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_skill_tool())
