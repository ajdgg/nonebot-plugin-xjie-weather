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
        get_place_url = f'{placen_url}?key={key}&city={city_name}&address={city_name}&output=JSON'
        gd_city_adcode = await self.__fetch_data(get_place_url)
        if gd_city_adcode is None:
            print(ValueError("Failed to send request"))
            return ["error", "获取城市编码失败"]
        coding_json = gd_city_adcode.json()
        xiangy = coding_json.get('status')
        if xiangy == 0:
            return ["error", coding_json["info"]]
        adcode = coding_json["geocodes"][0]["adcode"]
        if adcode is None:
            return ["error", "错误"]
        return adcode

    async def amap_get_weather(self, city_name: str, key: str):
        """
        async获取高德地图城市天气

        参数:
            city_name (str): 城市名字
            key (str): 高德地图API的密钥。

        返回:
            Any: 请求的结果。返回的类型取决于服务器响应的内容。
        """
        city_adcode = await self.amap_get_adcode(city_name, key)
        if isinstance(city_adcode, list):
            return city_adcode
        weathe_url = 'https://restapi.amap.com/v3/weather/weatherInfo'
        weather_url = f'{weathe_url}?key={key}&city={city_adcode}&output=JSON&extensions=all'
        gd_wather_base_url = f'{weathe_url}?key={key}&city={city_adcode}&output=JSON&extensions=base'

        weather_data = await self.__fetch_data(weather_url)
        weather_json = weather_data.json()

        weather_data_base = await self.__fetch_data(gd_wather_base_url)
        gd_theresultobtained_base = weather_data_base.json()

        if weather_json.get('status') == 0 or gd_theresultobtained_base.get('status') == 0:
            return ["error", '获取天气失败']
        gd_theresultobtained_base_data = gd_theresultobtained_base['lives'][0]
        forecast_data = weather_json["forecasts"][0]["casts"]

        # bot_sc = '===| ' + city_name + '天气 |===\n-----[ 今天 ]-----\n' + second_day_info_A['date'] + '\n星期' + second_day_info_A['week'] + '\n早：' + second_day_info_A['dayweather'] + '\n' + '晚：' + second_day_info_A['dayweather'] + '\n' + '温度：' + second_day_info_A['nighttemp'] + '~' + second_day_info_A['daytemp'] + '\n-----[ 明天 ]-----\n' + second_day_info_B['date'] + '\n星期' + second_day_info_B['week'] + '\n早：' + second_day_info_B['dayweather'] + '\n' + '晚：' + second_day_info_B['dayweather'] + '\n' + '温度：' + second_day_info_B['nighttemp'] + '~' + second_day_info_B['daytemp']
        img_data = await weather_img.get_weather_img(forecast_data, gd_theresultobtained_base_data, "AMAP", city_name)
        return img_data
