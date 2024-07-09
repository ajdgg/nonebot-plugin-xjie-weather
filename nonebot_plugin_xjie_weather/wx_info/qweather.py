from ..xj_requests import xj_requests
from ..main import weather_img
from ..file_handle import xj_file_handle


weather_img = weather_img()
xj_file_handle = xj_file_handle()


def qweather_return_url():
    QWEATHER_APITYPE = xj_file_handle.xj_file_reading("xjie_data.json", "QWEATHER_APITYPE")
    if QWEATHER_APITYPE == 0:
        return 'https://devapi.qweather.com/v7/weather/'
    else:
        return 'https://api.qweather.com/v7/weather/'


async def fetch_data(url):
    async with xj_requests() as xj:
        return await xj.xj_requests_main(url)


# 和风
async def qweather_get_location(city_name: str, key: str):
    location = 'https://geoapi.qweather.com/v2/city/lookup'
    location_url = f'{location}?location={city_name}&key={key}'
    gd_city_adcode = await fetch_data(location_url)
    if gd_city_adcode is None:
        raise ValueError("Failed to send request")
    coding_json = gd_city_adcode.json()
    xiangy = coding_json.get('code')
    if xiangy != '200':
        return ["error", '获取城市编码失败']
    return coding_json['location'][0]['id']


class QWEATHER:
    async def qweather_get_weather(self, city: set, key: str):
        location_data = await qweather_get_location(city, key)
        qweather_url = qweather_return_url()
        weather_url = f'{qweather_url}7d?location={location_data}&key={key}'
        hf_weather_url = f'{qweather_url}now?location={location_data}&key={key}'

        hf_city_location = await fetch_data(weather_url)
        weather_json = hf_city_location.json()
        forecast_data = weather_json["daily"]

        hf_city_location_base = await fetch_data(hf_weather_url)
        weather_json = hf_city_location_base.json()
        weather_data_base = weather_json["now"]

        if weather_json.get('code') != '200' or weather_json.get('code') != '200':
            return ["error", '获取天气失败']

        # bot_sc = '===| ' + city + '天气 |===\n-----[ 今天 ]-----\n' + second_day_info_A['fxDate'] + '\n早：' + second_day_info_A['textDay'] + '\n' + '晚：' + second_day_info_A['textNight'] + '\n' + '温度：' + second_day_info_A['tempMax'] + '~' + second_day_info_A['tempMin'] + '\n-----[ 明天 ]-----\n' + second_day_info_B['fxDate'] + '\n早：' + second_day_info_B['textDay'] + '\n' + '晚：' + second_day_info_B['textNight'] + '\n' + '温度：' + second_day_info_B['tempMax'] + '~' + second_day_info_B['tempMin']
        img_data = await weather_img.get_weather_img(forecast_data, weather_data_base, 'QWEATHER', city)
        return img_data
