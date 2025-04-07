from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from .api import Media302Api
from astrbot.api import logger

@register("Media302Save", "Qoo", "media302转存插件", "1.0.0")
class Media302SavePlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.api = Media302Api(config)
        if not all([self.api.base_url, self.api.token]):
            logger.error("media302插件配置不完整")

    @filter.command("115")
    async def handle_media_save(self, event: AstrMessageEvent, message: str):
        '''media302转存指令'''
        url = message.strip()
        if not url or not any(d in url for d in ("115.com/s/", "115cdn.com/s/")):
            yield event.plain_result("请输入有效的115网盘分享链接，格式如：https://115.com/s/xxxxx")
            return
            
        try:
            result = await self.api.save_share(url)
            if result.get('msg') in ('success', '文件已接收，无需重复接收！'):
                yield event.plain_result(f"✅ 转存成功！\n状态：{result.get('msg')}")
            else:
                error_msg = result.get('msg', '未知错误')
                logger.error(f"转存失败: {error_msg}")
                yield event.plain_result(f"❌ 转存失败：{error_msg}")
                
        except Exception as e:
            logger.error(f"处理请求时发生错误: {str(e)}", exc_info=True)
            yield event.plain_result(f"⚠️ 处理请求时发生错误: {str(e)}")
