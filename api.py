import httpx
from astrbot.api import logger

class Media302Api:
    def __init__(self, config: dict):
        self.base_url = config.get('media302_url')
        self.folder = config.get('folder', '转存监控')
        self.token = config.get('media302_token')
        
    async def save_share(self, url: str) -> dict:
        """保存115分享链接"""
        if not all([self.base_url, self.token]):
            logger.error("media302配置不完整")
            return {"success": False, "message": "插件配置不完整"}
            
        if not url.startswith(("https://115.com", "https://115cdn.com")):
            return {"success": False, "message": "无效的115分享链接"}
            
        try:
            api_url = f"{self.base_url.rstrip('/')}/strm/api/task/save-share"
            params = {"folder": self.folder, "token": self.token, "url": url}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(api_url, params=params, timeout=30)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            error_msg = f"请求失败: {str(e)}" if isinstance(e, httpx.RequestError) else \
                      f"HTTP错误: {e.response.status_code}" if isinstance(e, httpx.HTTPStatusError) else \
                      f"响应解析失败: {str(e)}" if isinstance(e, ValueError) else \
                      f"未知错误: {str(e)}"
            logger.error(error_msg, exc_info=not isinstance(e, (httpx.RequestError, httpx.HTTPStatusError, ValueError)))
            return {"success": False, "message": error_msg}