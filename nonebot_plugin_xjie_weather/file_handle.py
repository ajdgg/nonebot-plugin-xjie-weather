import json
from pathlib import Path


def file_path(file):
    return Path(__file__).resolve().parent / file


class xj_file_handle:
    def __init__(self):
        pass

    def xj_file_reading(self, file_name: str, file_content: str = None):
        """
        从JSON文件中读取数据。

        参数:
        - file_name (str): 要读取的JSON文件名。
        - file_content (str, 可选): 从文件中检索的具体内容键。如果不提供，
          则返回整个JSON对象。

        返回:
        - dict 或 任意类型: 如果没有请求特定的内容键，则返回整个JSON对象；
          否则返回与请求键相对应的值。如果指定的键未找到，则返回None。

        异常:
        - FileNotFoundError: 如果指定的文件不存在。
        - json.JSONDecodeError: 如果从文件解码JSON数据时出现错误。
        - Exception: 文件读取过程中发生的任何其他意外错误。

        使用示例:
        >>> xj_file_reading("example.json")
        {'key1': 'value1', 'key2': 'value2'}

        >>> xj_file_reading("example.json", "key1")
        'value1'
        """
        json_file_path_reading = file_path(file_name)
        try:
            with json_file_path_reading.open("r", encoding="utf-8") as json_file:
                loaded_data = json.load(json_file)
            if file_content is None:
                return loaded_data
            return loaded_data.get(file_content, None)
        except FileNotFoundError:
            print(f"找不到文件: {file_name}")
            return None
        except json.JSONDecodeError:
            print(f"从文件解码JSON时出错: {file_name}")
            return None
        except Exception as e:
            print(f"发生错误: {e}")
            return None

    def xj_file_change(self, file_name: str, file_key: str, file_content: str):
        """
        修改JSON文件中的特定键值。

        参数:
        - file_name (str): 要修改的JSON文件名。
        - file_key (str): 要更改的键名。
        - file_content (str): 新的键值。

        功能:
        - 读取指定的JSON文件。
        - 如果文件不存在或内容不是有效的JSON格式，将打印错误信息并返回。
        - 如果指定的键不存在于文件中，将打印错误信息并返回。
        - 将指定的键值更新为新的内容。
        - 将修改后的内容写回原文件。

        异常:
        - FileNotFoundError: 如果指定的文件不存在。
        - json.JSONDecodeError: 如果文件内容不是有效的JSON格式。
        - IOError: 写入文件时发生错误。

        使用示例:
        >>> xj_file_change("settings.json", "theme", "dark")
        # 这将把'settings.json'文件中的'theme'键值改为'dark'。
        """
        json_file_path_change = file_path(file_name)
        try:
            with json_file_path_change.open("r", encoding="utf-8") as json_file:
                loaded_data = json.load(json_file)
        except FileNotFoundError:
            print(f"文件 {file_name} 未找到。")
            return
        except json.JSONDecodeError:
            print(f"{file_name} 文件内容不是有效的JSON格式。")
            return
        if file_key not in loaded_data:
            print(f"键 '{file_key}' 在文件中不存在。")
            return
        loaded_data[file_key] = file_content
        try:
            with json_file_path_change.open("w", encoding="utf-8") as json_file:
                json.dump(loaded_data, json_file, indent=4)
        except IOError as e:
            print(f"写入文件时发生错误: {e}")

    def get_keys_ending_with_key(self, json_data: str, key_suffix: str = '_KEY') -> dict:
        """
        获取指定JSON文件中所有以特定后缀结尾的键及其对应的值。

        参数:
        - json_data (str): JSON文件的路径。
        - key_suffix (str, 可选): 键名需匹配的后缀，默认为'_KEY'。

        返回:
        - dict: 包含所有匹配后缀的键值对的字典。如果文件不存在、解析失败或发生其他错误，则返回None。

        异常:
        - FileNotFoundError: 文件未找到。
        - json.JSONDecodeError: 文件内容非有效JSON格式。
        - Exception: 其他未预期的错误。

        示例用法:
        >>> result = get_keys_ending_with_key("config.json")
        # 返回config.json中所有以'_KEY'结尾的键值对。

        注意:
        - 函数会忽略那些值为空的键。
        """
        try:
            json_file_path_reading = file_path(json_data)

            with open(json_file_path_reading, "r", encoding="utf-8") as json_file:
                loaded_data = json.load(json_file)

        except FileNotFoundError:
            print(f"错误: 文件 {json_file_path_reading} 未找到。")
            return None

        except json.JSONDecodeError:
            print(f"错误: 未能从文件 {json_file_path_reading} 解析JSON。")
            return None

        except Exception as e:
            print(f"发生了未预料到的错误: {e}")
            return None

        result = {}
        for key in loaded_data.keys():
            if key.endswith(key_suffix) and loaded_data[key]:
                result[key] = loaded_data[key]

        return result
