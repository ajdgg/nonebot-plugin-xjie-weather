import copy
from typing import Union
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
    "毛毛雨": "309",
    "细雨": "309",
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

VISUALCROSSING_WX_DATA = {
    "type_43": ["100", "晴"],
    "type_42": ["101", "多云"],
    "4": ["102", "少云"],
    "5": ["103", "晴间多云"],
    "6": ["104", "阴"],
    "7": ["300", "阵雨"],
    "8": ["301", "强阵雨"],
    "9": ["302", "雷阵雨"],
    "10": ["303", "强雷阵雨"],
    "11": ["304", "雷阵雨伴有冰雹"],
    "type_26": ["305", "小雨"],
    "13": ["306", "中雨"],
    "14": ["307", "大雨"],
    "15": ["308", "极端降雨"],
    "16": ["309", "毛毛雨/细雨"],
    "17": ["310", "暴雨"],
    "18": ["311", "大暴雨"],
    "19": ["312", "特大暴雨"],
    "type_10": ["313", "冻雨"],
    "type_11": ["313", "冻雨"],
    "type_13": ["313", "大冻雨"],
    "type_14": ["313", "小冻雨"],
    "21": ["314", "小到中雨"],
    "22": ["315", "中到大雨"],
    "23": ["316", "大到暴雨"],
    "24": ["317", "暴雨到大暴雨"],
    "25": ["318", "大暴雨到特大暴雨"],
    "type_21": ["399", "雨"],
    "type_35": ["400", "小雪"],
    "28": ["401", "中雪"],
    "29": ["402", " 大雪"],
    "30": ["403", "暴雪"],
    "31": ["404", "雨夹雪"],
    "32": ["405", "雨雪天气"],
    "33": ["408", "小到中雪"],
    "34": ["409", "中到大雪"],
    "35": ["410", "大到暴雪"],
    "36": ["456", "阵雨夹雪"],
    "37": ["457", "阵雪"],
    "type_31": ["499", "雪"],
    "39": ["500", "薄雾"],
    "40": ["501", "雾"],
    "41": ["502", "霾"],
    "42": ["503", "扬沙"],
    "43": ["504", "浮尘"],
    "44": ["507", "沙尘暴"],
    "45": ["508", "强沙尘暴"],
    "46": ["509", "浓雾"],
    "47": ["510", "强浓雾"],
    "48": ["511", "中度霾"],
    "49": ["512", "重度霾"],
    "50": ["513", "严重霾"],
    "51": ["514", "大雾"],
    "52": ["515", "特强浓雾"],
    "53": ["900", "热"],
    "54": ["901", "冷"],
    "type_27": ["999", "未知"],
    "type_28": ["999", "未知"],
    "type_29": ["999", "未知"],
    "type_12": ["999", "冻雾"],
    "55": ["999", "未知"],
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


def Celsius_to_Fahrenheit(Celsius) -> Union[str, None]:
    """华氏度转摄氏度

    传入:
        Celsius (int or str): 数字或者字符串数字

    返回:
        - 转换后的数字
        - None
    """
    try:
        return round(int(Celsius) * 9 / 5 + 32)
    except ValueError:
        return None


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
                amap["temp_range"] = f'{amap["nighttemp"]}&#xe75b~{amap["daytemp"]}&#xe75b'
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
            _eventual_data["base"] = data["base"]
            _eventual_data["base"]["obsTime"] = data["base"]["date"]
            _eventual_data["base"]["weather"] = data["base"]["type"]
            _eventual_data["base"]["temp"] = data["base"]["high"].replace("°C", "")
            _eventual_data["base"]["weather_img"] = f'<div class="weather-image qi-{icon.get(data["base"].get("type", "未知"), "999")}"></div>'
            blockdata = f'''
            <div class="weather-forecast weather-forecast-qweather">
                {HtmlModule.humidity_html(data["base"].get("humidity", "未知"))}
                {HtmlModule.WDSP_html(data["base"].get("fengxiang", "未知"), data["base"].get("fengli", "未知"), [False])}
            </div>
            '''
            _eventual_data["base"]["blockdata"] = blockdata.replace("\n", "")
            _eventual_data["all"] = data["all"]
            for item in _eventual_data["all"]:
                item["weather_list_image"] = f'<div class="weather-list-image qi-{icon.get(item["type"], "999")}"></div>'
                item["temp_range"] = f'{item["low"].replace("°C", "")}&#xe75b;~{item["high"].replace("°C", "")}&#xe75b;'
            return _eventual_data
        elif api_name == "VISUALCROSSING":
            _eventual_data["base"] = data["base"]
            _eventual_data["base"]["temp"] = Celsius_to_Fahrenheit(data["base"]["temp"])
            _eventual_data["base"]["obsTime"] = ""
            _eventual_data["base"]["weather"] = VISUALCROSSING_WX_DATA[data["base"]["conditions"]][1]
            _eventual_data["base"]["weather_img"] = f'<div class="weather-list-image qi-{VISUALCROSSING_WX_DATA.get(data["conditions"], ["999", "未知"])[0]}"></div>'
            return _eventual_data
