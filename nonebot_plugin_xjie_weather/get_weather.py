from .file_handle import xj_file_handle
from .wx_info.amap import AMAP
from .wx_info.qweather import QWEATHER
from .wx_info.vvhan import VVHAN
from .main import weather_img
weather_img = weather_img()
# xj_requests = xj_requests()
AMAP = AMAP()
QWEATHER = QWEATHER()
VVHAN = VVHAN()
xj_file_handle = xj_file_handle()


def a_qf():
    key_data = xj_file_handle.get_keys_ending_with_key("xjie_data.json")
    a = list(key_data.items())
    first_key, first_value = a[0]
    return [first_key, first_value]


select_get_platform_s = {
    "AMAP_KEY": AMAP.amap_get_weather,
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

    def xj_get_weather_main(self, city_name: str, get_default_platform: str = None):
        if get_default_platform is None or get_default_platform == '':
            MR_AP = a_qf()
            if MR_AP[0] not in select_get_platform_s:
                return ["error", '未知平台']
            return select_get_platform_s[MR_AP[0]](city_name, MR_AP[1])
        else:
            a_data = xj_file_handle.xj_file_reading("xjie_data.json", get_default_platform)
            if get_default_platform not in select_get_platform_s:
                return ["error", '未知平台']
            return select_get_platform_s[get_default_platform](city_name, a_data)
