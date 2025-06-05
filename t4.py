import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import uuid
from datetime import datetime

class TaskForm:
    def __init__(self, master, callback, task=None):
        self.callback = callback
        self.task = task

        self.top = tk.Toplevel(master)
        self.top.title("Formular Sarcină")
        self.top.geometry("400x350")
        self.top.resizable(False, False)

        tk.Label(self.top, text="Titlu:").pack(pady=5)
        self.title_var = tk.StringVar(value=task['title'] if task else '')
        tk.Entry(self.top, textvariable=self.title_var).pack(fill=tk.X, padx=20)

        tk.Label(self.top, text="Descriere:").pack(pady=5)
        self.desc_text = tk.Text(self.top, height=4)
        self.desc_text.pack(fill=tk.X, padx=20)
        if task:
            self.desc_text.insert(tk.END, task['description'])

        tk.Label(self.top, text="Termen (YYYY-MM-DD):").pack(pady=5)
        self.deadline_var = tk.StringVar(value=task['deadline'] if task else '')
        tk.Entry(self.top, textvariable=self.deadline_var).pack(fill=tk.X, padx=20)

        tk.Label(self.top, text="Stare:").pack(pady=5)
        self.status_var = tk.StringVar(value=task['status'] if task else 'În curs')
        ttk.Combobox(self.top, textvariable=self.status_var, values=["În curs", "Finalizat"]).pack(fill=tk.X, padx=20)

        tk.Button(self.top, text="Salvează", command=self.save).pack(pady=20)

    def save(self):
        title = self.title_var.get().strip()
        desc = self.desc_text.get("1.0", tk.END).strip()
        deadline = self.deadline_var.get().strip()
        status = self.status_var.get().strip()

        if not title or not deadline:
            messagebox.showerror("Eroare", "Titlul și termenul sunt obligatorii!")
            return

        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Eroare", "Formatul datei nu este valid (YYYY-MM-DD)!")
            return

        task_data = {
            "id": self.task['id'] if self.task else str(uuid.uuid4()),
            "title": title,
            "description": desc,
            "deadline": deadline,
            "status": status
        }

        self.callback(task_data)
        self.top.destroy()

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("800x550")
        self.root.resizable(False, False)

        self.tasks = self.load_tasks()

        self.setup_ui()
        self.refresh_task_list()

    def setup_ui(self):
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)

        tk.Button(frame_top, text="Adaugă sarcină", command=self.add_task).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Editează", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Șterge", command=self.delete_task).pack(side=tk.LEFT, padx=5)

        self.search_var = tk.StringVar()
        tk.Entry(frame_top, textvariable=self.search_var, width=40).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_top, text="Caută", command=self.search_tasks).pack(side=tk.LEFT)

        columns = ("ID", "Titlu", "Termen", "Stare")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150 if col != "Titlu" else 250)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(pady=5)

        self.stats_label = tk.Label(frame_bottom, text="")
        self.stats_label.pack(side=tk.LEFT, padx=10)

        tk.Button(frame_bottom, text="Exportă CSV", command=self.export_csv).pack(side=tk.RIGHT, padx=10)

    def refresh_task_list(self, tasks=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for task in tasks or self.tasks:
            self.tree.insert("", "end", values=(task["id"], task["title"], task["deadline"], task["status"]))
        self.update_stats()

    def add_task(self):
        TaskForm(self.root, self.save_new_task)

    def save_new_task(self, task):
        self.tasks.append(task)
        self.save_tasks(self.tasks)
        self.refresh_task_list()

    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenție", "Selectează o sarcină!")
            return
        item = self.tree.item(selected[0])
        task_id = item['values'][0]
        task = next((t for t in self.tasks if t['id'] == task_id), None)
        TaskForm(self.root, self.update_task, task)

    def update_task(self, updated_task):
        for idx, t in enumerate(self.tasks):
            if t['id'] == updated_task['id']:
                self.tasks[idx] = updated_task
                break
        self.save_tasks(self.tasks)
        self.refresh_task_list()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenție", "Selectează o sarcină!")
            return
        item = self.tree.item(selected[0])
        task_id = item['values'][0]
        self.tasks = [t for t in self.tasks if t['id'] != task_id]
        self.save_tasks(self.tasks)
        self.refresh_task_list()

    def search_tasks(self):
        term = self.search_var.get().lower()
        filtered = [t for t in self.tasks if term in t['title'].lower() or term in t['description'].lower()]
        self.refresh_task_list(filtered)

    def update_stats(self):
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t['status'] == 'Finalizat')
        pending = total - done
        self.stats_label.config(text=f"Total: {total} | Finalizate: {done} | În curs: {pending}")

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            import csv
            with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Titlu", "Descriere", "Termen", "Stare"])
                for task in self.tasks:
                    writer.writerow([task['id'], task['title'], task['description'], task['deadline'], task['status']])
            messagebox.showinfo("Export reușit", f"Fișierul a fost salvat la:\n{file_path}")

    def load_tasks(self):
        if not os.path.exists('tasks.json'):
            return []
        with open('tasks.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_tasks(self, tasks):
        with open('tasks.json', 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
