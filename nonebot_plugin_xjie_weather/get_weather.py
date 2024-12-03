'''
coding: UTF-8
Author: AwAjie
Date: 2024-07-05 16:26:29
'''
from .config import XjieVariable
from .xjie_db import DatabaseManager
from .file_handle import xj_file_handle
from .wx_info.amap import AMAP
from .wx_info.qweather import QWEATHER
from .wx_info.vvhan import VVHAN
from .main import weather_img
from typing import List
weather_img = weather_img()
# xj_requests = xj_requests()
AMAP = AMAP()
QWEATHER = QWEATHER()
VVHAN = VVHAN()
DatabaseManager = DatabaseManager()
xj_file_handle = xj_file_handle()


def a_qf():
    key_data = xj_file_handle.get_keys_ending_with_key("xjie_data.json")
    a = list(key_data.items())
    first_key, first_value = a[0]
    return [first_key, first_value]


Latitude_and_longitude_platform = [
    'QWEATHER_KEY',
    "QWEATHER_JWT_KEY"
]

only_localdata = [
    "VISUALCROSSING_KEY",
]

select_get_platform_s = {
    "AMAP_KEY": AMAP.amap_get_weather,
    "QWEATHER_JWT_KEY": QWEATHER.qweather_get_weather,
    "QWEATHER_KEY": QWEATHER.qweather_get_weather,
    "VVHAN_KEY": VVHAN.vvhan_weather,
}


# def select_get_platform(city, key, platform):
#     if platform == "AMAP_KEY":
#         return AMAP.amap_get_weather(city, key)
#     elif platform == "QWEATHER_KEY":
#         return QWEATHER.qweather_get_weather(city, key)
#     return


class get_weather:
    def __init__(self):
        pass

    async def xj_get_weather_main(self, city_name: str, get_default_platform=None):
        """
        调用

        参数:
        - city_name: str 城市名
        - get_default_platform: str 平台
        """
        async def localdata_code():
            List_of_regions = DatabaseManager.city_lnglat(city_name)
            print(List_of_regions)
            if (List_of_regions == []):
                return ["error", '未知城市']
            if len(List_of_regions) > 1:
                return ["multi_area", get_default_platform[0], List_of_regions]
            if get_default_platform[0] not in select_get_platform_s:
                return ["error", '未知平台']
            data = [
                get_default_platform[0],
                get_default_platform[1],
                List_of_regions[0][0],
                List_of_regions[0][1],
                List_of_regions[0][2],
                List_of_regions[0][3],
                None,
            ]
            return await select_get_platform_s[get_default_platform[0]](city_name, key=get_default_platform[1], province=data, complete=False)
        #
        # 启用本地经纬度数据库和支持的部分
        # #
        if XjieVariable._Local_database_status is True and get_default_platform[0] in Latitude_and_longitude_platform:
            return await localdata_code()

        #
        # 默认
        # #
        else:
            if get_default_platform[0] not in select_get_platform_s:
                return ["error", '未知平台']
            if get_default_platform[0] in only_localdata:
                return await localdata_code()
            return await select_get_platform_s[get_default_platform[0]](city_name, key=get_default_platform[1])

    async def xj_get_weather_p(self, list,):
        return await select_get_platform_s[list[0]](list[2], list[1], province=list, complete=False)
