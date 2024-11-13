# -*- coding: utf8 -*-
import pymysql
from source.database.database import DB_Connection
from colorama import Fore


class DB_auth_add:
    def __init__(self):
        self.db_conn = DB_Connection()
        self.cursor = self.db_conn.db.cursor()

    async def auth_add(self, member_id, login=None, password=None, role=None, name=None, surname=None, clas=None, mode="Full"):
        try:

            if mode == "Full":
                self.cursor.execute(
                    "UPDATE members SET login = %s, password = %s, role = %s, name = %s, surname = %s, class = %s WHERE member_id = %s",
                    (login, password, role, name, surname, clas, member_id,)
                )
                self.db_conn.db.commit()
                return "ok"

            elif mode == "OnlyLogin":
                self.cursor.execute(
                    "UPDATE members SET login = %s, role = %s, name = %s, surname = %s, class = %s WHERE member_id = %s",
                    (login, role, name, surname, clas, member_id,)
                )
                self.db_conn.db.commit()
                return "ok"

            elif mode == "OnlyPassword":
                self.cursor.execute(
                    "UPDATE members SET password = %s, role = %s, name = %s, surname = %s, class = %s WHERE member_id = %s",
                    (password, role, name, surname, clas, member_id,)
                )
                self.db_conn.db.commit()
                return "ok"

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.db_conn.db.rollback()
            return False

        finally:
            self.db_conn.db.close()
