from .xj_requests import xj_requests
from .file_handle import xj_file_handle
xj_requests = xj_requests()
xj_file_handle = xj_file_handle()
key_data = xj_file_handle.get_keys_ending_with_key("xjie_data.json")


def a_qf(arrt):
    a = list(arrt.items())
    first_key, first_value = a[0]
    return [first_key, first_value]


# 高德获取城市编码
def amap_get_adcode(city_name: str, key: str):
    placen_url = 'https://restapi.amap.com/v3/geocode/geo'
    get_place_url = f'{placen_url}?key={key}&city={city_name}&address={city_name}&output=JSON'
    gd_city_adcode = xj_requests.xj_requests_main(get_place_url)
    if gd_city_adcode is None:
        raise ValueError("Failed to send request")
    coding_json = gd_city_adcode.json()
    xiangy = coding_json.get('status')
    if xiangy == 0:
        return ["error", coding_json["info"]]
    adcode = coding_json["geocodes"][0]["adcode"]
    if adcode is None:
        return ["error", "错误"]
    return adcode


# 高德获取天气
def amap_get_weather(city_name: str, key: str):
    city_adcode = amap_get_adcode(city_name, key)
    if isinstance(city_adcode, list):
        return city_adcode
    weathe_url = 'https://restapi.amap.com/v3/weather/weatherInfo'
    weather_url = f'{weathe_url}?key={key}&city={city_adcode}&output=JSON&extensions=all'
    weather_data = xj_requests.xj_requests_main(weather_url)
    weather_json = weather_data.json()
    YZ_weather = weather_json['status'][0]
    if YZ_weather == 0:
        print('获取天气失败', weather_json.get('info'))
    forecast_data = weather_json["forecasts"][0]["casts"]
    second_day_info_A = forecast_data[0]
    second_day_info_B = forecast_data[1]
    bot_sc = '===| ' + city_name + '天气 |===\n-----[ 今天 ]-----\n' + second_day_info_A['date'] + '\n星期' + second_day_info_A['week'] + '\n早：' + second_day_info_A['dayweather'] + '\n' + '晚：' + second_day_info_A['dayweather'] + '\n' + '温度：' + second_day_info_A['nighttemp'] + '~' + second_day_info_A['daytemp'] + '\n-----[ 明天 ]-----\n' + second_day_info_B['date'] + '\n星期' + second_day_info_B['week'] + '\n早：' + second_day_info_B['dayweather'] + '\n' + '晚：' + second_day_info_B['dayweather'] + '\n' + '温度：' + second_day_info_B['nighttemp'] + '~' + second_day_info_B['daytemp']
    return bot_sc


def qweather_get_location(city_name: str, key: str):
    location = 'https://geoapi.qweather.com/v2/city/lookup'
    location_url = f'{location}?location={city_name}&key={key}'
    gd_city_adcode = xj_requests.xj_requests_main(location_url)
    if gd_city_adcode is None:
        raise ValueError("Failed to send request")
    coding_json = gd_city_adcode.json()
    xiangy = coding_json.get('code')
    if xiangy != '200':
        return ["error", '获取城市编码失败']
    return coding_json['location'][0]['id']


def qweather_get_weather(city: set, key: str):
    location_data = qweather_get_location(city, key)
    qweather_url = 'https://devapi.qweather.com/v7/weather/3d'
    weather_url = f'{qweather_url}?location={location_data}&key={key}'
    gd_city_location = xj_requests.xj_requests_main(weather_url)
    weather_json = gd_city_location.json()
    xiangy = weather_json.get('code')
    if xiangy != '200':
        return ["error", '获取天气失败']
    forecast_data = weather_json["daily"]
    second_day_info_A = forecast_data[0]
    second_day_info_B = forecast_data[1]
    bot_sc = '===| ' + city + '天气 |===\n-----[ 今天 ]-----\n' + second_day_info_A['fxDate'] + '\n早：' + second_day_info_A['textDay'] + '\n' + '晚：' + second_day_info_A['textNight'] + '\n' + '温度：' + second_day_info_A['tempMax'] + '~' + second_day_info_A['tempMin'] + '\n-----[ 明天 ]-----\n' + second_day_info_B['fxDate'] + '\n早：' + second_day_info_B['textDay'] + '\n' + '晚：' + second_day_info_B['textNight'] + '\n' + '温度：' + second_day_info_B['tempMax'] + '~' + second_day_info_B['tempMin']
    return bot_sc


def select_get_platform(city, key, platform):
    if platform == "AMAP_KEY":
        return amap_get_weather(city, key)
    elif platform == "QWEATHER_KEY":
        return qweather_get_weather(city, key)
    return key_data


class get_weather:
    def __init__(self):
        pass

    def xj_get_weather_main(self, city_name: str, get_default_platform: str = None):
        if get_default_platform is None or get_default_platform == '':
            MR_AP = a_qf(key_data)
            return select_get_platform(city_name, MR_AP[1], MR_AP[0])
        else:
            a_data = xj_file_handle.xj_file_reading("xjie_data.json", get_default_platform)
            return select_get_platform(city_name, a_data, get_default_platform)
