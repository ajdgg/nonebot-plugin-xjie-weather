import copy
img_svg_data = {
    "晴": '<div class="weather-image clear"></div>',
    "阴": '<div class="weather-image cloudy"></div>',
    "多云": '<div class="weather-image cloudy"></div>',
    "小雨": '<div class="weather-image light-rain"></div>',
    "中雨": '<div class="weather-image moderate-rain"></div>',
    "大雨": '<div class="weather-image heavy-rain"></div>',
}
list_svg_data = {
    "晴": '<div class="weather-list-image clear"></div>',
    "阴": '<div class="weather-list-image cloudy"></div>',
    "多云": '<div class="weather-list-image cloudy"></div>',
    "小雨": '<div class="weather-list-image light-rain"></div>',
    "中雨": '<div class="weather-list-image moderate-rain"></div>',
    "大雨": '<div class="weather-list-image heavy-rain"></div>',
}

_week = {
    "1": "星期一",
    "2": "星期二",
    "3": "星期三",
    "4": "星期四",
    "5": "星期五",
    "6": "星期六",
    "7": "星期日"
}

_eventual_data = {}


def add_or_replace_key_in_dicts(data_list, key_operation, key_source, replacement_dict=None, add_new_key=False, new_key_name=None):
    """
    在字典列表的深拷贝中，根据操作类型执行添加或替换键值。
    如果add_new_key为True，则添加新键；如果replacement_dict不为空，则替换值。
    如果在replacement_dict中找不到值，则尝试使用"未知"键的值（如果存在）。

    :param data_list: 包含字典的列表，每个字典可能包含操作所涉及的键
    :param key_operation: 操作类型，'replace'表示替换值，'add'表示添加新键
    :param key_source: 当操作为替换时，用于查找值的键；当操作为添加时，用于获取值的键
    :param replacement_dict: 仅当操作为替换时使用，用于映射替换值的字典
    :param add_new_key: 是否添加新键，默认False
    :param new_key_name: 添加新键时使用的键名
    :return: 修改后的字典列表的深拷贝
    """
    new_data_list = copy.deepcopy(data_list)

    for dictionary in new_data_list:
        if key_operation == 'replace' and replacement_dict is not None and key_source in dictionary:
            original_value = dictionary[key_source]
            if original_value in replacement_dict:
                dictionary[key_source] = replacement_dict[original_value]
        elif key_operation == 'add' and add_new_key and key_source in dictionary and new_key_name is not None:
            original_value = dictionary[key_source]
            new_value = replacement_dict.get(original_value, dictionary.get("未知", original_value))
            dictionary[new_key_name] = new_value

    return new_data_list


class weather_iaqamg:
    def __init__(self):
        pass

    def get_weather_getimg_data(self, data, api_name):
        if api_name == 'AMAP':
            _eventual_data["base"] = data["base"]
            _eventual_data["base"]["weather-img"] = img_svg_data[data["base"]["weather"]]
            blockdata = f'''
            <div class="humidness">
                <div class="humidness-image"></div>
                <div class="humidness-data">{data["base"]["humidity"]}%</div>
            </div>
            <div class="wind">
                <div class="wind-image"></div>
                <div class="wind-data">{data["base"]["winddirection"]}风<span>{data["base"]["windpower"]}</span></div>
            </div>
            '''
            _eventual_data["base"]["blockdata"] = blockdata.replace('\n', '')
            _eventual_data["all"] = data["all"]
            _eventual_data["all"] = add_or_replace_key_in_dicts(_eventual_data["all"], 'replace', "week", _week, add_new_key=False)
            _eventual_data["all"] = add_or_replace_key_in_dicts(_eventual_data["all"], "add", "dayweather", list_svg_data, add_new_key=True, new_key_name="weather_list_image")
            return _eventual_data
