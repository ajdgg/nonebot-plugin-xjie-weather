import asyncio
from nonebot import on_command, on_message, get_bot
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message, Bot, Event
from nonebot.typing import T_State
from .data_utilities import menu_dispose, is_integer_not_float
from .file_handle import xj_file_handle
from .config import XjieVariable
from nonebot.log import logger


xj_file_handle = xj_file_handle()

_time_a = {}
_configuration_state = {}
_configuration_option = {}

_configuration_option["ground-floor"] = True
_configuration_option["SG"] = True
_configuration_option["SF"] = True

xj_yes = ['是', 'y', 'yes', 'Y', 'YES', 'YeS', 'YEs', 'YeS']
xj_no = ['否', 'n', 'no', 'N', 'NO', 'No', 'nO', 'N0']

dz = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

qweather_kid_sub = ['QWEATHER_JWT_KID', 'QWEATHER_JWT_SUB']

setup_function_list = ['配置key', '设置优先平台', '和风天气订阅类型', '是否启用和风天气jwt验证', '是否启用本地数据库', '和风天气凭据ID和项目ID设置']
qweather_subscribe = ['免费订阅', '付费订阅']


def remove_if_exists(user_id):
    keys_to_remove = [user_id] + ["option", "SL", "X_KEY"]

    for key in keys_to_remove:
        if key in _configuration_state:
            del _configuration_state[key]
        elif key in _configuration_option:
            del _configuration_option[key]

    _time_a["t"] = False
    _configuration_option["ground-floor"] = True
    _configuration_option["SG"] = True
    _configuration_option["SF"] = True


async def timeout_task(user_id):
    await asyncio.sleep(300)
    bot = get_bot()
    if _time_a["t"]:
        remove_if_exists(user_id)
        message = "您的操作已超时，会话 已结束。"
        await bot.send_private_msg(user_id=user_id, message=message)


xj_setup = on_command("setup", aliases={"k"}, rule=to_me(), priority=10, block=True)


@xj_setup.handle()
async def setup_handle(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()):
    ids = event.get_session_id()
    user_id = event.get_user_id()
    if ids.startswith("group"):
        await xj_setup.finish("请使用使用有管理员权限的账号私聊bot进行设置")
    elif XjieVariable._admin_whitelist == []:
        _configuration_state[user_id] = "enter_configuration_mode"
        _configuration_option["option"] = "set_administrator"
        await xj_setup.send("无配置管理员是否配置管理员，在配置完成后需要管理员才能额外添加新的管理员y/n")
    elif int(user_id) in XjieVariable._admin_whitelist or user_id in XjieVariable._admin_whitelist:
        if xj_user_configuration := args.extract_plain_text():
            print(xj_user_configuration)
            await xj_setup.finish("暂不支持")
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
    if args == "退出" or args == "t":
        remove_if_exists(user_id)
        await xj_setup_responsive.finish("退出成功")
    if _configuration_option.get("option") == "set_administrator":
        async def update_admin_list(user_id, confirm):
            if confirm:
                XjieVariable._admin_whitelist.append(user_id)
                admin_string = ",".join(map(str, XjieVariable._admin_whitelist))
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
            await xj_setup_responsive.send("请输入y/n")

    elif _configuration_option.get("option") == "setting_list":
        print(_configuration_option)
        if _configuration_option["ground-floor"] and is_integer_not_float(args):
            logger.warning(f"\033经{args},jincos1\033[0m")
            try:
                args = dz[int(args)]
                logger.warning(f"\033经{args},cos1\033[0m")
            except IndexError:
                await xj_setup_responsive.send("输入错误，请重新输入")

        keydata = xj_file_handle.xj_file_reading("xjie_data.json")
        keys_ending_with_KEY = [k for k in keydata.keys() if k.endswith("_KEY")]

        # 设置平台key
        # #
        if args == 'one' or _configuration_option.get("SL", '') == '1':
            _configuration_option["ground-floor"] = False
            _configuration_option["SL"] = "1"

            if _configuration_option["SG"]:
                _configuration_option["SG"] = False
                return await xj_setup_responsive.send(f"请选择要设置的key\n{menu_dispose(keys_ending_with_KEY)}")

            if _configuration_option["SF"]:
                if not is_integer_not_float(args):
                    logger.warning(f"\033{args},cos12\033[0m")
                    return await xj_setup_responsive.send("输入错误")

                try:
                    a_data = keys_ending_with_KEY[int(args) - 1]
                    _configuration_option["X_KEY"] = a_data
                    _configuration_option["SF"] = False
                    return await xj_setup_responsive.send(f"请输入{a_data}的key")
                except IndexError:
                    print(f"索引 {int(args)} 无效，列表长度为 {len(keys_ending_with_KEY)}")
                    return await xj_setup_responsive.finish("输入错误，请重新输入")

            x_data = _configuration_option["X_KEY"]
            xj_file_handle.xj_file_change("xjie_data.json", x_data, args)
            await xj_setup_responsive.send("配置成功")
            XjieVariable._get_default_platform["xjie_data"] = xj_file_handle.get_keys_ending_with_key("xjie_data.json")
            remove_if_exists(user_id)

        # 配置默认平台
        # #
        elif args == 'two' or _configuration_option.get("SL", '') == '2':

            _configuration_option["ground-floor"] = False
            _configuration_option["SL"] = "2"

            if _configuration_option["SG"]:
                _configuration_option["SG"] = False
                return await xj_setup_responsive.send(f"请选择要设置的key\n{menu_dispose(keys_ending_with_KEY)}")

            if not is_integer_not_float(args):
                return await xj_setup_responsive.send("输入错误1")

            try:
                x_data = keys_ending_with_KEY[int(args) - 1]
                xj_file_handle.xj_file_change("xjie_data.json", "default_api", x_data)
                XjieVariable._get_default_platform["mr"] = x_data
                remove_if_exists(user_id)
                await xj_setup_responsive.send(f"默认天气平台已切换为{x_data}")
            except IndexError:
                await xj_setup_responsive.send("输入错误，请重新输入")

        # 切换和风天气订阅
        # #
        elif args == 'three' or _configuration_option.get("SL", '') == '3':
            _configuration_option["ground-floor"] = False
            _configuration_option["SL"] = "3"

            if _configuration_option["SG"]:
                _configuration_option["SG"] = False
                return await xj_setup_responsive.send(f"请选择要设置的key\n{menu_dispose(qweather_subscribe)}")

            if not is_integer_not_float(args):
                return await xj_setup_responsive.send("输入错误")

            try:
                xj_file_handle.xj_file_change("xjie_data.json", "QWEATHER_APITYPE", int(args) - 1)
                await xj_setup_responsive.send(f"和风天气订阅已切换为{qweather_subscribe[int(args) - 1]}")
                remove_if_exists(user_id)
            except IndexError:
                print("IndexError")
                await xj_setup_responsive.send("输入错误，请重新输入")

        # 和风天气jwt
        # #
        elif args == 'four' or _configuration_option.get("SL", '') == '4':
            _configuration_option["ground-floor"] = False
            _configuration_option["SL"] = "4"

            if _configuration_option["SG"]:
                _configuration_option["SG"] = False
                return await xj_setup_responsive.send(f'是否启用和风天气jwt验证[Y/N]\n目前状态:{XjieVariable.QWEATHER_JWT}')

            if args in xj_yes:
                if XjieVariable.QWEATHER_JWT:
                    await xj_setup_responsive.send("和风天气jwt验证已是开启状态")
                else:
                    xj_file_handle.xj_file_change("xjie_data.json", "QWEATHER_JWT", True)
                    XjieVariable.QWEATHER_JWT = True
                    await xj_setup_responsive.send("已开启和风天气jwt验证")
                remove_if_exists(user_id)
            elif args in xj_no:
                if not XjieVariable.QWEATHER_JWT:
                    await xj_setup_responsive.send("和风天气jwt验证已是关闭状态")
                else:
                    xj_file_handle.xj_file_change("xjie_data.json", "QWEATHER_JWT", False)
                    XjieVariable.QWEATHER_JWT = False
                    await xj_setup_responsive.send("已关闭和风天气jwt验证")
                remove_if_exists(user_id)
            else:
                await xj_setup_responsive.send("请选择是或否")

        # 本地数据库
        # #
        elif args == 'five' or _configuration_option.get("SL", '') == '5':
            _configuration_option["ground-floor"] = False
            _configuration_option["SL"] = "5"

            if _configuration_option["SG"]:
                _configuration_option["SG"] = False
                return await xj_setup_responsive.send(f'是否启用本地数据库[Y/N]\n目前状态:{XjieVariable._Local_database_status}')

            if args in xj_yes:
                if XjieVariable._Local_database_status:
                    await xj_setup_responsive.send("本地数据库已是开启状态")
                else:
                    xj_file_handle.xj_file_change("xjie_data.json", "Local_database_status", True)
                    XjieVariable._Local_database_status = True
                    await xj_setup_responsive.send("已开启本地数据库")
                remove_if_exists(user_id)
            elif args in xj_no:
                if not XjieVariable._Local_database_status:
                    await xj_setup_responsive.send("本地数据库已是关闭状态")
                else:
                    xj_file_handle.xj_file_change("xjie_data.json", "Local_database_status", False)
                    XjieVariable._Local_database_status = False
                    await xj_setup_responsive.send("已关闭本地数据库")
                remove_if_exists(user_id)
            else:
                await xj_setup_responsive.send("请选择是或否")

        elif args == 'six' or _configuration_option.get("SL", '') == '6':

            _configuration_option["ground-floor"] = False
            _configuration_option["SL"] = "6"

            if _configuration_option["SG"]:
                _configuration_option["SG"] = False
                return await xj_setup_responsive.send(f"请选择要设置的key\n{menu_dispose(qweather_kid_sub)}")

            if _configuration_option["SF"]:
                try:
                    q_data = qweather_kid_sub[int(args) - 1]
                    _configuration_option["X_KEY"] = q_data
                    _configuration_option["SF"] = True
                    return await xj_setup_responsive.send(f"请输入{q_data}的ID")
                except IndexError:
                    return await xj_setup_responsive.send("输入错误，请重新输入")

            xj_file_handle.xj_file_change("xjie_data.json", _configuration_option["X_KEY"], args)
            if _configuration_option["X_KEY"] == "QWEATHER_JWT_KID":
                XjieVariable.QWEATHER_JWT_KID = args
            elif _configuration_option["X_KEY"] == "QWEATHER_JWT_SUB":
                XjieVariable.QWEATHER_JWT_SUB = args
            await xj_setup_responsive.send(f"已将{_configuration_option["X_KEY"]}设置为{args}")
            remove_if_exists(user_id)

        else:
            await xj_setup_responsive.send("输入错误")
