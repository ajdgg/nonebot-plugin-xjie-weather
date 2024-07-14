from pathlib import Path
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from .get_weather import get_weather
from nonebot import on_command, require
from nonebot.rule import to_me
from nonebot.params import CommandArg, ArgPlainText
from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from .config import XjieVariable
from .setup import xj_setup

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import UniMessage

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-xjie-weather",
    description="一个小小的天气插件",
    usage="目前支持和风天气和高德地图的天气api",
    type="application",
    homepage="https://github.com/ajdgg/nonebot-plugin-xjie-weather",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
)

setup_function_list = ['配置key', '设置优先平台']

get_weather = get_weather()

xj_weather = on_command("天气", rule=to_me(), priority=10, block=True)


@xj_weather.handle()
async def bot_self_inspection():
    if not XjieVariable._get_default_platform["xjie_data"]:
        await xj_weather.finish("无配置api未配置")


@xj_weather.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("xj_user_message", args)


@xj_weather.got("xj_user_message", prompt="请输入地名")
async def got_location(xj_user_message: str = ArgPlainText()):
    path = Path(__file__).parent / "weatherforecast.png"
    if XjieVariable._get_default_platform["mr"] != '':
        bot_result = await get_weather.xj_get_weather_main(xj_user_message, XjieVariable._get_default_platform["mr"])
        if bot_result == '200':
            await UniMessage.image(path=path).send()
        elif isinstance(bot_result, list):
            if bot_result[0] == "error":
                await xj_weather.finish(bot_result[1])
    else:
        bot_result = await get_weather.xj_get_weather_main(xj_user_message)
        if bot_result == '200':
            await UniMessage.image(path=path).send()
        elif isinstance(bot_result, list):
            if bot_result[0] == "error":
                await xj_weather.finish(bot_result[1])
