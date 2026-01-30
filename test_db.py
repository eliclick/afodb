import os
import unittest
from database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db_name = "test_employees.db"
        self.db = Database(self.db_name)

    def tearDown(self):
        del self.db
        if os.path.exists(self.db_name):
            os.remove(self.db_name)

    def test_insert_and_fetch_employee(self):
        self.db.insert_employee("1", "John Doe", "Software Engineer", "Male", "Active")
        employees = self.db.fetch_employees()
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0], ("1", "John Doe", "Software Engineer", "Male", "Active"))

    def test_duplicate_id(self):
        self.db.insert_employee("1", "John Doe", "Software Engineer", "Male", "Active")
        result = self.db.insert_employee("1", "Jane Doe", "Manager", "Female", "Active")
        self.assertFalse(result)
        employees = self.db.fetch_employees()
        self.assertEqual(len(employees), 1)

if __name__ == '__main__':
    unittest.main()
