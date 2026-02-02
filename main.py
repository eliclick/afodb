#!/usr/bin/env python3
import customtkinter as ctk
from tkinter import ttk, messagebox
from database import Database

# Set theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class EmployeeTable(ctk.CTkFrame):
    def __init__(self, master, columns=None, **kwargs):
        super().__init__(master, **kwargs)
        self.columns = columns or ("email", "fname", "lname", "role", "company", "status", "termed")
        self.create_table()

    def create_table(self):
        # Treeview Style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

        self.tree = ttk.Treeview(self, columns=self.columns, show="headings", selectmode="browse")

        # Define headings
        if "email" in self.columns:
            self.tree.heading("email", text="Email")
            self.tree.column("email", width=250)
        if "fname" in self.columns:
            self.tree.heading("fname", text="First Name")
            self.tree.column("fname", width=100)
        if "lname" in self.columns:
            self.tree.heading("lname", text="Last Name")
            self.tree.column("lname", width=100)
        if "role" in self.columns:
            self.tree.heading("role", text="Role")
            self.tree.column("role", width=150)
        if "company" in self.columns:
            self.tree.heading("company", text="Company")
            self.tree.column("company", width=100)
        if "status" in self.columns:
            self.tree.heading("status", text="Status")
            self.tree.column("status", width=100)
        if "termed" in self.columns:
            self.tree.heading("termed", text="Termed")
            self.tree.column("termed", width=80)
        if "id" in self.columns:
             self.tree.heading("id", text="ID")
             self.tree.column("id", width=50)
        if "timestamp" in self.columns:
             self.tree.heading("timestamp", text="Timestamp")
             self.tree.column("timestamp", width=150)
        if "action" in self.columns:
             self.tree.heading("action", text="Action")
             self.tree.column("action", width=100)
        if "details" in self.columns:
             self.tree.heading("details", text="Details")
             self.tree.column("details", width=500)

        # Highlight termed employees
        self.tree.tag_configure('termed', background='red', foreground='white')

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_data(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in data:
            tags = ()
            # Highlight if termed. Assuming standard employee tuple structure.
            # Check if 'termed' is in columns to avoid doing this for history table
            if "termed" in self.columns and len(row) > 6 and row[6] == "Yes":
                tags = ('termed',)
            self.tree.insert("", "end", values=row, tags=tags)

    def get_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            return self.tree.item(selected_item[0])['values']
        return None

class MainMenu(ctk.CTkFrame):
    def __init__(self, master, open_add_user_callback, open_edit_user_callback, open_term_user_callback, open_history_callback):
        super().__init__(master)
        self.open_add_user_callback = open_add_user_callback
        self.open_edit_user_callback = open_edit_user_callback
        self.open_term_user_callback = open_term_user_callback
        self.open_history_callback = open_history_callback

        # Center content
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        self.label_title = ctk.CTkLabel(self, text="AFO IT DB", font=("Arial", 24, "bold"))
        self.label_title.grid(row=1, column=0, padx=20, pady=(20, 10))

        self.btn_add_user = ctk.CTkButton(self, text="Add Employee", command=self.open_add_user_callback, font=("Arial", 16))
        self.btn_add_user.grid(row=2, column=0, padx=20, pady=10)

        self.btn_edit_user = ctk.CTkButton(self, text="Edit Employees", command=self.open_edit_user_callback, font=("Arial", 16))
        self.btn_edit_user.grid(row=3, column=0, padx=20, pady=10)

        self.btn_term_user = ctk.CTkButton(self, text="Term Employee", command=self.open_term_user_callback, font=("Arial", 16))
        self.btn_term_user.grid(row=4, column=0, padx=20, pady=10)

        self.btn_history = ctk.CTkButton(self, text="History", command=self.open_history_callback, font=("Arial", 16))
        self.btn_history.grid(row=5, column=0, padx=20, pady=(10, 20))

class EmployeeView(ctk.CTkFrame):
    def __init__(self, master, db, back_callback):
        super().__init__(master)
        self.db = db
        self.back_callback = back_callback

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1) # Form and Table
        self.grid_rowconfigure(1, weight=0) # Back button

        # Form Frame
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.create_form()

        # Table Frame
        self.table_frame = EmployeeTable(self)
        self.table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Back Button
        self.btn_back = ctk.CTkButton(self, text="Back to Menu", command=self.back_callback, fg_color="gray")
        self.btn_back.grid(row=1, column=0, columnspan=2, pady=10)

        # Load Data
        self.load_data()

    def create_form(self):
        self.label_heading = ctk.CTkLabel(self.form_frame, text="Add Employee", font=("Arial", 20, "bold"))
        self.label_heading.pack(pady=20)

        # Email
        self.entry_email = ctk.CTkEntry(self.form_frame, placeholder_text="Email")
        self.entry_email.pack(pady=10, padx=20, fill="x")

        # First Name
        self.entry_fname = ctk.CTkEntry(self.form_frame, placeholder_text="First Name")
        self.entry_fname.pack(pady=10, padx=20, fill="x")

        # Last Name
        self.entry_lname = ctk.CTkEntry(self.form_frame, placeholder_text="Last Name")
        self.entry_lname.pack(pady=10, padx=20, fill="x")

        # Role
        self.entry_role = ctk.CTkEntry(self.form_frame, placeholder_text="Role")
        self.entry_role.pack(pady=10, padx=20, fill="x")

        # Company
        self.combo_company = ctk.CTkComboBox(self.form_frame, values=["Air Force One", "Custom Air", "Troy Filters", "CMS Water Solutions"])
        self.combo_company.set("Company")
        self.combo_company.pack(pady=10, padx=20, fill="x")

        # Status
        self.combo_status = ctk.CTkComboBox(self.form_frame, values=["Active", "Inactive"])
        self.combo_status.set("Status")
        self.combo_status.pack(pady=10, padx=20, fill="x")

        # Termed
        self.combo_termed = ctk.CTkComboBox(self.form_frame, values=["No", "Yes"])
        self.combo_termed.set("No")
        self.combo_termed.pack(pady=10, padx=20, fill="x")

        # Add Button
        self.btn_add = ctk.CTkButton(self.form_frame, text="Add Employee", command=self.add_employee)
        self.btn_add.pack(pady=20, padx=20, fill="x")

        # Clear Button
        self.btn_clear = ctk.CTkButton(self.form_frame, text="Clear", command=self.clear_form, fg_color="gray")
        self.btn_clear.pack(pady=5, padx=20, fill="x")

    def add_employee(self):
        email = self.entry_email.get()
        fname = self.entry_fname.get()
        lname = self.entry_lname.get()
        role = self.entry_role.get()
        company = self.combo_company.get()
        status = self.combo_status.get()
        termed = self.combo_termed.get()

        if not (email and fname and lname and role and company != "Company" and status != "Status"):
            messagebox.showerror("Error", "All fields are required!")
            return

        if self.db.insert_employee(email, fname, lname, role, company, status, termed):
            messagebox.showinfo("Success", "Employee added successfully!")
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Error", "Email already exists!")

    def clear_form(self):
        self.entry_email.delete(0, 'end')
        self.entry_fname.delete(0, 'end')
        self.entry_lname.delete(0, 'end')
        self.entry_role.delete(0, 'end')
        self.combo_company.set("Company")
        self.combo_status.set("Status")
        self.combo_termed.set("No")

    def load_data(self):
        employees = self.db.fetch_employees()
        self.table_frame.load_data(employees)

class HistoryView(ctk.CTkFrame):
    def __init__(self, master, db, back_callback):
        super().__init__(master)
        self.db = db
        self.back_callback = back_callback

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.label_heading = ctk.CTkLabel(self, text="History Logs", font=("Arial", 20, "bold"))
        self.label_heading.grid(row=0, column=0, pady=10)

        self.table = EmployeeTable(self, columns=("id", "timestamp", "action", "details"))
        self.table.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Not setting column widths here because I moved them to EmployeeTable.create_table
        # based on column presence, but HistoryView had custom widths.
        # I'll re-apply them here to be safe and match original.
        self.table.tree.column("id", width=50)
        self.table.tree.column("timestamp", width=150)
        self.table.tree.column("action", width=100)
        self.table.tree.column("details", width=500)

        self.btn_back = ctk.CTkButton(self, text="Back to Menu", command=self.back_callback, fg_color="gray")
        self.btn_back.grid(row=2, column=0, pady=10)

        self.load_data()

    def load_data(self):
        history_data = self.db.fetch_history()
        self.table.load_data(history_data)

class EditEmployeesView(ctk.CTkFrame):
    def __init__(self, master, db, back_callback):
        super().__init__(master)
        self.db = db
        self.back_callback = back_callback

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Container for swapping views
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.create_list_view()
        self.create_edit_view()

        self.show_list_view()

    def create_list_view(self):
        self.list_frame = ctk.CTkFrame(self.container)
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(1, weight=1)

        self.label_list = ctk.CTkLabel(self.list_frame, text="Select Employee to Edit", font=("Arial", 20, "bold"))
        self.label_list.grid(row=0, column=0, pady=10)

        self.table = EmployeeTable(self.list_frame)
        self.table.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.btn_select = ctk.CTkButton(self.list_frame, text="Edit Selected", command=self.on_select)
        self.btn_select.grid(row=2, column=0, pady=10)

        self.btn_remove = ctk.CTkButton(self.list_frame, text="Remove Selected", command=self.on_remove, fg_color="firebrick")
        self.btn_remove.grid(row=3, column=0, pady=(0, 10))

        self.btn_back_list = ctk.CTkButton(self.list_frame, text="Back to Menu", command=self.back_callback, fg_color="gray")
        self.btn_back_list.grid(row=4, column=0, pady=10)

    def create_edit_view(self):
        self.edit_frame = ctk.CTkFrame(self.container)
        self.edit_frame.grid_columnconfigure(0, weight=1)

        self.label_edit = ctk.CTkLabel(self.edit_frame, text="Edit Employee", font=("Arial", 20, "bold"))
        self.label_edit.pack(pady=20)

        # Fields
        self.entry_email = ctk.CTkEntry(self.edit_frame, placeholder_text="Email (Read Only)")
        self.entry_email.pack(pady=10, padx=20, fill="x")
        self.entry_email.configure(state="disabled") # Email is PK, cannot change

        self.entry_fname = ctk.CTkEntry(self.edit_frame, placeholder_text="First Name")
        self.entry_fname.pack(pady=10, padx=20, fill="x")

        self.entry_lname = ctk.CTkEntry(self.edit_frame, placeholder_text="Last Name")
        self.entry_lname.pack(pady=10, padx=20, fill="x")

        self.entry_role = ctk.CTkEntry(self.edit_frame, placeholder_text="Role")
        self.entry_role.pack(pady=10, padx=20, fill="x")

        self.combo_company = ctk.CTkComboBox(self.edit_frame, values=["Air Force One", "Custom Air", "Troy Filters", "CMS Water Solutions"])
        self.combo_company.pack(pady=10, padx=20, fill="x")

        self.combo_status = ctk.CTkComboBox(self.edit_frame, values=["Active", "Inactive"])
        self.combo_status.pack(pady=10, padx=20, fill="x")

        self.combo_termed = ctk.CTkComboBox(self.edit_frame, values=["No", "Yes"])
        self.combo_termed.pack(pady=10, padx=20, fill="x")

        self.btn_save = ctk.CTkButton(self.edit_frame, text="Save Changes", command=self.save_changes)
        self.btn_save.pack(pady=20, padx=20, fill="x")

        self.btn_cancel = ctk.CTkButton(self.edit_frame, text="Cancel", command=self.show_list_view, fg_color="gray")
        self.btn_cancel.pack(pady=5, padx=20, fill="x")

    def show_list_view(self):
        self.edit_frame.pack_forget()
        self.list_frame.pack(fill="both", expand=True)
        self.load_data()

    def show_edit_view(self, employee):
        self.list_frame.pack_forget()
        self.edit_frame.pack(fill="both", expand=True)

        # Populate fields
        self.entry_email.configure(state="normal")
        self.entry_email.delete(0, 'end')
        self.entry_email.insert(0, employee[0])
        self.entry_email.configure(state="disabled")

        self.entry_fname.delete(0, 'end')
        self.entry_fname.insert(0, employee[1])

        self.entry_lname.delete(0, 'end')
        self.entry_lname.insert(0, employee[2])

        self.entry_role.delete(0, 'end')
        self.entry_role.insert(0, employee[3])

        self.combo_company.set(employee[4])
        self.combo_status.set(employee[5])
        self.combo_termed.set(employee[6])

    def load_data(self):
        employees = self.db.fetch_employees()
        self.table.load_data(employees)

    def on_select(self):
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Warning", "Please select an employee first.")
            return
        self.show_edit_view(selected)

    def on_remove(self):
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Warning", "Please select an employee first.")
            return

        email = selected[0]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to remove {email}?")
        if confirm:
            if self.db.delete_employee(email):
                messagebox.showinfo("Success", "Employee removed.")
                self.load_data()
            else:
                messagebox.showerror("Error", "Failed to remove employee.")

    def save_changes(self):
        email = self.entry_email.get()
        fname = self.entry_fname.get()
        lname = self.entry_lname.get()
        role = self.entry_role.get()
        company = self.combo_company.get()
        status = self.combo_status.get()
        termed = self.combo_termed.get()

        if self.db.update_employee(email, fname, lname, role, company, status, termed):
            messagebox.showinfo("Success", "Employee updated.")
            self.show_list_view()
        else:
            messagebox.showerror("Error", "Failed to update employee.")

class TermEmployeeView(ctk.CTkFrame):
    def __init__(self, master, db, back_callback):
        super().__init__(master)
        self.db = db
        self.back_callback = back_callback

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.label_heading = ctk.CTkLabel(self, text="Select Employee to Terminate", font=("Arial", 20, "bold"))
        self.label_heading.grid(row=0, column=0, pady=10)

        self.table = EmployeeTable(self)
        self.table.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.btn_term = ctk.CTkButton(self, text="Term Selected", command=self.on_term, fg_color="firebrick")
        self.btn_term.grid(row=2, column=0, pady=10)

        self.btn_back = ctk.CTkButton(self, text="Back to Menu", command=self.back_callback, fg_color="gray")
        self.btn_back.grid(row=3, column=0, pady=10)

        self.load_data()

    def load_data(self):
        employees = self.db.fetch_employees()
        self.table.load_data(employees)

    def on_term(self):
        selected = self.table.get_selected()
        if not selected:
            messagebox.showwarning("Warning", "Please select an employee first.")
            return

        email = selected[0]

        # Check if already termed
        if len(selected) > 6 and selected[6] == "Yes":
             messagebox.showinfo("Info", "Employee is already termed.")
             return

        confirm = messagebox.askyesno("Confirm Term", f"Are you sure you want to terminate {email}?")
        if confirm:
            fname = selected[1]
            lname = selected[2]
            role = selected[3]
            company = selected[4]
            status = selected[5]
            termed = "Yes"

            if self.db.update_employee(email, fname, lname, role, company, status, termed):
                messagebox.showinfo("Success", "Employee termed.")
                self.load_data()
            else:
                messagebox.showerror("Error", "Failed to term employee.")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AFO IT DB")
        self.geometry("900x600")
        self.db = Database()

        self.current_frame = None
        self.show_main_menu()

    def switch_frame(self, frame_class, **kwargs):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = frame_class(self, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

    def show_main_menu(self):
        self.switch_frame(MainMenu,
                          open_add_user_callback=self.show_employee_view,
                          open_edit_user_callback=self.show_edit_employees_view,
                          open_term_user_callback=self.show_term_employee_view,
                          open_history_callback=self.show_history_view)

    def show_employee_view(self):
        self.switch_frame(EmployeeView, db=self.db, back_callback=self.show_main_menu)

    def show_edit_employees_view(self):
        self.switch_frame(EditEmployeesView, db=self.db, back_callback=self.show_main_menu)

    def show_term_employee_view(self):
        self.switch_frame(TermEmployeeView, db=self.db, back_callback=self.show_main_menu)

    def show_history_view(self):
        self.switch_frame(HistoryView, db=self.db, back_callback=self.show_main_menu)

if __name__ == "__main__":
    app = App()
    app.mainloop()
