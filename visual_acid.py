import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
from datetime import datetime

DB_FILE = "visual_acid.db"

# ---------------------------------------
# Initialize database (fresh start)
# ---------------------------------------
def init_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("CREATE TABLE accounts (name TEXT PRIMARY KEY, balance INTEGER NOT NULL)")
    c.executemany("INSERT INTO accounts VALUES (?, ?)", [
        ('Alice', 1000),
        ('Bob', 1000)
    ])
    conn.commit()
    conn.close()

# ---------------------------------------
# Log helper
# ---------------------------------------
def log(message, color="black"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_box.insert(tk.END, f"[{timestamp}] {message}\n", color)
    log_box.see(tk.END)

# ---------------------------------------
# Database connection setup
# ---------------------------------------
def connect_db():
    global conn, cursor
    conn = sqlite3.connect(DB_FILE, isolation_level=None)
    cursor = conn.cursor()

def get_balances():
    cursor.execute("SELECT * FROM accounts")
    return cursor.fetchall()

def refresh_display():
    balances = get_balances()
    balance_display.delete(1.0, tk.END)
    for name, balance in balances:
        balance_display.insert(tk.END, f"{name}: {balance}\n")

# ---------------------------------------
# Transaction operations
# ---------------------------------------
def start_transaction():
    try:
        cursor.execute("BEGIN;")
        log("BEGIN TRANSACTION", "blue")
        messagebox.showinfo("Transaction", "Transaction started.")
        refresh_display()
    except Exception as e:
        log(f"Error starting transaction: {e}", "red")

def transfer():
    try:
        cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE name='Alice'")
        cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE name='Bob'")
        refresh_display()
        log("Executed transfer 100 from Alice → Bob (pending commit)", "orange")
    except Exception as e:
        log(f"Transfer error: {e}", "red")

def commit():
    try:
        cursor.execute("COMMIT;")
        log("COMMIT executed (changes saved permanently)", "green")
        messagebox.showinfo("Commit", "Transaction committed successfully!")
        refresh_display()
    except Exception as e:
        log(f"Commit error: {e}", "red")

def rollback():
    try:
        cursor.execute("ROLLBACK;")
        log("ROLLBACK executed (changes undone)", "red")
        messagebox.showinfo("Rollback", "Transaction rolled back successfully.")
        refresh_display()
    except Exception as e:
        log(f"Rollback error: {e}", "red")

def simulate_crash():
    try:
        conn.close()
        log("💥 Simulated crash! Connection closed unexpectedly.", "red")
        messagebox.showwarning("Crash", "System crash simulated! Database closed.")
    except Exception as e:
        log(f"Crash simulation error: {e}", "red")

def reconnect():
    try:
        connect_db()
        refresh_display()
        log("🔁 Database reconnected (checking durability)", "blue")
        messagebox.showinfo("Reconnect", "Reconnected to database successfully.")
    except Exception as e:
        log(f"Reconnect error: {e}", "red")

# ---------------------------------------
# GUI setup
# ---------------------------------------
root = tk.Tk()
root.title("💾 Visual ACID Transaction Demo")
root.geometry("750x600")
root.config(bg="#f7f7f7")

title = tk.Label(root, text="ACID Properties Demo", font=("Arial", 18, "bold"), bg="#f7f7f7")
title.pack(pady=10)

# Balances area
balance_frame = tk.LabelFrame(root, text="Account Balances", font=("Arial", 12, "bold"), bg="#f7f7f7")
balance_frame.pack(pady=10)

balance_display = tk.Text(balance_frame, height=5, width=30, font=("Consolas", 12))
balance_display.pack(padx=10, pady=10)

# Buttons
button_frame = tk.Frame(root, bg="#f7f7f7")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Start Transaction", width=18, command=start_transaction, bg="#0275d8", fg="white").grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Transfer 100 (Alice→Bob)", width=18, command=transfer, bg="#5cb85c", fg="white").grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Commit", width=18, command=commit, bg="#5bc0de", fg="white").grid(row=1, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Rollback", width=18, command=rollback, bg="#d9534f", fg="white").grid(row=1, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Simulate Crash", width=18, command=simulate_crash, bg="#f0ad4e", fg="white").grid(row=2, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Reconnect DB", width=18, command=reconnect, bg="#292b2c", fg="white").grid(row=2, column=1, padx=5, pady=5)

# Transaction log area
log_frame = tk.LabelFrame(root, text="Transaction Log", font=("Arial", 12, "bold"), bg="#f7f7f7")
log_frame.pack(pady=10, fill="both", expand=True)

log_box = tk.Text(log_frame, height=12, font=("Consolas", 11))
log_box.pack(padx=10, pady=10, fill="both", expand=True)

# Color tags for log
log_box.tag_config("blue", foreground="blue")
log_box.tag_config("orange", foreground="orange")
log_box.tag_config("green", foreground="green")
log_box.tag_config("red", foreground="red")
log_box.tag_config("black", foreground="black")

# Initialize DB and connect
init_db()
connect_db()
refresh_display()
log("Initialized new database with Alice=1000, Bob=1000", "black")

root.mainloop()
