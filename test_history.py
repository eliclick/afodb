from database import Database
import unittest
from unittest.mock import MagicMock

class TestHistory(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.db = Database(self.mock_db)

    def test_logging(self):
        # Setup return for fetch_history
        mock_docs = []
        actions = [
            ("Employee Deleted", "Deleted employee: test@example.com"),
            ("Employee Termed", "Termed employee: test@example.com"),
            ("Employee Updated", "Updated employee: test@example.com"),
            ("Employee Added", "Added employee: test@example.com")
        ]

        for i, (action, details) in enumerate(actions):
            m = MagicMock()
            m.to_dict.return_value = {
                "action": action,
                "details": details,
                "editor": "testuser",
                "timestamp": "2023-01-01"
            }
            m.id = f"doc{i}"
            mock_docs.append(m)

        self.mock_db.collection.return_value.order_by.return_value.stream.return_value = mock_docs

        # Ensure insert_employee thinks the user doesn't exist yet
        self.mock_db.collection.return_value.document.return_value.get.return_value.exists = False

        print("Adding employee...")
        self.db.insert_employee("test@example.com", "John", "Doe", "Developer", "AFO", "Active")

        print("Updating employee...")
        self.db.update_employee("test@example.com", "John", "Doe", "Senior Developer", "AFO", "Active")

        print("Terminating employee...")
        self.db.term_employee("test@example.com")

        print("Deleting employee...")
        self.db.delete_employee("test@example.com")

        # Verify adds were called (log_event uses .add())
        # insert uses .set(), update uses .update(), delete uses .delete()
        # So only log_event uses .add()
        self.assertEqual(self.mock_db.collection.return_value.add.call_count, 4)

        history = self.db.fetch_history()
        self.assertEqual(len(history), 4)

        # history is ordered by timestamp DESC, so newest first
        self.assertEqual(history[0]['action'], "Employee Deleted")
        self.assertEqual(history[0]['details'], "Deleted employee: test@example.com")

        self.assertEqual(history[1]['action'], "Employee Termed")
        self.assertEqual(history[1]['details'], "Termed employee: test@example.com")

        self.assertEqual(history[2]['action'], "Employee Updated")
        self.assertEqual(history[2]['details'], "Updated employee: test@example.com")

        self.assertEqual(history[3]['action'], "Employee Added")
        self.assertEqual(history[3]['details'], "Added employee: test@example.com")

if __name__ == "__main__":
    unittest.main()
