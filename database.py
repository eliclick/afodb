import sqlite3

class Database:
    def __init__(self, db_name="employees.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.check_schema()
        self.migrate_table()

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

    def check_schema(self):
        """Checks if the schema is valid (has 'email' column). If not, resets the table."""
        self.cursor.execute("PRAGMA table_info(employees)")
        columns = [col[1].lower() for col in self.cursor.fetchall()]

        # If table exists (columns not empty) but 'email' is missing
        if columns and 'email' not in columns:
            print("Warning: Corrupted database schema detected (missing 'email'). Backing up and recreating.")
            try:
                self.cursor.execute("ALTER TABLE employees RENAME TO employees_backup_corrupted")
                self.conn.commit()
            except sqlite3.OperationalError:
                # Backup might already exist, append random suffix or just fail safe
                pass
            self.create_table()

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

    def term_employee(self, email):
        self.cursor.execute("UPDATE employees SET termed='Yes' WHERE email=?", (email,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
