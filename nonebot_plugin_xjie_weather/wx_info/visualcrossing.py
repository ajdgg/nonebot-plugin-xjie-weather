'''
coding: UTF-8
Author: AwAjie
Date: 2024-08-26 23:50:21
'''
from ..xj_requests import xj_requests
from ..main import weather_img


weather_img = weather_img()


class VISUALCROSSING:

    """
    visualcrossing

    获取visualcrossing城市天气
        visualcrossing_weather(self, city_name: str, key: str)
    """
    async def __fetch_data(self, url):
        async with xj_requests() as xj:
            return await xj.xj_requests_main(url)

    async def visualcrossing_weather(self, city_name: str, key: str, province=None, complete: bool = True) -> any:
        visualcrossing_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

        visualcrossing_url += f"{province[4]},{province[5]}?include=days&lang=zh&key={key}&contentType=json"
        weather_data = await self.__fetch_data(visualcrossing_url)
        if weather_data is None:
            return ['error', '请求失败']
        weather_data = weather_data.json()

        weather_data_all = weather_data["days"]
        weather_data_base = weather_data["days"][0]

        return await weather_img.get_weather_img(weather_data_all, weather_data_base, "VISUALCROSSING", city_name)
