import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="employees.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                email TEXT PRIMARY KEY,
                fname TEXT NOT NULL,
                lname TEXT NOT NULL,
                role TEXT NOT NULL,
                company TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def insert_employee(self, email, fname, lname, role, company, status):
        try:
            self.cursor.execute("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?)",
                                (email, fname, lname, role, company, status))
            self.log_event("Insert", f"Added employee {email}")
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception:
            self.conn.rollback()
            return False

    def fetch_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()

    def delete_employee(self, email):
        try:
            self.cursor.execute("DELETE FROM employees WHERE email=?", (email,))
            if self.cursor.rowcount > 0:
                self.log_event("Delete", f"Deleted employee {email}")
                self.conn.commit()
                return True
            else:
                return False
        except Exception:
            self.conn.rollback()
            return False

    def update_employee(self, email, fname, lname, role, company, status):
        try:
            self.cursor.execute("""
                UPDATE employees SET fname=?, lname=?, role=?, company=?, status=? WHERE email=?
            """, (fname, lname, role, company, status, email))
            if self.cursor.rowcount > 0:
                self.log_event("Update", f"Updated employee {email}")
                self.conn.commit()
                return True
            else:
                return False
        except Exception:
            self.conn.rollback()
            return False

    def log_event(self, action, details):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO history (timestamp, action, details) VALUES (?, ?, ?)",
                            (timestamp, action, details))

    def fetch_history(self):
        self.cursor.execute("SELECT * FROM history ORDER BY id DESC")
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()
