import sqlite3

class Database:
    def __init__(self, db_name="employees.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                gender TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def insert_employee(self, emp_id, name, role, gender, status):
        try:
            self.cursor.execute("INSERT INTO employees VALUES (?, ?, ?, ?, ?)",
                                (emp_id, name, role, gender, status))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def fetch_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()

    def delete_employee(self, emp_id):
        self.cursor.execute("DELETE FROM employees WHERE id=?", (emp_id,))
        self.conn.commit()

    def update_employee(self, emp_id, name, role, gender, status):
        self.cursor.execute("""
            UPDATE employees SET name=?, role=?, gender=?, status=? WHERE id=?
        """, (name, role, gender, status, emp_id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
