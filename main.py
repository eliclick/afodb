#!/usr/bin/env python3
import customtkinter as ctk
from tkinter import ttk, messagebox
from database import Database

# Set theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class EmployeeTable(ctk.CTkFrame):
    def __init__(self, master, db):
        super().__init__(master)
        self.db = db
        self.create_table()
        self.load_data()

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

        columns = ("email", "fname", "lname", "role", "company", "status", "termed")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        self.tree.heading("email", text="Email")
        self.tree.heading("fname", text="First Name")
        self.tree.heading("lname", text="Last Name")
        self.tree.heading("role", text="Role")
        self.tree.heading("company", text="Company")
        self.tree.heading("status", text="Status")
        self.tree.heading("termed", text="Termed")

        self.tree.column("email", width=250)
        self.tree.column("fname", width=100)
        self.tree.column("lname", width=100)
        self.tree.column("role", width=150)
        self.tree.column("company", width=100)
        self.tree.column("status", width=100)
        self.tree.column("termed", width=80)

        self.tree.tag_configure("termed", background="#D32F2F", foreground="white")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        employees = self.db.fetch_employees()
        for emp in employees:
            tags = ()
            if len(emp) > 6 and emp[6] == "Yes":
                tags = ("termed",)
            self.tree.insert("", "end", values=emp, tags=tags)

    def get_selected_email(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return None
        item = self.tree.item(selected_item)
        values = item['values']
        return values[0]

class MainMenu(ctk.CTkFrame):
    def __init__(self, master, open_add_user_callback, open_term_user_callback):
        super().__init__(master)
        self.open_add_user_callback = open_add_user_callback
        self.open_term_user_callback = open_term_user_callback

        # Center content
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1)

        # Title
        self.label_title = ctk.CTkLabel(self, text="AFO IT DB", font=("Arial", 24, "bold"))
        self.label_title.grid(row=0, column=0, pady=20, sticky="n")

        self.btn_add_user = ctk.CTkButton(self, text="Add new user", command=self.open_add_user_callback, font=("Arial", 16))
        self.btn_add_user.grid(row=2, column=0, padx=20, pady=20)

        self.btn_term_user = ctk.CTkButton(self, text="Term a user", command=self.open_term_user_callback, font=("Arial", 16))
        self.btn_term_user.grid(row=3, column=0, padx=20, pady=20)

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
        self.table_frame = EmployeeTable(self, self.db)
        self.table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Back Button
        self.btn_back = ctk.CTkButton(self, text="Back to Menu", command=self.back_callback, fg_color="gray")
        self.btn_back.grid(row=1, column=0, columnspan=2, pady=10)

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

        if not (email and fname and lname and role and company != "Company" and status != "Status"):
            messagebox.showerror("Error", "All fields are required!")
            return

        if self.db.insert_employee(email, fname, lname, role, company, status):
            messagebox.showinfo("Success", "Employee added successfully!")
            self.clear_form()
            self.table_frame.load_data()
        else:
            messagebox.showerror("Error", "Email already exists!")

    def clear_form(self):
        self.entry_email.delete(0, 'end')
        self.entry_fname.delete(0, 'end')
        self.entry_lname.delete(0, 'end')
        self.entry_role.delete(0, 'end')
        self.combo_company.set("Company")
        self.combo_status.set("Status")

class TermUserView(ctk.CTkFrame):
    def __init__(self, master, db, back_callback):
        super().__init__(master)
        self.db = db
        self.back_callback = back_callback

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Table
        self.grid_rowconfigure(1, weight=0) # Button
        self.grid_rowconfigure(2, weight=0) # Back button

        # Table Frame
        self.table_frame = EmployeeTable(self, self.db)
        self.table_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Term Button
        self.btn_term = ctk.CTkButton(self, text="Term Selected User", command=self.term_user, fg_color="#D32F2F", hover_color="#B71C1C")
        self.btn_term.grid(row=1, column=0, pady=10)

        # Back Button
        self.btn_back = ctk.CTkButton(self, text="Back to Menu", command=self.back_callback, fg_color="gray")
        self.btn_back.grid(row=2, column=0, pady=10)

    def term_user(self):
        email = self.table_frame.get_selected_email()
        if not email:
            messagebox.showerror("Error", "Please select a user to term.")
            return

        self.db.term_employee(email)
        messagebox.showinfo("Success", f"User {email} has been termed.")
        self.table_frame.load_data()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Employee Management System")
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
        self.switch_frame(MainMenu, open_add_user_callback=self.show_employee_view, open_term_user_callback=self.show_term_user_view)

    def show_employee_view(self):
        self.switch_frame(EmployeeView, db=self.db, back_callback=self.show_main_menu)

    def show_term_user_view(self):
        self.switch_frame(TermUserView, db=self.db, back_callback=self.show_main_menu)

if __name__ == "__main__":
    app = App()
    app.mainloop()
