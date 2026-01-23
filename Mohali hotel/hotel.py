import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

DB_NAME = "mohali_hotel.db"

class MohaliHotelManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Mohali Hotel Management System")
        self.root.geometry("950x560")

        self.dark_mode = False

        # ===== DATABASE =====
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.create_table()

        # ===== STYLES =====
        self.light = {
            "bg": "#f3f4f6",
            "card": "white",
            "header": "#111827",
            "text": "#111827"
        }
        self.dark = {
            "bg": "#0f172a",
            "card": "#1e293b",
            "header": "#020617",
            "text": "white"
        }

        self.apply_theme()

        # ===== HEADER =====
        self.header = tk.Frame(root, bg=self.theme["header"], height=70)
        self.header.pack(fill="x")

        tk.Label(
            self.header, text="MOHALI HOTEL",
            font=("Segoe UI", 22, "bold"),
            bg=self.theme["header"], fg="white"
        ).pack(pady=(10, 0))

        tk.Label(
            self.header, text="Hotel Management System",
            font=("Segoe UI", 11),
            bg=self.theme["header"], fg="#9ca3af"
        ).pack()

        # ===== MAIN =====
        self.main = tk.Frame(root, bg=self.theme["bg"])
        self.main.pack(fill="both", expand=True, padx=20, pady=20)

        # ===== LEFT PANEL =====
        self.left = tk.Frame(self.main, bg=self.theme["card"], width=300)
        self.left.pack(side="left", fill="y", padx=(0, 15))
        self.left.pack_propagate(False)

        tk.Label(
            self.left, text="Guest Details",
            font=("Segoe UI", 14, "bold"),
            bg=self.theme["card"], fg=self.theme["text"]
        ).pack(anchor="w", padx=15, pady=15)

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.room_var = tk.StringVar(value="Single")
        self.bill_var = tk.StringVar()

        self.field("Guest Name", self.name_var)
        self.field("Phone Number", self.phone_var)
        self.field("Bill Amount (₹)", self.bill_var)

        tk.Label(self.left, text="Room Type", bg=self.theme["card"], fg=self.theme["text"]).pack(anchor="w", padx=15)
        ttk.Combobox(
            self.left,
            textvariable=self.room_var,
            values=["Single", "Double", "Deluxe", "Suite"],
            state="readonly"
        ).pack(fill="x", padx=15, pady=(0, 20))

        tk.Button(
            self.left, text="Check In",
            bg="#2563eb", fg="white",
            font=("Segoe UI", 10, "bold"),
            command=self.check_in
        ).pack(fill="x", padx=15, pady=5)

        tk.Button(
            self.left, text="Check Out",
            bg="#ef4444", fg="white",
            font=("Segoe UI", 10, "bold"),
            command=self.check_out
        ).pack(fill="x", padx=15, pady=5)

        tk.Button(
            self.left, text="Toggle Dark Mode",
            bg="#6b7280", fg="white",
            font=("Segoe UI", 10),
            command=self.toggle_theme
        ).pack(fill="x", padx=15, pady=(20, 10))

        # ===== RIGHT PANEL =====
        self.right = tk.Frame(self.main, bg=self.theme["card"])
        self.right.pack(side="right", fill="both", expand=True)

        tk.Label(
            self.right, text="Current Guests",
            font=("Segoe UI", 14, "bold"),
            bg=self.theme["card"], fg=self.theme["text"]
        ).pack(anchor="w", padx=15, pady=15)

        columns = ("id", "name", "phone", "room", "bill", "date")
        self.table = ttk.Treeview(self.right, columns=columns, show="headings")

        for col, title, w in [
            ("id", "ID", 40),
            ("name", "Name", 160),
            ("phone", "Phone", 120),
            ("room", "Room", 100),
            ("bill", "Bill (₹)", 100),
            ("date", "Check-In Date", 140)
        ]:
            self.table.heading(col, text=title)
            self.table.column(col, width=w)

        self.table.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.load_data()

    # ===== UI HELPERS =====
    def field(self, label, var):
        tk.Label(self.left, text=label, bg=self.theme["card"], fg=self.theme["text"]).pack(anchor="w", padx=15)
        tk.Entry(self.left, textvariable=var).pack(fill="x", padx=15, pady=(0, 10))

    def apply_theme(self):
        self.theme = self.dark if self.dark_mode else self.light
        self.root.configure(bg=self.theme["bg"])

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.root.destroy()
        root = tk.Tk()
        MohaliHotelManagement(root)
        root.mainloop()

    # ===== DATABASE =====
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS guests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                room TEXT,
                bill REAL,
                checkin_date TEXT
            )
        """)
        self.conn.commit()

    def load_data(self):
        for row in self.table.get_children():
            self.table.delete(row)

        self.cursor.execute("SELECT * FROM guests")
        for row in self.cursor.fetchall():
            self.table.insert("", "end", values=row)

    # ===== LOGIC =====
    def check_in(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        room = self.room_var.get()
        bill = self.bill_var.get().strip()

        if not name or not phone or not bill:
            messagebox.showwarning("Error", "All fields required.")
            return
        if not phone.isdigit() or not bill.isdigit():
            messagebox.showwarning("Error", "Phone & bill must be numeric.")
            return

        date = datetime.now().strftime("%d-%m-%Y %H:%M")

        self.cursor.execute(
            "INSERT INTO guests (name, phone, room, bill, checkin_date) VALUES (?, ?, ?, ?, ?)",
            (name, phone, room, bill, date)
        )
        self.conn.commit()
        self.load_data()

        self.name_var.set("")
        self.phone_var.set("")
        self.bill_var.set("")

    def check_out(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Error", "Select a guest to check out.")
            return

        guest_id = self.table.item(selected[0])["values"][0]
        self.cursor.execute("DELETE FROM guests WHERE id=?", (guest_id,))
        self.conn.commit()
        self.load_data()


# ===== RUN =====
root = tk.Tk()
MohaliHotelManagement(root)
root.mainloop()
