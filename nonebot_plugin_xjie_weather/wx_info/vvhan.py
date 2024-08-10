from ..xj_requests import xj_requests
from ..main import weather_img
from typing import List


weather_img = weather_img()


class VVHAN:
    async def __fetch_data(self, url):
        async with xj_requests() as xj:
            return await xj.xj_requests_main(url)

    async def vvhan_weather(self, city_name: str, key: str):
        vvhan_weather_url = "https://api.vvhan.com/api/weather"
        vvhan_weather_realtime_url = f"{vvhan_weather_url}?city={city_name}"
        vvhan_weather_oneweek_url = f"{vvhan_weather_url}?city={city_name}&type=week"
        print(vvhan_weather_realtime_url, vvhan_weather_oneweek_url)

        vvhan_weather_realtime_httpdata = await self.__fetch_data(vvhan_weather_realtime_url)
        vvhan_weather_realtime_httpdata_json = vvhan_weather_realtime_httpdata.json()

        vvhan_weather_oneweek_httpdata = await self.__fetch_data(vvhan_weather_oneweek_url)
        vvhan_weather_oneweek_httpdata_json = vvhan_weather_oneweek_httpdata.json()

        if not vvhan_weather_realtime_httpdata_json.get('success') or not vvhan_weather_oneweek_httpdata_json.get('success'):
            return ["error", '获取天气失败']

        forecast_data = vvhan_weather_oneweek_httpdata_json.get('data')
        vvhan_theresultobtained_base_data = vvhan_weather_realtime_httpdata_json.get('data')

        print(forecast_data, vvhan_theresultobtained_base_data)
        # img_data = await weather_img.get_weather_img(forecast_data, vvhan_theresultobtained_base_data, "VVHAN", city_name)
        # return img_data
