'''
coding: UTF-8
Author: AwAjie
Date: 2024-08-26 23:50:21
'''
from ..xj_requests import xj_requests
from ..xjie_db import DatabaseManager


class VISUALCROSSING:
    def __init__(self) -> None:
        self.db = DatabaseManager()

    """
    visualcrossing

    获取visualcrossing城市天气
        visualcrossing_weather(self, city_name: str, key: str)
    """
    async def __fetch_data(self, url):
        async with xj_requests() as xj:
            return await xj.xj_requests_main(url)

    async def visualcrossing_weather(self, citly: str, key: str) -> any:
        visualcrossing_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        latlng = self.db.city_lnglat(citly)
        self.db.close()
        visualcrossing_url += f"{latlng[0]},{latlng[1]}?include=days&lang=zh&key={key}&contentType=json"
        weather_data = await self.__fetch_data(visualcrossing_url)
        if weather_data is None:
            return ['error', '请求失败']
