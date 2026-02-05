import firebase_admin
from firebase_admin import firestore
import getpass

class Database:
    def __init__(self, db=None):
        self.db = db
        self.CURRENT_APP_USER = getpass.getuser()

    def log_event(self, action, details, editor):
        self.db.collection('history').add({
            'action': action,
            'details': details,
            'editor': editor,
            'timestamp': firestore.SERVER_TIMESTAMP
        })

    def fetch_history(self):
        docs = self.db.collection('history').order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
        history = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            history.append(data)
        return history

    def insert_employee(self, email, fname, lname, role, company, status, termed="No"):
        doc_ref = self.db.collection('employees').document(email)
        if doc_ref.get().exists:
            return False

        doc_ref.set({
            'email': email,
            'fname': fname,
            'lname': lname,
            'role': role,
            'company': company,
            'status': status,
            'termed': termed
        })
        self.log_event("Employee Added", f"Added employee: {email}", self.CURRENT_APP_USER)
        return True

    def search_employees(self, query):
        query = query.lower()
        all_docs = self.fetch_employees()
        results = []
        for emp in all_docs:
            # Check if query is in any of the string values of the employee record
            values = [str(v).lower() for v in emp.values()]
            if any(query in v for v in values):
                results.append(emp)
        return results

    def fetch_employees(self):
        docs = self.db.collection('employees').stream()
        return [doc.to_dict() for doc in docs]

    def delete_employee(self, email):
        self.db.collection('employees').document(email).delete()
        self.log_event("Employee Deleted", f"Deleted employee: {email}", self.CURRENT_APP_USER)

    def update_employee(self, email, fname, lname, role, company, status):
        self.db.collection('employees').document(email).update({
            'fname': fname,
            'lname': lname,
            'role': role,
            'company': company,
            'status': status
        })
        self.log_event("Employee Updated", f"Updated employee: {email}", self.CURRENT_APP_USER)

    def term_employee(self, email):
        self.db.collection('employees').document(email).update({'termed': 'Yes'})
        self.log_event("Employee Termed", f"Termed employee: {email}", self.CURRENT_APP_USER)
