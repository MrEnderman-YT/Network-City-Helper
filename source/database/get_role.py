# -*- coding: utf8 -*-
import pymysql
from source.database.database import DB_Connection
from colorama import Fore


class DB_role_get:
    def __init__(self):
        self.db_conn = DB_Connection()
        self.cursor = self.db_conn.db.cursor()

    async def role_get(self, member_id):
        try:
            self.cursor.execute("SELECT role FROM members WHERE member_id = %s", (member_id,))
            existing_role = self.cursor.fetchone()

            existing_role = existing_role["role"]

            if not existing_role:
                return "doesnt exist"

            else:
                if existing_role == "admin" or "Admin":
                    return "admin"
                elif existing_role == "teacher" or "Teacher":
                    return "teacher"
                elif existing_role == "student" or "Student":
                    return "student"
                else:
                    return "none"

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.db_conn.db.rollback()
            return False

        finally:
            self.db_conn.db.close()
