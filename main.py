#!/usr/bin/env python3
import customtkinter as ctk
from tkinter import ttk, messagebox
from database import Database

# Set theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Employee Management System")
        self.geometry("900x600")
        self.db = Database()

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # Form Frame
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.create_form()

        # Table Frame
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.create_table()
        
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

        # Add Button
        self.btn_add = ctk.CTkButton(self.form_frame, text="Add Employee", command=self.add_employee)
        self.btn_add.pack(pady=20, padx=20, fill="x")
        
        # Clear Button
        self.btn_clear = ctk.CTkButton(self.form_frame, text="Clear", command=self.clear_form, fg_color="gray")
        self.btn_clear.pack(pady=5, padx=20, fill="x")

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
        
        columns = ("email", "fname", "lname", "role", "company", "status")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        
        self.tree.heading("email", text="Email")
        self.tree.heading("fname", text="First Name")
        self.tree.heading("lname", text="Last Name")
        self.tree.heading("role", text="Role")
        self.tree.heading("company", text="Company")
        self.tree.heading("status", text="Status")

        self.tree.column("email", width=250)
        self.tree.column("fname", width=100)
        self.tree.column("lname", width=100)
        self.tree.column("role", width=150)
        self.tree.column("company", width=100)
        self.tree.column("status", width=100)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

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

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        employees = self.db.fetch_employees()
        for emp in employees:
            self.tree.insert("", "end", values=emp)

if __name__ == "__main__":
    app = App()
    app.mainloop()
