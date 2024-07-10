from pydantic import BaseModel, Field
from typing import Optional
from nonebot import get_plugin_config


class Config(BaseModel):
    amap_key: Optional[str] = Field(default=None)
    qweather_key: Optional[str] = Field(default=None)
    superusers: Optional[list] = Field(default=[])


plugin_config: Config = get_plugin_config(Config)
AMAP_KEY = plugin_config.amap_key
QWEATHER_KEY = plugin_config.qweather_key
X_SUPERUSERS = plugin_config.superusers
