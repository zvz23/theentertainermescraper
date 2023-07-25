import sqlite3

class WebScraperDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.table = 'items'
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.row_factory = sqlite3.Row
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()
    
    def init_db(self):
        self.cursor.execute("""
            CREATE TABLE items (
            ID   INTEGER NOT NULL
                        PRIMARY KEY AUTOINCREMENT,
            URL  TEXT    NOT NULL
                        UNIQUE,
            INFO TEXT
        );
    """)
        self.conn.commit()
        print("Database initialized")

    def get_all(self):
        self.cursor.execute(f"SELECT * FROM {self.table}")
        return self.cursor.fetchall()

    def get_all_without_info(self):
        self.cursor.execute(f"SELECT * FROM {self.table} WHERE INFO IS NULL")
        return self.cursor.fetchall()
    
    def get_all_with_info(self):
        self.cursor.execute(f"SELECT * FROM {self.table} WHERE INFO IS NOT NULL")
        return self.cursor.fetchall()

    def save_url(self, url: str):
        self.cursor.execute(f"INSERT OR IGNORE INTO {self.table}(URL) VALUES(?)", [url])

    def save_urls(self, urls: list):
        self.cursor.executemany(f"INSERT OR IGNORE INTO {self.table}(URL) VALUES(?)", urls)

    def set_info(self, id: int, info: str):
        self.cursor.execute(f"UPDATE {self.table} SET INFO=? WHERE ID=?", [info, id])


if __name__ == '__main__':
    with WebScraperDB('theentertainerme.db') as conn:
        conn.init_db()