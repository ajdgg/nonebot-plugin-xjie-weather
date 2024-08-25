# '''
# coding: UTF-8
# Author: AwAjie
# Date: 2024-08-24 13:35:34
# '''
import sqlite3
from pathlib import Path

# 连接SQLite数据库
conn = sqlite3.connect(Path(__file__).resolve().parent / 'src/db/region.db')

c = conn.cursor()


def city_lnglat(value: str, key="name"):
    c.execute(f'SELECT lng, lat FROM region WHERE {key} LIKE ?', (f'{value}%',))
    row = c.fetchone()
    if row:
        return row
    else:
        return None


def close():
    c.close()
    conn.close()
