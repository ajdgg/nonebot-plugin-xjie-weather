import json
from pathlib import Path


def file_path(file):
    return Path(__file__).resolve().parent / file


class xj_file_handle:
    def __init__(self):
        pass

    def xj_file_reading(self, file_name: str, file_content: str = None):
        json_file_path_reading = file_path(file_name)
        with json_file_path_reading.open("r", encoding="utf-8") as json_file:
            loaded_data = json.load(json_file)
        if file_content is None:
            return loaded_data
        return loaded_data.get(file_content, None)

    def xj_file_change(self, file_name: str, file_key: str, file_content: str):
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

    def get_keys_ending_with_key(self, json_data, key_suffix='_KEY'):
        json_file_path_reading = file_path(json_data)
        with json_file_path_reading.open("r", encoding="utf-8") as json_file:
            loaded_data = json.load(json_file)
        result = {}
        for key in loaded_data.keys():
            if key.endswith(key_suffix) and loaded_data[key]:
                result[key] = loaded_data[key]
        return result
