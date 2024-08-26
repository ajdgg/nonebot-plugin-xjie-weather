'''
coding: UTF-8
Author: AwAjie
Date: 2024-08-16 17:06:12
'''
import sqlite3
from pathlib import Path


# 连接SQLite数据库
class DatabaseManager:
    def __init__(self):
        db_path = Path(__file__).resolve().parent / 'src/db/region.db'
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def city_lnglat(self, value: str, key="name"):
        self.cursor.execute(f'SELECT lng, lat FROM region WHERE {key} LIKE ?', (f'{value}%',))
        row = self.cursor.fetchone()
        if row:
            return row
        else:
            return None

    def close(self):
        self.cursor.close()
        self.conn.close()
