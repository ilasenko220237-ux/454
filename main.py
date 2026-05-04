import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("850x650")
        self.data_file = "expenses.json"
        self.expenses = []
        self.load_data()

        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        # --- Панель ввода ---
        input_frame = ttk.LabelFrame(self.root, text="➕ Добавить расход")
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Сумма (₽):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = ttk.Entry(input_frame, width=10)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Категория:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.category_combo = ttk.Combobox(input_frame, values=["Еда", "Транспорт", "Развлечения", "Жильё", "Здоровье", "Другое"], state="readonly")
        self.category_combo.grid(row=0, column=3, padx=5, pady=5)
        self.category_combo.current(0)

        ttk.Label(input_frame, text="Дата (YYYY-MM-DD):").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.date_entry = ttk.Entry(input_frame, width=12)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(input_frame, text="Добавить расход", command=self.add_expense).grid(row=0, column=6, padx=10, pady=5)

        # --- Панель фильтрации ---
        filter_frame = ttk.LabelFrame(self.root, text="🔍 Фильтрация и подсчёт")
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Категория:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.filter_category = ttk.Combobox(filter_frame, values=["Все", "Еда", "Транспорт", "Развлечения", "Жильё", "Здоровье", "Другое"], state="readonly", width=12)
        self.filter_category.grid(row=0, column=1, padx=5, pady=5)
        self.filter_category.current(0)

        ttk.Label(filter_frame, text="С (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.filter_date_start = ttk.Entry(filter_frame, width=12)
        self.filter_date_start.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(filter_frame, text="По (YYYY-MM-DD):").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.filter_date_end = ttk.Entry(filter_frame, width=12)
        self.filter_date_end.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(filter_frame, text="Применить", command=self.apply_filter).grid(row=0, column=6, padx=5, pady=5)
        ttk.Button(filter_frame, text="Сбросить", command=self.reset_filter).grid(row=0, column=7, padx=5, pady=5)

        self.total_label = ttk.Label(filter_frame, text="💰 Итого: 0.00 ₽", font=("Segoe UI", 11, "bold"))
        self.total_label.grid(row=1, column=0, columnspan=8, pady=10, padx=10, sticky="w")

        # --- Таблица ---
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("id", "date", "category", "amount")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("id", text="№")
        self.tree.heading("date", text="Дата")
        self.tree.heading("category", text="Категория")
        self.tree.heading("amount", text="Сумма (₽)")
        
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("date", width=110, anchor="center")
        self.tree.column("category", width=160, anchor="center")
        self.tree.column("amount", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def add_expense(self):
        amount_str = self.amount_entry.get().strip().replace(",", ".")
        category = self.category_combo.get()
        date_str = self.date_entry.get().strip()

        # Валидация суммы
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Ошибка ввода", "Сумма должна быть положительным числом.")
                return
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Некорректный формат суммы.")
            return

        # Валидация даты
        if not self.validate_date(date_str):
            messagebox.showerror("Ошибка ввода", "Дата должна быть в формате YYYY-MM-DD.")
            return

        expense = {
            "amount": round(amount, 2),
            "category": category,
            "date": date_str
        }
        self.expenses.append(expense)
        self.save_data()
        self.refresh_table()
        
        # Очистка полей
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        messagebox.showinfo("Успех", "Расход успешно добавлен!")

    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=2)

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.expenses = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.expenses = []

    def refresh_table(self, filtered_data=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        data = filtered_data if filtered_data is not None else self.expenses
        for idx, exp in enumerate(data, 1):
            self.tree.insert("", "end", values=(
                idx, 
                exp["date"], 
                exp["category"], 
                f"{exp['amount']:.2f}"
            ))
        self.update_total(data)

    def apply_filter(self):
        category = self.filter_category.get()
        start_str = self.filter_date_start.get().strip()
        end_str = self.filter_date_end.get().strip()

        if start_str and not self.validate_date(start_str):
            messagebox.showerror("Ошибка", "Неверный формат даты начала (YYYY-MM-DD).")
            return
        if end_str and not self.validate_date(end_str):
            messagebox.showerror("Ошибка", "Неверный формат даты конца (YYYY-MM-DD).")
            return

        start_date = datetime.strptime(start_str, "%Y-%m-%d") if start_str else datetime.min
        end_date = datetime.strptime(end_str, "%Y-%m-%d") if end_str else datetime.max

        filtered = []
        for exp in self.expenses:
            exp_date = datetime.strptime(exp["date"], "%Y-%m-%d")
            cat_match = (category == "Все") or (exp["category"] == category)
            date_match = start_date <= exp_date <= end_date
            if cat_match and date_match:
                filtered.append(exp)

        self.refresh_table(filtered)

    def reset_filter(self):
        self.filter_category.current(0)
        self.filter_date_start.delete(0, tk.END)
        self.filter_date_end.delete(0, tk.END)
        self.refresh_table()

    def update_total(self, data):
        total = sum(exp["amount"] for exp in data)
        self.total_label.config(text=f"💰 Итого: {total:.2f} ₽")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
