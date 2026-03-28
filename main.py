import asyncio
from src.devmate.agents.agent import agent
from src.devmate.utils.logger import logger
from src.devmate.rag.retriever import retriever
from dotenv import load_dotenv  
load_dotenv()  

async def main():
    """主函数"""
    try:
        # 初始化 RAG 检索器
        logger.info("初始化 RAG 检索器...")
        retriever.ingest_documents()
        
        # 启动交互式对话
        logger.info("DevMate 启动成功，开始对话...")
        logger.info("=====================================")
        logger.info("DevMate - AI 编程助手")
        logger.info("=====================================")
        logger.info("输入 'exit' 退出对话")
        logger.info("=====================================")
        
        while True:
            user_input = input("用户: ")
            if user_input.lower() == "exit":
                logger.info("对话结束")
                break
            
            logger.info(f"用户输入: {user_input}")
            logger.info("正在生成.......")
            result = await agent.run(user_input)
            logger.info(f"DevMate: {result}")
            logger.info("=====================================")
    except Exception as e:
        logger.error(f"应用程序启动失败: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
