import pymysql
from source.database.database import DB_Connection
from colorama import Fore


class DB_notification_add:
    def __init__(self):
        self.db_conn = DB_Connection()
        self.cursor = self.db_conn.db.cursor()

    async def notification_add(self, member_id, column_id):
        try:
            self.cursor.execute(f"UPDATE members SET {column_id} = CASE {column_id} WHEN 1 THEN 0 WHEN 0 THEN 1 ELSE {column_id} END WHERE member_id = %s", (member_id,))
            self.db_conn.db.commit()
            return "ok"

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.db_conn.db.rollback()
            return False

        finally:
            self.db_conn.db.close()



