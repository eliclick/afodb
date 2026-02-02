from database import Database
import os
import unittest

class TestHistory(unittest.TestCase):
    def setUp(self):
        self.db_name = "test_history.db"
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
        self.db = Database(self.db_name)

    def tearDown(self):
        del self.db
        if os.path.exists(self.db_name):
            os.remove(self.db_name)

    def test_logging(self):
        print("Adding employee...")
        self.db.insert_employee("test@example.com", "John", "Doe", "Developer", "AFO", "Active")

        print("Updating employee...")
        self.db.update_employee("test@example.com", "John", "Doe", "Senior Developer", "AFO", "Active")

        print("Terminating employee...")
        self.db.term_employee("test@example.com")

        print("Deleting employee...")
        self.db.delete_employee("test@example.com")

        history = self.db.fetch_history()
        self.assertEqual(len(history), 4)

        # history is ordered by timestamp DESC, so newest first
        self.assertEqual(history[0][2], "Employee Deleted")
        self.assertEqual(history[0][3], "Deleted employee: test@example.com")

        self.assertEqual(history[1][2], "Employee Termed")
        self.assertEqual(history[1][3], "Termed employee: test@example.com")

        self.assertEqual(history[2][2], "Employee Updated")
        self.assertEqual(history[2][3], "Updated employee: test@example.com")

        self.assertEqual(history[3][2], "Employee Added")
        self.assertEqual(history[3][3], "Added employee: test@example.com")

if __name__ == "__main__":
    unittest.main()
