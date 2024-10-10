'''
coding: UTF-8
Author: AwAjie
Date: 2024-08-16 17:06:12
'''
import sqlite3
from pathlib import Path


# 连接SQLite数据库

class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path(__file__).resolve().parent / 'db/region.db'
        self.conn = sqlite3.connect(db_path, timeout=10)  # 设置连接超时
        self.cursor = self.conn.cursor()

    def city_lnglat(self, value: str, key="name"):
        try:
            query = f'SELECT {key}, lng, lat FROM region WHERE {key} LIKE ?'
            self.cursor.execute(query, (value + '%',))
            row = self.cursor.fetchall()
            return row
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def close(self):
        self.cursor.close()
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
