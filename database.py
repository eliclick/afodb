import sqlite3
import getpass

class Database:
    def __init__(self, db_name="employees.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.create_history_table()
        self.check_schema()
        self.migrate_table()
        self.CURRENT_APP_USER = getpass.getuser()

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

    def create_history_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                action TEXT,
                details TEXT,
                editor TEXT
            )
        """)
        self.conn.commit()

    def log_event(self, action, details, editor):
        self.cursor.execute("INSERT INTO history (action, details, editor) VALUES (?, ?, ?)", (action, details, editor))
        self.conn.commit()

    def fetch_history(self):
        self.cursor.execute("SELECT * FROM history ORDER BY timestamp DESC, id DESC")
        return self.cursor.fetchall()

    def insert_employee(self, email, fname, lname, role, company, status, termed="No"):
        try:
            self.cursor.execute("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (email, fname, lname, role, company, status, termed))
            self.conn.commit()
            self.log_event("Employee Added", f"Added employee: {email}", self.CURRENT_APP_USER)
            return True
        except sqlite3.IntegrityError:
            return False

    def search_employees(self, query):
        q = f"%{query}%"
        self.cursor.execute("""
            SELECT * FROM employees WHERE
            email LIKE ? OR
            fname LIKE ? OR
            lname LIKE ? OR
            role LIKE ? OR
            company LIKE ? OR
            status LIKE ? OR
            termed LIKE ?
        """, (q, q, q, q, q, q, q))
        return self.cursor.fetchall()

    def fetch_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()

    def delete_employee(self, email):
        self.cursor.execute("DELETE FROM employees WHERE email=?", (email,))
        self.conn.commit()
        self.log_event("Employee Deleted", f"Deleted employee: {email}", self.CURRENT_APP_USER)

    def update_employee(self, email, fname, lname, role, company, status):
        self.cursor.execute("""
            UPDATE employees SET fname=?, lname=?, role=?, company=?, status=? WHERE email=?
        """, (fname, lname, role, company, status, email))
        self.conn.commit()
        self.log_event("Employee Updated", f"Updated employee: {email}", self.CURRENT_APP_USER)

    def term_employee(self, email):
        self.cursor.execute("UPDATE employees SET termed='Yes' WHERE email=?", (email,))
        self.conn.commit()
        self.log_event("Employee Termed", f"Termed employee: {email}", self.CURRENT_APP_USER)

    def __del__(self):
        self.conn.close()
