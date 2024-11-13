# -*- coding: utf8 -*-
import pymysql
from source.database.database import DB_Connection
from colorama import Fore


class DB_member_check:
    def __init__(self):
        self.db_conn = DB_Connection()
        self.cursor = self.db_conn.db.cursor()

    async def member_check(self, member_id):
        try:
            self.cursor.execute("SELECT * FROM members WHERE member_id = %s", (member_id,))
            existing_id_profile = self.cursor.fetchone()

            if not existing_id_profile:
                self.cursor.execute("INSERT INTO members (member_id) VALUES (%s)", (member_id,))
                self.db_conn.db.commit()

                return "doesnt exist"
            else:
                return "exist"

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.db_conn.db.rollback()
            return False

        finally:
            self.db_conn.db.close()
