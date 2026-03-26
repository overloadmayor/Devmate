import httpx
from pydantic import BaseModel
from ..utils.logger import logger

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

class MCPClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    async def search_web(
        self, 
        query: str, 
        max_results: int = 5,
        topic: str = "general",
        search_depth: str = "basic",
        time_range: str | None = None,
        include_images: bool = False,
        include_domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
        start_date: str | None = None,
        end_date: str | None = None
    ):
        """通过 MCP Server 搜索网络"""
        try:
            async with httpx.AsyncClient() as client:
                request_data = {
                    "query": query,
                    "max_results": max_results,
                    "topic": topic,
                    "search_depth": search_depth,
                    "time_range": time_range,
                    "include_images": include_images,
                    "include_domains": include_domains,
                    "exclude_domains": exclude_domains,
                    "start_date": start_date,
                    "end_date": end_date
                }
                
                # 过滤掉None值
                request_data = {k: v for k, v in request_data.items() if v is not None}
                
                response = await client.post(
                    f"{self.base_url}/search",
                    json=request_data
                )
                response.raise_for_status()
                
                data = response.json()
                search_response = SearchResponse(**data)
                logger.info(f"MCP 搜索成功: {query}")
                return search_response
        except Exception as e:
            logger.error(f"MCP 搜索失败: {e}")
            return SearchResponse(results=[])

mcp_client = MCPClient()
