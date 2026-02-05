import unittest
from unittest.mock import MagicMock, patch
from database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.db = Database(self.mock_db)

    def test_insert_and_fetch_employee(self):
        # Setup mock for insert
        doc_ref = self.mock_db.collection.return_value.document.return_value
        doc_ref.get.return_value.exists = False

        # Setup mock for fetch
        mock_doc = MagicMock()
        mock_doc.to_dict.return_value = {
            "email": "john.doe@example.com",
            "fname": "John",
            "lname": "Doe",
            "role": "Software Engineer",
            "company": "Custom Air",
            "status": "Active",
            "termed": "No"
        }
        # When fetch_employees is called, it calls collection('employees').stream()
        # We need to make sure the mock returns the list of docs
        self.mock_db.collection.return_value.stream.return_value = [mock_doc]

        # Execute
        self.db.insert_employee("john.doe@example.com", "John", "Doe", "Software Engineer", "Custom Air", "Active")
        employees = self.db.fetch_employees()

        # Verify
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0]['email'], "john.doe@example.com")
        self.assertEqual(employees[0]['fname'], "John")

        # Verify insert called correct set
        # Check if collection('employees') was called
        # self.mock_db.collection.assert_any_call('employees') # This might be tricky if multiple calls to collection happen

        # Check specific document set
        doc_ref.set.assert_called_with({
            'email': "john.doe@example.com",
            'fname': "John",
            'lname': "Doe",
            'role': "Software Engineer",
            'company': "Custom Air",
            'status': "Active",
            'termed': "No"
        })

    def test_term_employee(self):
        self.db.term_employee("john.doe@example.com")

        doc_ref = self.mock_db.collection.return_value.document.return_value
        doc_ref.update.assert_called_with({'termed': 'Yes'})

    def test_duplicate_email(self):
        # Setup mock to say it exists
        doc_ref = self.mock_db.collection.return_value.document.return_value
        doc_ref.get.return_value.exists = True

        result = self.db.insert_employee("john.doe@example.com", "Jane", "Doe", "Manager", "Troy Filters", "Active")
        self.assertFalse(result)

        # Ensure set was NOT called
        doc_ref.set.assert_not_called()

    def test_search_employees(self):
        # Mock data
        emp1 = {"email": "alice@example.com", "fname": "Alice", "lname": "Wonderland", "role": "Explorer", "company": "Fantasy Inc", "status": "Active", "termed": "No"}
        emp2 = {"email": "bob@example.com", "fname": "Bob", "lname": "Builder", "role": "Construction", "company": "BuildCo", "status": "Active", "termed": "No"}

        mock_doc1 = MagicMock()
        mock_doc1.to_dict.return_value = emp1
        mock_doc2 = MagicMock()
        mock_doc2.to_dict.return_value = emp2

        self.mock_db.collection.return_value.stream.return_value = [mock_doc1, mock_doc2]

        # Test exact match
        results = self.db.search_employees("Alice")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['fname'], "Alice")

        # Test partial match
        results = self.db.search_employees("Build")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['lname'], "Builder")

        # Test match in different field (email)
        results = self.db.search_employees("example.com")
        self.assertEqual(len(results), 2)

        # Test no match
        results = self.db.search_employees("Charlie")
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
