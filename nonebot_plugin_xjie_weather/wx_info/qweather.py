'''
coding: UTF-8
Author: AwAjie
Date: 2024-07-09 13:53:29
'''
from ..xj_requests import xj_requests
from ..main import weather_img
from ..config import XjieVariable
from typing import List


weather_img = weather_img()
XjieVariable = XjieVariable()


class QWEATHER:
    """
    高德地图

    获取和风天气城市编码
        qweather_get_location(city_name: str, key: str)

    获取和风天气城市天气
        qweather_get_weather(city_name: str, key: str)
    """
    async def __fetch_data(self, url):
        async with xj_requests() as xj:
            return await xj.xj_requests_main(url)

    def __qweather_return_url(self) -> str:
        if XjieVariable.QWEATHER_APITYPE == 0:
            return 'https://devapi.qweather.com/v7/weather/'
        else:
            return 'https://api.qweather.com/v7/weather/'

    # 和风
    async def qweather_get_location(self, city_name: str, key: str):
        """
        async获取和风天气城市编码

        参数:
            city_name (str): 城市名字
            key (str): 和风天气API的密钥。

        返回:
            Any: 请求的结果。返回的类型取决于服务器响应的内容。
        """
        location = 'https://geoapi.qweather.com/v2/city/lookup'

        if isinstance(city_name, List):
            location_url = f'{location}?location={city_name[1]}&adm={city_name[0]}&key={key}'
        else:
            location_url = f'{location}?location={city_name}&key={key}'

        gd_city_adcode = await self.__fetch_data(location_url)
        if gd_city_adcode is None:
            return ['error', '网络延迟过高']
            # raise ValueError("Failed to send request")
        coding_json = gd_city_adcode.json()
        if coding_json.get('code') != '200':
            return ["error", '获取城市编码失败']

        validation_one = len(coding_json.get('location', []))
        if validation_one > 1:
            return ["multi_area_app", "QWEATHER_KEY", key, coding_json["location"]]
        if validation_one == 0:
            return ["error", "获取城市编码失败"]
        return ["ok", coding_json['location'][0]['id']]

    async def qweather_get_weather(self, city_name, key: str, province=None, complete: bool = True):
        """
        async获取和风天气城市天气

        参数:
            city_name (str): 城市名字
            key (str): 和风天气API的密钥。

        返回:
            Any: 请求的结果。返回的类型取决于服务器响应的内容。
        """

        location_data = None
        if complete:
            location_data = await self.qweather_get_location(city_name, key)
            if location_data[0] == "error":
                return location_data
            if location_data[0] == "multi_area_app":
                return location_data
            location_data = location_data[1]

        qweather_url = self.__qweather_return_url()
        location_data = location_data if location_data is not None else (f"{province[4]:.2f}" + "," + f"{province[5]:.2f}") if province[4] is not None and province[5] is not None else province[6]
        print(location_data, "1")
        print(XjieVariable._Local_in_latitude_and_longitude, "3")
        print(province[6], "4")
        weather_url = f'{qweather_url}7d?location={location_data}&key={key}'
        hf_weather_url = f'{qweather_url}now?location={location_data}&key={key}'

        hf_city_location = await self.__fetch_data(weather_url)
        hf_city_location_base = await self.__fetch_data(hf_weather_url)
        if hf_city_location is None or hf_city_location_base is None:
            return ['error', '网络延迟过高']
        weather_json_a = hf_city_location.json()

        weather_json_b = hf_city_location_base.json()

        if weather_json_a.get('code') != '200' or weather_json_b.get('code') != '200':
            return ["error", '获取天气失败']

        forecast_data = weather_json_a["daily"]
        weather_data_base = weather_json_b["now"]

        img_data = await weather_img.get_weather_img(forecast_data, weather_data_base, 'QWEATHER', city_name)
        return img_data
