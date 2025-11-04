import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# ---------------------------------------
# Data structure
# ---------------------------------------
students = []  # List of dictionaries


# ---------------------------------------
# Core functions
# ---------------------------------------
def add_student():
    name = simpledialog.askstring("Add Student", "Enter student name:")
    reg_no = simpledialog.askstring("Add Student", "Enter registration number:")
    grade = simpledialog.askfloat("Add Student", "Enter grade:")

    if name and reg_no and grade is not None:
        student = {"name": name, "reg_no": reg_no, "grade": grade}
        students.append(student)
        refresh_table()
        messagebox.showinfo("Success", f"Student '{name}' added successfully!")
    else:
        messagebox.showwarning("Input Error", "All fields are required!")


def view_students():
    refresh_table()
    if not students:
        messagebox.showinfo("Info", "No student records found.")


def search_student():
    key = simpledialog.askstring("Search", "Enter name or registration number:")
    if not key:
        return

    for s in students:
        if s["name"].lower() == key.lower() or s["reg_no"] == key:
            messagebox.showinfo(
                "Found",
                f"Name: {s['name']}\nReg No: {s['reg_no']}\nGrade: {s['grade']}"
            )
            return
    messagebox.showwarning("Not Found", "No student found with that information.")


def sort_students():
    n = len(students)
    if n < 2:
        messagebox.showinfo("Info", "Not enough records to sort.")
        return

    # Bubble sort algorithm
    for i in range(n - 1):
        for j in range(n - i - 1):
            if students[j]["grade"] > students[j + 1]["grade"]:
                students[j], students[j + 1] = students[j + 1], students[j]

    refresh_table()
    messagebox.showinfo("Sorted", "Students sorted by grade successfully!")


def delete_student():
    reg_no = simpledialog.askstring("Delete", "Enter registration number:")
    for s in students:
        if s["reg_no"] == reg_no:
            students.remove(s)
            refresh_table()
            messagebox.showinfo("Deleted", f"Student '{s['name']}' removed successfully!")
            return
    messagebox.showwarning("Not Found", "Student not found.")


# ---------------------------------------
# Table (Treeview) update function
# ---------------------------------------
def refresh_table():
    for row in table.get_children():
        table.delete(row)

    for s in students:
        table.insert("", "end", values=(s["name"], s["reg_no"], s["grade"]))


# ---------------------------------------
# GUI setup
# ---------------------------------------
root = tk.Tk()
root.title("📚 Student Record Management System")
root.geometry("600x500")
root.config(bg="#f7f7f7")

title_label = tk.Label(root, text="Student Record Management System", font=("Arial", 18, "bold"), bg="#f7f7f7")
title_label.pack(pady=10)

# Frame for buttons
button_frame = tk.Frame(root, bg="#f7f7f7")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Student", width=15, command=add_student).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Search Student", width=15, command=search_student).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Sort by Grade", width=15, command=sort_students).grid(row=0, column=2, padx=5, pady=5)
tk.Button(button_frame, text="Delete Student", width=15, command=delete_student).grid(row=0, column=3, padx=5, pady=5)
tk.Button(button_frame, text="Refresh Table", width=15, command=view_students).grid(row=0, column=4, padx=5, pady=5)

# Frame for table
table_frame = tk.Frame(root)
table_frame.pack(pady=10, fill="both", expand=True)

# Scrollbars
scroll_y = tk.Scrollbar(table_frame, orient="vertical")
scroll_y.pack(side="right", fill="y")

scroll_x = tk.Scrollbar(table_frame, orient="horizontal")
scroll_x.pack(side="bottom", fill="x")

# Treeview table
table = ttk.Treeview(table_frame, columns=("Name", "Reg No", "Grade"),
                     yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, show="headings")

table.heading("Name", text="Name")
table.heading("Reg No", text="Reg No")
table.heading("Grade", text="Grade")

table.column("Name", width=180)
table.column("Reg No", width=120)
table.column("Grade", width=80)

table.pack(fill="both", expand=True)

scroll_y.config(command=table.yview)
scroll_x.config(command=table.xview)

# Exit button
tk.Button(root, text="Exit", width=15, command=root.destroy, bg="#d9534f", fg="white").pack(pady=15)

root.mainloop()
