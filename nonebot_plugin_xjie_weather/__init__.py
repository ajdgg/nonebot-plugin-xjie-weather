'''
coding: UTF-8
Author: AwAjie
Date: 2024-07-05 16:26:29
'''
from PIL import Image
import io
from pathlib import Path
from typing import List
from nonebot.log import logger
from nonebot.adapters import Message, Bot, Event
from nonebot.matcher import Matcher
from .get_weather import get_weather
from nonebot import on_command, require, on_message
from nonebot.rule import to_me
from nonebot.params import CommandArg, ArgPlainText
from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from .config import XjieVariable, AMAP_KEY, QWEATHER_KEY, QWEATHER_APITYPE
from .file_handle import xj_file_handle
from .data_utilities import l_list, menu_dispose
from .setup import xj_setup

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import UniMessage

from .xjie_db import DatabaseManager
dblg = DatabaseManager()

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

if QWEATHER_APITYPE is not None:
    if QWEATHER_APITYPE in [0, 1]:
        xj_file_handle.xj_file_change("xjie_data.json", 'QWEATHER_APITYPE', QWEATHER_APITYPE)
    else:
        logger.warning("如果您有在.env配置和风天气的QWEATHER_APITYPE因而触发此提示，请检查配置文件.env中的QWEATHER_APITYPE是否正确，当然您也可以无视此提示，这将使用默认值，您可以使用插件内设置功能进行设置。")


setup_function_list = ['配置key', '设置优先平台']

get_weather = get_weather()

_special_position_temporary_storage = {}

xj_weather = on_command("天气", rule=to_me(), priority=10, block=True)


def get_the_default_platform():
    """
    获取默认平台
    Get the default platform

    返回:
        list: [default_platform, default_api]
    """
    key_data = xj_file_handle.get_keys_ending_with_key("xjie_data.json")
    a = list(key_data.items())
    first_key, first_value = a[0]
    return [first_key, first_value]


def split_string_by_hash(input_string: str):
    if '#' in input_string:
        parts = input_string.split('#')
        parts = [part for part in parts if part]
        return parts
    else:
        return input_string


@xj_weather.handle()
async def bot_self_inspection():
    if not XjieVariable._get_default_platform["xjie_data"]:
        await xj_weather.finish("无配置api未配置")


@xj_weather.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("xj_user_message", args)


@xj_weather.got("xj_user_message", prompt="请输入地名")
async def got_location(event: Event, xj_user_message: str = ArgPlainText()):
    #
    # get_weather.xj_get_weather_main返回 [状态类型， 数据内容]
    # 进入重复选择的信息类型 ["Selective_area", 平台名称, 平台key, 重复的数据数组]
    # #

    user_id = event.get_user_id()

    #
    # 有设置默认api
    # #
    if XjieVariable._get_default_platform["mr"][0] != '':
        bot_result = await get_weather.xj_get_weather_main(
            split_string_by_hash(xj_user_message),
            [
                XjieVariable._get_default_platform["mr"][0],
                XjieVariable._get_default_platform["mr"][1],
            ],
        )
        if bot_result[0] == '200':
            await UniMessage.image(raw=bot_result[1]).send()
        elif bot_result[0] == "error":
            await xj_weather.finish(bot_result[1])
        elif bot_result[0] == "multi_area":
            _special_position_temporary_storage[user_id] = [
                "Selective_area",
                bot_result[1],
                XjieVariable._get_default_platform["mr"][1],
                bot_result[2]
            ]
            await xj_weather.send(menu_dispose(l_list(bot_result[1])))
        elif bot_result[0] == "multi_area_app":
            if bot_result[1] == "AMAP_KEY":
                _special_position_temporary_storage[user_id] = [
                    "Selective_area",
                    bot_result[1],
                    XjieVariable._get_default_platform["mr"][1],
                    [
                        {"formatted_address": item["formatted_address"], "adcode": item["adcode"]}
                        for item in bot_result[3]
                    ],
                ]
                await xj_weather.send(menu_dispose([item["formatted_address"] for item in bot_result[3]]))

    #
    # 无默认api
    # #
    else:
        bot_result = await get_weather.xj_get_weather_main(split_string_by_hash(xj_user_message), get_the_default_platform())
        if bot_result[0] == '200':
            await UniMessage.image(raw=bot_result[1]).send()
        elif bot_result[0] == "error":
            await xj_weather.finish(bot_result[1])
        elif bot_result[0] == "multi_area":
            _special_position_temporary_storage[user_id] = [
                "Selective_area",
                bot_result[1],
                XjieVariable._get_default_platform["mr"][1],
                bot_result[2]
            ]
            await xj_weather.send(menu_dispose(l_list(bot_result[1])))
        elif bot_result[0] == "multi_area_app":
            if bot_result[1] == "AMAP_KEY":
                print("asdddd")
                _special_position_temporary_storage[user_id] = [
                    "Selective_area",
                    bot_result[1],
                    XjieVariable._get_default_platform["mr"][1],
                    [
                        {"formatted_address": item["formatted_address"], "adcode": item["adcode"]}
                        for item in bot_result[3]
                    ],
                ]
                await xj_weather.send(menu_dispose([item["formatted_address"] for item in bot_result[3]]))


special_position_temporary_storage_handle = on_message(rule=lambda event: isinstance(event, Event) and _special_position_temporary_storage.get(event.get_user_id(), [None])[0] == "Selective_area", priority=5)


@special_position_temporary_storage_handle.handle()
async def special_position_temporary_storage_handle_fun(event: Event):
    user_id = event.get_user_id()
    args = event.get_message().extract_plain_text()

    if args == "退出" or args == "t":
        await special_position_temporary_storage_handle.send("已退出")
        del _special_position_temporary_storage[user_id]

    # print(_special_position_temporary_storage[user_id][1][int(args) - 1])
    if _special_position_temporary_storage[user_id][1] == "AMAP_KEY":
        # print(
        #     [
        #         _special_position_temporary_storage[user_id][1],
        #         _special_position_temporary_storage[user_id][2],
        #         _special_position_temporary_storage[user_id][3][int(args) - 1].get(
        #             "formatted_address", None
        #         ),
        #         None,
        #         None,
        #         None,
        #         _special_position_temporary_storage[user_id][3][int(args) - 1].get(
        #             "adcode", None
        #         ),
        #     ]
        # )
        bot_result = await get_weather.xj_get_weather_p(
            [
                _special_position_temporary_storage[user_id][1],
                _special_position_temporary_storage[user_id][2],
                _special_position_temporary_storage[user_id][3][int(args) - 1].get(
                    "formatted_address", None
                ),
                None,
                None,
                None,
                _special_position_temporary_storage[user_id][3][int(args) - 1].get(
                    "adcode", None
                ),
            ]
        )

    # await special_position_temporary_storage_handle.send(_special_position_temporary_storage[user_id][1][int(args) - 1])
    if bot_result[0] == "200":
        await UniMessage.image(raw=bot_result[1]).send()
    del _special_position_temporary_storage[user_id]


lg = on_command("lg", rule=to_me(), priority=10, block=True)


@lg.handle()
async def lg_handle_first_receive(args: Message = CommandArg()):
    await lg.finish(str(dblg.city_lnglat(args.extract_plain_text())))
