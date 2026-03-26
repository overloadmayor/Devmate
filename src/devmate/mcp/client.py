import httpx
from pydantic import BaseModel
from ..utils.logger import logger

class SearchRequest(BaseModel):
    query: str
    max_results: int = 5

class SearchResult(BaseModel):
    title: str
    url: str
    content: str

class SearchResponse(BaseModel):
    results: list[SearchResult]

class MCPClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    async def search_web(self, query: str, max_results: int = 5):
        """通过 MCP Server 搜索网络"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/search",
                    json={"query": query, "max_results": max_results}
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
