from pydantic import BaseModel, Field
from typing import Optional
from nonebot import get_plugin_config
from .file_handle import xj_file_handle
from .data_utilities import convert_to_int_list, has_common_elements, save_superusers

xj_file_handle = xj_file_handle()


class Config(BaseModel):
    amap_key: Optional[str] = Field(default=None)
    qweather_key: Optional[str] = Field(default=None)
    superusers: Optional[list] = Field(default=[])


plugin_config: Config = get_plugin_config(Config)
X_SUPERUSERS = plugin_config.superusers
AMAP_KEY = plugin_config.amap_key
QWEATHER_KEY = plugin_config.qweather_key


class XjieVariable:
    _admin_whitelist = []
    try:
        administrator = xj_file_handle.xj_file_reading("xjie_data.json", "admin_whitelist")
        _admin_whitelist = convert_to_int_list(administrator.split(",")) if administrator else []

        if not has_common_elements(X_SUPERUSERS, _admin_whitelist) or set(_admin_whitelist) != set(X_SUPERUSERS):
            save_superusers(X_SUPERUSERS)
    except Exception as e:
        print(f"Error processing administrator list: {e}")
    _get_default_platform = {}

    xj_data = xj_file_handle.get_keys_ending_with_key("xjie_data.json")
    _get_default_platform["xjie_data"] = xj_data

    default_api = xj_file_handle.xj_file_reading("xjie_data.json", "default_api")
    _get_default_platform["mr"] = default_api
