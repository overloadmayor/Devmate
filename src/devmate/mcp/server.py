from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from tavily import TavilyClient
from ..utils.config import config
from ..utils.logger import logger

app = FastAPI()

class SearchRequest(BaseModel):
    query: str
    max_results: int = 5

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
        tavily_client = TavilyClient(api_key=tavily_api_key)
        logger.info("Tavily 客户端初始化成功")
    except Exception as e:
        logger.error(f"Tavily 客户端初始化失败: {e}")

@app.post("/search")
async def search_web(request: SearchRequest):
    try:
        if not tavily_client:
            raise HTTPException(status_code=500, detail="Tavily 客户端未初始化")
        
        results = tavily_client.search(
            query=request.query,
            max_results=request.max_results,
            search_depth="basic"
        )
        
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
