from PIL import Image
import io
from pathlib import Path
from nonebot.log import logger
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from .get_weather import get_weather
from nonebot import on_command, require
from nonebot.rule import to_me
from nonebot.params import CommandArg, ArgPlainText
from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from .config import XjieVariable, AMAP_KEY, QWEATHER_KEY, QWEATHER_APITYPE
from .file_handle import xj_file_handle
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

xj_file_handle = xj_file_handle()

apikey = {
    'AMAP_KEY': AMAP_KEY,
    'QWEATHER_KEY': QWEATHER_KEY
}
key_json_data = xj_file_handle.xj_file_reading("xjie_data.json")
for key in apikey:
    if key_json_data[str(key)] == '':
        xj_file_handle.xj_file_change("xjie_data.json", key, apikey[key])

if QWEATHER_APITYPE in [0, 1]:
    xj_file_handle.xj_file_change("xjie_data.json", 'QWEATHER_APITYPE', QWEATHER_APITYPE)
else:
    logger.warning("\033[31m请检查配置文件.env中的QWEATHER_APITYPE是否正确\033[0m")

setup_function_list = ['配置key', '设置优先平台']

get_weather = get_weather()

xj_weather = on_command("天气", rule=to_me(), priority=10, block=True)


def img_byte_arr():
    img = Image.open(Path(__file__).parent / "weatherforecast.png")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()


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

    if XjieVariable._get_default_platform["mr"] != '':
        bot_result = await get_weather.xj_get_weather_main(xj_user_message, XjieVariable._get_default_platform["mr"])
        if bot_result == '200':
            await UniMessage.image(raw=img_byte_arr()).send()
        elif isinstance(bot_result, list):
            if bot_result[0] == "error":
                await xj_weather.finish(bot_result[1])
    else:
        bot_result = await get_weather.xj_get_weather_main(xj_user_message)
        if bot_result == '200':
            await UniMessage.image(raw=img_byte_arr()).send()
        elif isinstance(bot_result, list):
            if bot_result[0] == "error":
                await xj_weather.finish(bot_result[1])
