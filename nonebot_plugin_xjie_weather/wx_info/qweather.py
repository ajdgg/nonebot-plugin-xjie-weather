'''
coding: UTF-8
Author: AwAjie
Date: 2024-07-09 13:53:29
'''
from ..xj_requests import xj_requests
from ..main import weather_img
from ..config import XjieVariable
from typing import List
import jwt
import time

weather_img = weather_img()


class QWEATHER:
    """
    高德地图

    获取和风天气城市编码
        qweather_get_location(city_name: str, key: str)

    获取和风天气城市天气
        qweather_get_weather(city_name: str, key: str)
    """
    def Qjwt(self, key) -> str:
        HeaderObj = {
            "alg": "EdDSA",
            "kid": XjieVariable.QWEATHER_JWT_SUB
        }
        PayloadObj = {
            "sub": XjieVariable.QWEATHER_JWT_KID,
            "iat": int(time.time()) - 30,
            "exp": int(time.time()) + 900
        }

        return jwt.encode(PayloadObj, key, headers=HeaderObj, algorithm='EdDSA')

    async def __fetch_data(self, url, headers=None):
        async with xj_requests() as xj:
            return await xj.xj_requests_main(url, headers=headers)

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
            location_params = f'location={city_name[1]}&adm={city_name[0]}'
        else:
            location_params = f'location={city_name}'

        if XjieVariable.QWEATHER_JWT:
            xheader = {
                "Authorization": 'Bearer ' + self.Qjwt(key)
            }
            location_url = f'{location}?{location_params}'
            headers = xheader
        else:
            location_url = f'{location}?{location_params}&key={key}'
            headers = None

        gd_city_adcode = await self.__fetch_data(location_url, headers=headers)

        if gd_city_adcode is None:
            return ['error', '网络延迟过高']
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
        key = key if XjieVariable.QWEATHER_JWT else XjieVariable.QWEATHER_KEY
        location_data = None
        if complete:
            location_data = await self.qweather_get_location(city_name, key)
            if location_data[0] == "error":
                return location_data
            if location_data[0] == "multi_area_app":
                return location_data
            location_data = location_data[1]

        qweather_url = self.__qweather_return_url()
        if location_data is None:
            if province[4] is not None and province[5] is not None:
                location_data = f"{province[4]:.2f},{province[5]:.2f}"
            else:
                location_data = province[6]

        if XjieVariable.QWEATHER_JWT:
            xheader = {
                "Authorization": 'Bearer ' + self.Qjwt(key)
            }
            auth_param = ''
            header = xheader
        else:
            auth_param = f'&key={key}'
            header = None

        base_url_template = f'{qweather_url}{{}}?location={location_data}{auth_param}'
        hf_city_location = await self.__fetch_data(base_url_template.format('7d'), headers=header)
        hf_city_location_base = await self.__fetch_data(base_url_template.format('now'), headers=header)

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
