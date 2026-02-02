import sqlite3

class Database:
    def __init__(self, db_name="employees.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.create_history_table()
        self.migrate_table()

    def create_history_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                action TEXT NOT NULL,
                details TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                email TEXT PRIMARY KEY,
                fname TEXT NOT NULL,
                lname TEXT NOT NULL,
                role TEXT NOT NULL,
                company TEXT NOT NULL,
                status TEXT NOT NULL,
                termed TEXT DEFAULT 'No'
            )
        """)
        self.conn.commit()

    def migrate_table(self):
        """Adds 'termed' column if it doesn't exist."""
        try:
            self.cursor.execute("ALTER TABLE employees ADD COLUMN termed TEXT DEFAULT 'No'")
            self.conn.commit()
        except sqlite3.OperationalError:
            # Column likely already exists
            pass

    def insert_employee(self, email, fname, lname, role, company, status, termed="No"):
        try:
            self.cursor.execute("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (email, fname, lname, role, company, status, termed))
            self.log_event("Employee Added", f"Added employee: {email}")
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False

    def fetch_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()

    def delete_employee(self, email):
        self.cursor.execute("DELETE FROM employees WHERE email=?", (email,))
        self.log_event("Employee Deleted", f"Deleted employee: {email}")
        self.conn.commit()

    def update_employee(self, email, fname, lname, role, company, status):
        self.cursor.execute("""
            UPDATE employees SET fname=?, lname=?, role=?, company=?, status=? WHERE email=?
        """, (fname, lname, role, company, status, email))
        self.log_event("Employee Updated", f"Updated employee: {email}")
        self.conn.commit()

    def term_employee(self, email):
        self.cursor.execute("UPDATE employees SET termed='Yes' WHERE email=?", (email,))
        self.log_event("Employee Termed", f"Termed employee: {email}")
        self.conn.commit()

    def log_event(self, action, details):
        self.cursor.execute("INSERT INTO history (action, details) VALUES (?, ?)", (action, details))

    def fetch_history(self):
        self.cursor.execute("SELECT * FROM history ORDER BY timestamp DESC, id DESC")
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()
