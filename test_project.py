from src.devmate.utils.config import config
from src.devmate.utils.logger import logger

# 测试配置加载
logger.info("测试配置加载...")
logger.info(f"模型配置: {config.model}")
logger.info(f"搜索配置: {config.search}")
logger.info(f"LangSmith 配置: {config.langsmith}")
logger.info(f"Skills 配置: {config.skills}")

logger.info("项目结构测试完成")
