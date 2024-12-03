'''
coding: UTF-8
Author: AwAjie
Date: 2024-07-09 13:05:47
'''
from ..xj_requests import xj_requests
from ..main import weather_img
from typing import List


weather_img = weather_img()


# 高德获取天气
class AMAP:
    """
    高德地图

    获取高德地图城市编码
        amap_get_adcode(city_name: str, key: str)

    获取高德地图城市天气
        amap_get_weather(city_name: str, key: str)
    """
    async def __fetch_data(self, url):
        async with xj_requests() as xj:
            return await xj.xj_requests_main(url)

    async def amap_get_adcode(self, city_name: str, key: str) -> List:
        """
        async获取高德地图城市编码

        参数:
            city_name (str): 城市名字
            key (str): 高德地图API的密钥。

        返回:
            Any: 请求的结果。返回的类型取决于服务器响应的内容。
        """
        placen_url = 'https://restapi.amap.com/v3/geocode/geo'

        get_place_url = f'{placen_url}?key={key}&address={city_name}&output=JSON'
        gd_city_adcode = await self.__fetch_data(get_place_url)
        if gd_city_adcode is None:
            return ["error", "获取城市编码失败"]
        coding_json = gd_city_adcode.json()
        xiangy = coding_json.get('status')
        if xiangy == 0:
            return ["error", coding_json["info"]]
        # adcode = coding_json["geocodes"][0]["adcode"]-+        # if adcode is None:
        #     return ["error", "错误"]
        # return adcode
        validation_one = len(coding_json.get('geocodes', []))
        if validation_one > 1:
            return ["multi_area_app", "AMAP_KEY", key, coding_json["geocodes"]]
        if validation_one == 0:
            return ["error", "获取城市编码失败"]
        return ["ok", coding_json["geocodes"][0]["adcode"]]

    async def amap_get_weather(self, city_name, key: str, province=None, complete: bool = True):
        """
        async获取高德地图城市天气

        参数:
            city_name (str): 城市名字
            key (str): 高德地图API的密钥。
            province：多地区确认后的参数数组
            complete: 是否是第2次进入

        返回:
            Any: 请求的结果。返回的类型取决于服务器响应的内容。
        """
        if isinstance(city_name, List):
            city_name = city_name[0] + city_name[1]

        city_adcode = None
        if complete:
            city_adcode = await self.amap_get_adcode(city_name, key)
            if city_adcode[0] == "error":
                return city_adcode
            if city_adcode[0] == "multi_area_app":
                return city_adcode
            city_adcode = city_adcode[1]

        weathe_url = 'https://restapi.amap.com/v3/weather/weatherInfo'

        city_data = city_adcode if city_adcode is not None else province[6]
        weather_url = f'{weathe_url}?key={key}&city={city_data}&output=JSON&extensions=all'
        gd_wather_base_url = f'{weathe_url}?key={key}&city={city_data}&output=JSON&extensions=base'

        weather_data = await self.__fetch_data(weather_url)
        weather_json = weather_data.json()

        weather_data_base = await self.__fetch_data(gd_wather_base_url)
        gd_theresultobtained_base = weather_data_base.json()

        if weather_json.get('status') == 0 or gd_theresultobtained_base.get('status') == 0:
            return ["error", '获取天气失败']
        gd_theresultobtained_base_data = gd_theresultobtained_base['lives'][0]
        forecast_data = weather_json["forecasts"][0]["casts"]

        img_data = await weather_img.get_weather_img(forecast_data, gd_theresultobtained_base_data, "AMAP", city_name)
        return img_data
