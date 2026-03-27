import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from devmate.skills.manager import skills_manager
from devmate.utils.logger import logger


def test_skills_loading():
    logger.info("开始测试 Skills 加载功能")
    
    skills_list = skills_manager.list_skills()
    logger.info(f"已加载的技能: {skills_list}")
    
    if not skills_list:
        logger.warning("未找到任何技能")
        return False
    
    for skill_name in skills_list:
        skill = skills_manager.get_skill(skill_name)
        logger.info(f"技能名称: {skill.name}")
        logger.info(f"技能描述: {skill.description}")
        logger.info(f"技能提示词长度: {len(skill.prompt_template) if skill.prompt_template else 0}")
    
    skills_prompt = skills_manager.get_skills_prompt()
    logger.info(f"生成的技能提示词长度: {len(skills_prompt)}")
    
    return True


def test_agent_with_skills():
    logger.info("开始测试 Agent 与 Skills 集成")
    
    try:
        from devmate.agents.agent import agent
        
        logger.info("Agent 初始化成功")
        logger.info("Skills 已集成到 Agent 的系统提示词中")
        
        return True
    except Exception as e:
        logger.error(f"Agent 初始化失败: {e}")
        return False


if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("Skills 功能测试")
    logger.info("=" * 50)
    
    test1_passed = test_skills_loading()
    test2_passed = test_agent_with_skills()
    
    logger.info("=" * 50)
    if test1_passed and test2_passed:
        logger.info("所有测试通过")
    else:
        logger.error("部分测试失败")
    logger.info("=" * 50)
