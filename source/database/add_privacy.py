import pymysql
from source.database.database import DB_Connection
from colorama import Fore


class DB_privacy_add:
    def __init__(self):
        self.db_conn = DB_Connection()
        self.cursor = self.db_conn.db.cursor()

    async def privacy_add(self, member_id):
        try:
            self.cursor.execute(f"UPDATE members SET privacy_policy = 1 WHERE member_id = %s", (member_id,))
            self.db_conn.db.commit()
            return "ok"

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.db_conn.db.rollback()
            return False

        finally:
            self.db_conn.db.close()





