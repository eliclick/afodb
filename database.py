import sqlite3

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
        self.conn.commit()

    def insert_employee(self, email, fname, lname, role, company, status):
        try:
            self.cursor.execute("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?)",
                                (email, fname, lname, role, company, status))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def fetch_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()

    def delete_employee(self, email):
        self.cursor.execute("DELETE FROM employees WHERE email=?", (email,))
        self.conn.commit()

    def update_employee(self, email, fname, lname, role, company, status):
        self.cursor.execute("""
            UPDATE employees SET fname=?, lname=?, role=?, company=?, status=? WHERE email=?
        """, (fname, lname, role, company, status, email))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
