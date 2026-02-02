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
        self.db.insert_employee("john.doe@example.com", "John", "Doe", "Software Engineer", "Custom Air", "Active")
        employees = self.db.fetch_employees()
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0], ("john.doe@example.com", "John", "Doe", "Software Engineer", "Custom Air", "Active", "No"))

    def test_term_employee(self):
        self.db.insert_employee("john.doe@example.com", "John", "Doe", "Software Engineer", "Custom Air", "Active")
        self.db.term_employee("john.doe@example.com")
        employees = self.db.fetch_employees()
        self.assertEqual(employees[0][-1], "Yes")

    def test_duplicate_email(self):
        self.db.insert_employee("john.doe@example.com", "John", "Doe", "Software Engineer", "Custom Air", "Active")
        result = self.db.insert_employee("john.doe@example.com", "Jane", "Doe", "Manager", "Troy Filters", "Active")
        self.assertFalse(result)
        employees = self.db.fetch_employees()
        self.assertEqual(len(employees), 1)

    def test_search_employees(self):
        self.db.insert_employee("alice@example.com", "Alice", "Wonderland", "Explorer", "Fantasy Inc", "Active")
        self.db.insert_employee("bob@example.com", "Bob", "Builder", "Construction", "BuildCo", "Active")

        # Test exact match
        results = self.db.search_employees("Alice")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "Alice")

        # Test partial match
        results = self.db.search_employees("Build")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][2], "Builder")

        # Test match in different field (email)
        results = self.db.search_employees("example.com")
        self.assertEqual(len(results), 2)

        # Test no match
        results = self.db.search_employees("Charlie")
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
