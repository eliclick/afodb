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
        self.db.insert_employee("john.doe@example.com", "John", "Doe", "Software Engineer", "Custom Air", "Active", "No")
        employees = self.db.fetch_employees()
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0], ("john.doe@example.com", "John", "Doe", "Software Engineer", "Custom Air", "Active", "No"))

    def test_duplicate_email(self):
        self.db.insert_employee("john.doe@example.com", "John", "Doe", "Software Engineer", "Custom Air", "Active", "No")
        result = self.db.insert_employee("john.doe@example.com", "Jane", "Doe", "Manager", "Troy Filters", "Active", "No")
        self.assertFalse(result)
        employees = self.db.fetch_employees()
        self.assertEqual(len(employees), 1)

    def test_termed_field(self):
        self.db.insert_employee("jane.doe@example.com", "Jane", "Doe", "Manager", "Troy Filters", "Active", "Yes")
        employees = self.db.fetch_employees()
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0][6], "Yes")

        # Update termed status
        self.db.update_employee("jane.doe@example.com", "Jane", "Doe", "Manager", "Troy Filters", "Active", "No")
        employees = self.db.fetch_employees()
        self.assertEqual(employees[0][6], "No")

if __name__ == '__main__':
    unittest.main()
