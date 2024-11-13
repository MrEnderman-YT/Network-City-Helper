# -*- coding: utf8 -*-
import pymysql
from source.database.database import DB_Connection
from colorama import Fore


class DB_role_add:
    def __init__(self):
        self.db_conn = DB_Connection()
        self.cursor = self.db_conn.db.cursor()

    async def role_add(self, member_id, role):
        try:

            self.cursor.execute(
                "UPDATE members SET role = %s WHERE member_id = %s",
                (role, member_id,)
            )
            self.db_conn.db.commit()
            return "ok"

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.db_conn.db.rollback()
            return False

        finally:
            self.db_conn.db.close()
