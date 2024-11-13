# -*- coding: utf8 -*-
import pymysql
from source.database.database import DB_Connection
from colorama import Fore


class DB_profile_get:
    def __init__(self):
        self.db_conn = DB_Connection()
        self.cursor = self.db_conn.db.cursor()

    async def profile_get(self, member_id):
        try:
            self.cursor.execute("SELECT role, name, surname, class FROM members WHERE member_id = %s", (member_id,))
            existing_profile = self.cursor.fetchone()

            if not existing_profile:
                return "doesnt exist"

            else:
                return existing_profile

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.db_conn.db.rollback()
            return False

        finally:
            self.db_conn.db.close()
