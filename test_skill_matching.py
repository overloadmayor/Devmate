import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from devmate.agents.agent import DevMateAgent
from devmate.utils.logger import logger


async def test_skill_matching():
    logger.info("开始测试技能匹配逻辑")
    
    agent = DevMateAgent()
    
    # 测试用例
    test_cases = [
        "我想创建一个 FastAPI 服务",
        "帮我创建一个 Python 项目",
        "我需要一个 FastAPI 应用",
        "创建一个新的 Python 项目结构"
    ]
    
    for query in test_cases:
        logger.info(f"测试查询: {query}")
        # 这里我们只测试匹配逻辑，不实际调用模型
        
        # 模拟 agent.run 中的技能匹配逻辑
        from devmate.skills.manager import skills_manager
        matched_skill = None
        
        for skill_name in skills_manager.list_skills():
            skill = skills_manager.get_skill(skill_name)
            if not skill:
                continue
            
            # 检查技能名称是否在查询中
            if skill_name in query.lower():
                matched_skill = skill
                break
            
            # 检查技能名称中的关键词是否在查询中
            skill_keywords = skill_name.split('_')
            for keyword in skill_keywords:
                if keyword and keyword in query.lower():
                    matched_skill = skill
                    break
            if matched_skill:
                break
            
            # 检查技能描述是否与查询相关
            if skill.description and any(keyword in skill.description.lower() for keyword in query.lower().split()):
                matched_skill = skill
                break
        
        if matched_skill:
            logger.info(f"匹配到技能: {matched_skill.name} - {matched_skill.description}")
        else:
            logger.info("未匹配到技能")
        
        logger.info("-" * 50)


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_skill_matching())
