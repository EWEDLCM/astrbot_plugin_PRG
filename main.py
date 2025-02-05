from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

@register("sign_in", "签到", "回复签到成功。", "1.0")
class SignInPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.context = context
        self.config = config

    @filter.command("签到")
    async def sign_in(self, event: AstrMessageEvent):
        user_id = event.sender.id # 获取用户ID
        # 在这里你可以添加更复杂的逻辑，比如记录签到时间，判断是否已经签到等等
        # 例如，你可以使用 self.context.database 来存储用户签到信息。
        yield event.plain_result(f"\n签到成功！ 用户ID: {user_id}")
