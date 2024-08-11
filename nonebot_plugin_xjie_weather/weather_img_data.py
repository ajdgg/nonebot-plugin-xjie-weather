import copy
from datetime import datetime
from .html_module import HtmlModule

HtmlModule = HtmlModule()

icon = {
    "晴": "100",
    "多云": "101",
    "少云": "102",
    "晴间多云": "103",
    "阴": "104",
    "阵雨": "300",
    "强阵雨": "301",
    "雷阵雨": "302",
    "强雷阵雨": "303",
    "雷阵雨伴有冰雹": "304",
    "小雨": "305",
    "中雨": "306",
    "大雨": "307",
    "极端降雨": "308",
    "毛毛雨/细雨": "309",
    "暴雨": "310",
    "大暴雨": "311",
    "特大暴雨": "312",
    "冻雨": "313",
    "小到中雨": "314",
    "中到大雨": "315",
    "大到暴雨": "316",
    "暴雨到大暴雨": "317",
    "大暴雨到特大暴雨": "318",
    "雨": "399",
    "小雪": "400",
    "中雪": "401",
    "大雪": "402",
    "暴雪": "403",
    "雨夹雪": "404",
    "雨雪天气": "405",
    "小到中雪": "408",
    "中到大雪": "409",
    "大到暴雪": "410",
    "阵雨夹雪": "456",
    "阵雪": "457",
    "雪": "499",
    "薄雾": "500",
    "雾": "501",
    "霾": "502",
    "扬沙": "503",
    "浮尘": "504",
    "沙尘暴": "507",
    "强沙尘暴": "508",
    "浓雾": "509",
    "强浓雾": "510",
    "中度霾": "511",
    "重度霾": "512",
    "严重霾": "513",
    "大雾": "514",
    "特强浓雾": "515",
    "热": "900",
    "冷": "901",
    "未知": "999",
}

_eventual_data = {}


def infer_weekday(year, month, day):
    """
    给定年、月、日，返回对应的星期几。
    星期一为0，星期日为6。
    """
    date = datetime(year, month, day)
    weekday = date.weekday()
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    return weekdays[weekday]


class weather_iaqamg:
    def __init__(self):
        pass

    def get_weather_getimg_data(self, data, api_name):
        if api_name == "AMAP":
            _eventual_data["base"] = data["base"]
            _eventual_data["base"]["temp"] = data["base"]["temperature"]
            _eventual_data["base"]["obsTime"] = data["base"]["reporttime"]
            _eventual_data["base"]["weather_img"] = f'<div class="weather-image qi-{icon.get(data["base"].get("weather", "未知"), "999")}"></div>'
            blockdata = f'''
            <div class="weather-forecast weather-forecast-amap">
                {HtmlModule.humidity_html(data["base"]["humidity"])}
                {HtmlModule.WDSP_html(data["base"]["winddirection"], data["base"]["windpower"])}
            </div>
            '''
            _eventual_data["base"]["blockdata"] = blockdata.replace("\n", "")
            _eventual_data["all"] = data["all"]
            for amap in _eventual_data["all"]:
                year, month, day = map(int, amap["date"].split("-"))
                amap["week"] = infer_weekday(year, month, day)
                amap["weather_list_image"] = f'<div class="weather-list-image qi-{icon.get(amap["dayweather"], "999")}"></div>'
                amap["temp_range"] = f'{amap["nighttemp"]}℃~{amap["daytemp"]}℃'
            return _eventual_data
        elif api_name == "QWEATHER":
            _eventual_data["base"] = data["base"]
            _eventual_data["base"]["weather"] = data["base"]["text"]
            _eventual_data["base"]["weather_img"] = f'<div class="weather-image qi-{icon.get(data["base"].get("text", "未知"), "999")}"></div>'
            blockdata = f'''
            <div class="weather-forecast weather-forecast-qweather">
                {HtmlModule.humidity_html(data["base"].get("humidity", "未知"))}
                {HtmlModule.WDSP_html(data["base"].get("windDir", "未知"), data["base"].get("windScale", "未知"))}
                {HtmlModule.body_surface_temperature_html(data["base"].get("feelsLike", "未知"))}
                {HtmlModule.air_pressure_html(data["base"].get("pressure", "未知"))}
                {HtmlModule.visibility_html(data["base"].get("vis", "未知"))}
            </div>
            '''
            _eventual_data["base"]["blockdata"] = blockdata.replace("\n", "")
            _eventual_data["all"] = data["all"]
            for item in _eventual_data["all"]:
                year, month, day = map(int, item["fxDate"].split("-"))
                item["week"] = infer_weekday(year, month, day)
                item["weather_list_image"] = f'<div class="weather-list-image qi-{icon.get(item["textDay"], "999")}"></div>'
                item["date"] = item["fxDate"]
                item["temp_range"] = f'{item["tempMin"]}&#xe75b;~{item["tempMax"]}&#xe75b;'
            return _eventual_data
        elif api_name == "VVHAN":
            print(data)
            _eventual_data["base"] = data["base"]
            print("1", _eventual_data)
            _eventual_data["base"]["weather"] = data["base"]["type"]
            _eventual_data["base"]["obsTime"] = data["base"]["high"]
            _eventual_data["base"]["weather_img"] = f'<div class="weather-image qi-{icon.get(data["base"].get("type", "未知"), "999")}"></div>'
            blockdata = f'''
            <div class="weather-forecast weather-forecast-qweather">
                {HtmlModule.humidity_html(data["base"].get("humidity", "未知"))}
                {HtmlModule.WDSP_html(data["base"].get("fengxiang", "未知"), data["base"].get("fengli", "未知"))}
            </div>
            '''
            print("2", _eventual_data)
            pass
