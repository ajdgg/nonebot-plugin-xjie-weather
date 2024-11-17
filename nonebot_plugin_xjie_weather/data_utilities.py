from typing import List
from .file_handle import xj_file_handle


xj_file_handle = xj_file_handle()


def menu_dispose(list: List[str]) -> str:
    """
    将一个字符串列表转换为带有索引的菜单格式字符串。

    参数:
        list (List[str]): 包含菜单项的字符串列表。

    返回:
        str: 格式化后的菜单字符串，每一行包含一个索引和对应的菜单项。

    示例:
        如果输入的list为 ["Option1", "Option2"]，则输出为：
        "[1] Option1
        [2] Option2"
    """
    return "\n".join(f"[{i}] {func}" for i, func in enumerate(list, start=1))


def is_integer_not_float(s: str) -> bool:
    """
    判断给定的字符串是否能被解析为一个整数。

    参数:
        s (str): 要检查的字符串。

    返回:
        bool: 如果字符串可以被解析为整数，则返回True；否则返回False。
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def has_common_elements(list1: List, list2: List) -> bool:
    """
    判断两个列表是否有共同的元素。

    参数:
        list1 (List): 第一个列表。
        list2 (List): 第二个列表。

    返回:
        bool: 如果两个列表有至少一个共同元素，则返回True；否则返回False。
    """
    set1 = set(list1)
    set2 = set(list2)
    return bool(set1 & set2)


def convert_to_int_list(values) -> List:
    """
    将输入的可迭代对象中的每个元素转换为整数，并返回一个整数列表。

    参数:
        values (Iterable): 包含可转换为整数的元素的可迭代对象。

    返回:
        List[int]: 一个包含整数的列表。如果输入中存在不可转换为整数的元素，
                    则返回一个空列表。

    示例:
        >>> convert_to_int_list(['1', '2', '3'])
        [1, 2, 3]
        >>> convert_to_int_list(['1', 'a', '3'])
        []
    """
    try:
        return [int(value) for value in values]
    except ValueError:
        return []


def save_superusers(superusers):
    """
    将超级用户列表保存到配置文件中。

    参数:
        superusers (list): 超级用户的ID列表。

    功能:
        - 将superusers列表转换为逗号分隔的字符串。
        - 调用xj_file_handle.xj_file_change方法更新"xjie_data.json"文件中的"admin_whitelist"字段，
        将转换后的字符串作为新值。

    注意:
        - superusers列表中的元素应能转换为字符串。
        - xj_file_handle.xj_file_change方法负责文件的读取和写入操作。
    """
    superusers_str = ",".join(map(str, superusers))
    xj_file_handle.xj_file_change("xjie_data.json", "admin_whitelist", superusers_str)


def l_list(list_data):
    """拼接字符串
    Args:
        list_data (_type_): _description_

    Returns:
        _type_: _description_
    """
    return [f"{province}-{district}" for district, province, _, _ in list_data]
