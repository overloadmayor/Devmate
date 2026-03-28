from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from langchain_tavily import TavilySearch

from ..utils.config import config
from ..utils.logger import logger


app = FastAPI()

class SearchRequest(BaseModel):
    query: str
    max_results: int = 5
    topic: str = "general"
    search_depth: str = "basic"
    time_range: str | None = None
    include_images: bool = False
    include_domains: list[str] | None = None
    exclude_domains: list[str] | None = None
    start_date: str | None = None
    end_date: str | None = None

class SearchResult(BaseModel):
    title: str
    url: str
    content: str

class SearchResponse(BaseModel):
    results: list[SearchResult]

tavily_client = None

@app.on_event("startup")
def startup_event():
    global tavily_client
    try:
        tavily_api_key = config.search.get("tavily_api_key")
        if not tavily_api_key:
            logger.error("Tavily API key 未配置")
            return
        tavily_client = TavilySearch(
            max_results=5,
            topic="general",
            search_depth="basic"
        )
        logger.info("Tavily 客户端初始化成功")
    except Exception as e:
        logger.error(f"Tavily 客户端初始化失败: {e}")

@app.post("/search")
async def search_web(request: SearchRequest):
    try:
        if not tavily_client:
            raise HTTPException(status_code=500, detail="Tavily 客户端未初始化")
        
        invoke_params = {
            "query": request.query,
            "topic": request.topic,
            "search_depth": request.search_depth,
            "time_range": request.time_range,
            "include_images": request.include_images,
            "include_domains": request.include_domains,
            "exclude_domains": request.exclude_domains,
            "start_date": request.start_date,
            "end_date": request.end_date
        }
        
        # 过滤掉None值
        invoke_params = {k: v for k, v in invoke_params.items() if v is not None}
        
        results = tavily_client.invoke(invoke_params)
        
        formatted_results = []
        for result in results.get("results", []):
            formatted_results.append(SearchResult(
                title=result.get("title", ""),
                url=result.get("url", ""),
                content=result.get("content", "")
            ))
        
        logger.info(f"搜索完成: {request.query}")
        return SearchResponse(results=formatted_results)
    except Exception as e:
        logger.error(f"搜索失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
