import asyncio
from pathlib import Path
from typing import List
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from .file_handle import xj_file_handle
from .get_weather import get_weather
from nonebot import on_command, on_message, get_bot, require
from nonebot.rule import to_me
from nonebot.params import CommandArg, ArgPlainText
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

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

_time_a = {}
_get_default_platform = {}
_configuration_state = {}
_configuration_option = {}
_admin_whitelist = []

_configuration_option["ground-floor"] = True
_configuration_option["SG"] = False
_configuration_option["SF"] = False

xj_yes = ['是', 'y', 'yes', 'Y', 'YES', 'YeS', 'YEs', 'YeS']
xj_no = ['否', 'n', 'no', 'N', 'NO', 'No', 'nO', 'N0']

dz = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

setup_function_list = ['配置key', '设置优先平台']

get_weather = get_weather()
xj_file_handle = xj_file_handle()
_get_default_platform["xjie_data"] = xj_file_handle.get_keys_ending_with_key("xjie_data.json")
_get_default_platform["mr"] = xj_file_handle.xj_file_reading("xjie_data.json", "default_api")


def menu_dispose(list: List[str]) -> str:
    """
    将一个字符串列表转换为带有索引的菜单格式字符串。

    参数:
        list (List[str]): 包含菜单项的字符串列表。

    返回:
        str: 格式化后的菜单字符串，每一行包含一个索引和对应的菜单项。

    示例:
        如果输入的list为 ["Option1", "Option2"]，则输出为：
        "[1] Option1
        [2] Option2"
    """
    return "\n".join(f"[{i}] {func}" for i, func in enumerate(setup_function_list, start=1))


def is_integer_not_float(s: str) -> bool:
    """
    判断给定的字符串是否能被解析为一个整数。

    参数:
        s (str): 要检查的字符串。

    返回:
        bool: 如果字符串可以被解析为整数，则返回True；否则返回False。
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def original(user_id):
    del _configuration_state[user_id]
    del _configuration_option["option"]
    del _configuration_option["SL"]
    del _configuration_option["X_KEY"]
    _configuration_option["SG"] = False
    _configuration_option["SF"] = False


async def timeout_task(user_id):
    await asyncio.sleep(300)
    bot = get_bot()
    if _time_a["t"]:
        original(user_id)
        message = "您的操作已超时，会话 已结束。"
        await bot.send_private_msg(user_id=user_id, message=message)

administrator = xj_file_handle.xj_file_reading("xjie_data.json", "admin_whitelist")
if administrator != "":
    _admin_whitelist = [int(num) for num in administrator.split(",")]


xj_setup = on_command("setup", aliases={"k"}, rule=to_me(), priority=10, block=True)


@xj_setup.handle()
async def setup_handle(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()):
    ids = event.get_session_id()
    user_id = event.get_user_id()
    if ids.startswith("group"):
        await xj_setup.finish("请使用使用有管理员权限的账号私聊bot进行设置")
    elif _admin_whitelist == []:
        _configuration_state[user_id] = "enter_configuration_mode"
        _configuration_option["option"] = "set_administrator"
        await xj_setup.send("无配置管理员是否配置管理员，在配置完成后需要管理员才能额外添加新的管理员y/n")
    elif int(user_id) in _admin_whitelist or user_id in _admin_whitelist:
        if xj_user_configuration := args .extract_plain_text():
            print(xj_user_configuration)
            await xj_setup.finish("优先天气")
        else:
            ids = event.get_session_id()
            _configuration_state[user_id] = "enter_configuration_mode"
            _configuration_option["option"] = "setting_list"
            _time_a["t"] = True
            asyncio.create_task(timeout_task(user_id))
            await xj_setup.finish(f'选择\n{menu_dispose(setup_function_list)}')
    else:
        await xj_setup.finish("无管理员权限")

xj_setup_responsive = on_message(rule=lambda event: isinstance(event, Event) and _configuration_state.get(event.get_user_id(), "") == "enter_configuration_mode", priority=5)


@xj_setup_responsive.handle()
async def configuration_responsive(bot: Bot, event: Event):
    user_id = event.get_user_id()
    args = str(event.get_message()).strip()
    if args == "退出":
        await xj_setup_responsive.send("退出成功")
        original(user_id)
    if _configuration_option["option"] == "set_administrator":
        async def update_admin_list(user_id, confirm):
            if confirm:
                _admin_whitelist.append(user_id)
                admin_string = ",".join(map(str, _admin_whitelist))
                try:
                    xj_file_handle.xj_file_change("xjie_data.json", "admin_whitelist", admin_string)

                    await xj_setup_responsive.send("设置成功")

                    del _configuration_state[user_id]
                    del _configuration_option["option"]
                    _time_a["t"] = False
                except Exception as e:
                    await xj_setup_responsive.send(f"设置失败：{e}")
            else:
                del _configuration_state[user_id]
                del _configuration_option["option"]
                _time_a["t"] = False
                await xj_setup_responsive.finish("已取消管理员配置")

        if args in xj_yes:
            await update_admin_list(user_id, True)
        elif args in xj_no:
            await update_admin_list(user_id, False)
        else:
            await xj_setup_responsive.finish("请输入y/n")

    elif _configuration_option["option"] == "setting_list":

        if _configuration_option["ground-floor"] and is_integer_not_float(args):

            try:
                args = dz[int(args)]
                print(args)
            except IndexError:
                await xj_setup_responsive.finish("输入错误，请重新输入")

        keydata = xj_file_handle.xj_file_reading("xjie_data.json")
        keys_ending_with_KEY = [k for k in keydata.keys() if k.endswith("_KEY")]

        if args == 'one' or _configuration_option.get("SL", '') == '1':

            _configuration_option["ground-floor"] = False
            _configuration_option["SL"] = "1"

            if _configuration_option["SG"]:

                if _configuration_option["SF"]:

                    x_data = _configuration_option["X_KEY"]
                    xj_file_handle.xj_file_change("xjie_data.json", x_data, args)
                    await xj_setup_responsive.send("配置成功")
                    _get_default_platform["xjie_data"] = xj_file_handle.get_keys_ending_with_key("xjie_data.json")

                    _time_a["t"] = False
                    _configuration_option["ground-floor"] = True
                    _configuration_option["SG"] = False
                    del _configuration_state[user_id]
                    del _configuration_option["SL"]
                    del _configuration_option["option"]

                else:

                    if is_integer_not_float(args):

                        try:
                            a_data = keys_ending_with_KEY[int(args) - 1]
                        except IndexError:
                            print(f"索引 {int(args)} 无效，列表长度为 {len(keys_ending_with_KEY)}")
                            await xj_setup_responsive.finish("输入错误，请重新输入")

                        await xj_setup_responsive.send(f"请输入{a_data}的key")

                        _configuration_option["X_KEY"] = a_data
                        _configuration_option["SF"] = True
                    else:
                        await xj_setup_responsive.send("输入错误")
            else:
                await xj_setup_responsive.send(f"请选择要设置的key\n{menu_dispose(keys_ending_with_KEY)}")

                _configuration_option["SG"] = True
        elif args == 'two' or _configuration_option.get("SL", '') == '2':

            _configuration_option["ground-floor"] = False
            _configuration_option["SL"] = "2"

            if _configuration_option["SG"]:
                if is_integer_not_float(args):

                    try:
                        x_data = keys_ending_with_KEY[int(args) - 1]
                    except IndexError:
                        await xj_setup_responsive.finish("输入错误，请重新输入")

                    xj_file_handle.xj_file_change("xjie_data.json", "default_api", x_data)
                    await xj_setup_responsive.send(f"默认天气平台已切换为{x_data}")

                    _configuration_option["ground-floor"] = True
                    _configuration_option["SG"] = False
                    del _configuration_state[user_id]
                    del _configuration_option["SL"]
                    del _configuration_option["option"]
                else:
                    await xj_setup_responsive.send("输入错误")
            else:
                await xj_setup_responsive.send(f"请选择要设置的key\n{menu_dispose(keys_ending_with_KEY)}")

                _configuration_option["SG"] = True
        else:
            await xj_setup_responsive.finish("输入错误")

xj_weather = on_command("天气", rule=to_me(), priority=10, block=True)


@xj_weather.handle()
async def bot_self_inspection():
    if not _get_default_platform["xjie_data"]:
        await xj_weather.finish("无配置api未配置")


@xj_weather.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("xj_user_message", args)


@xj_weather.got("xj_user_message", prompt="请输入地名")
async def got_location(xj_user_message: str = ArgPlainText()):
    path = Path(__file__).parent / "weatherforecast.png"
    if _get_default_platform["mr"] != '':
        bot_result = await get_weather.xj_get_weather_main(xj_user_message, _get_default_platform["mr"])
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
