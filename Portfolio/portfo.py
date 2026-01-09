import tkinter as tk
from tkinter import messagebox, filedialog

# ================= FUNCTIONS =================
def generate_portfolio():
    name = name_entry.get().strip()
    bio = bio_entry.get("1.0", tk.END).strip()
    skills = skills_entry.get("1.0", tk.END).strip().split('\n')
    projects = projects_entry.get("1.0", tk.END).strip().split('\n')
    template = template_var.get()

    if not name or not bio:
        messagebox.showerror("Error", "Name and Bio are required.")
        return

    if template == "Simple":
        output = f"""PORTFOLIO

Name: {name}

Bio:
{bio}

Skills:
""" + '\n'.join([f"- {s}" for s in skills if s]) + "\n\nProjects:\n" + \
                 '\n'.join([f"- {p}" for p in projects if p])

    else:  # Detailed
        output = f"""==============================
PORTFOLIO PROFILE
==============================

Name:
{name}

Professional Summary:
{bio}

Technical Skills:
""" + '\n'.join([f"• {s}" for s in skills if s]) + """

Projects:
""" + '\n'.join([f"• {p}" for p in projects if p]) + """

Generated using Portfolio Generator Tool
"""

    output_box.config(state='normal')
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, output)
    output_box.config(state='disabled')


def export_to_file():
    content = output_box.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Warning", "Generate portfolio first.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )

    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        messagebox.showinfo("Success", "Portfolio exported successfully.")


def clear_all():
    name_entry.delete(0, tk.END)
    bio_entry.delete("1.0", tk.END)
    skills_entry.delete("1.0", tk.END)
    projects_entry.delete("1.0", tk.END)
    output_box.config(state='normal')
    output_box.delete("1.0", tk.END)
    output_box.config(state='disabled')


# ================= GUI =================
root = tk.Tk()
root.title("Portfolio Generator")
root.geometry("780x650")
root.configure(bg="#f4f6f8")

# ================= HEADER =================
tk.Label(
    root,
    text="Portfolio Generator Tool",
    font=("Segoe UI", 18, "bold"),
    bg="#f4f6f8",
    fg="#2c3e50"
).pack(pady=10)

# ================= INPUT CARD =================
card = tk.Frame(root, bg="white", padx=20, pady=20, relief="groove", bd=1)
card.pack(padx=20, pady=10, fill="x")

tk.Label(card, text="Name", bg="white").grid(row=0, column=0, sticky="w")
name_entry = tk.Entry(card, width=40)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(card, text="Bio", bg="white").grid(row=1, column=0, sticky="nw")
bio_entry = tk.Text(card, width=40, height=4)
bio_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(card, text="Skills (one per line)", bg="white").grid(row=2, column=0, sticky="nw")
skills_entry = tk.Text(card, width=40, height=4)
skills_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(card, text="Projects (one per line)", bg="white").grid(row=3, column=0, sticky="nw")
projects_entry = tk.Text(card, width=40, height=4)
projects_entry.grid(row=3, column=1, padx=10, pady=5)

# ================= OPTIONS =================
options_frame = tk.Frame(root, bg="#f4f6f8")
options_frame.pack(pady=5)

tk.Label(options_frame, text="Template:", bg="#f4f6f8").pack(side="left", padx=5)
template_var = tk.StringVar(value="Simple")
tk.OptionMenu(options_frame, template_var, "Simple", "Detailed").pack(side="left")

# ================= BUTTONS =================
btn_frame = tk.Frame(root, bg="#f4f6f8")
btn_frame.pack(pady=10)

tk.Button(
    btn_frame, text="Generate",
    command=generate_portfolio,
    bg="#1976d2", fg="white", width=15
).pack(side="left", padx=5)

tk.Button(
    btn_frame, text="Export to File",
    command=export_to_file,
    bg="#2e7d32", fg="white", width=15
).pack(side="left", padx=5)

tk.Button(
    btn_frame, text="Clear",
    command=clear_all,
    bg="#d32f2f", fg="white", width=15
).pack(side="left", padx=5)

# ================= OUTPUT =================
output_box = tk.Text(
    root, height=15, width=90,
    font=("Consolas", 10),
    bg="white", relief="groove", bd=2
)
output_box.pack(padx=20, pady=10)
output_box.config(state='disabled')

root.mainloop()
