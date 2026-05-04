import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "movies.json"

movies_list = []
tree = None
title_entry = None
genre_entry = None
year_entry = None
rating_entry = None
filter_genre_entry = None
filter_year_entry = None

def load_data():
    global movies_list
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                movies_list = json.load(f)
        except json.JSONDecodeError:
            movies_list = []
    else:
        movies_list = []

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(movies_list, f, ensure_ascii=False, indent=4)

def validate_input(title, genre, year_str, rating_str):
    if not title or not genre or not year_str or not rating_str:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return False

    try:
        year = int(year_str)
        if year < 1888 or year > 2026:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Год должен быть корректным числом (1888-2026).")
        return False

    try:
        rating = float(rating_str)
        if rating < 0 or rating > 10:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10.")
        return False

    return True

def add_movie():
    global movies_list
    
    title = title_entry.get().strip()
    genre = genre_entry.get().strip()
    year_str = year_entry.get().strip()
    rating_str = rating_entry.get().strip()

    if not validate_input(title, genre, year_str, rating_str):
        return

    new_movie = {
        "id": len(movies_list) + 1,
        "title": title,
        "genre": genre,
        "year": int(year_str),
        "rating": float(rating_str)
    }

    movies_list.append(new_movie)
    save_data()
    refresh_table()

    title_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)
    
    messagebox.showinfo("Успех", "Фильм добавлен в библиотеку!")

def refresh_table(data=None):
    global tree
    
    for item in tree.get_children():
        tree.delete(item)
    
    display_data = data if data is not None else movies_list
    
    for m in display_
        tree.insert("", tk.END, values=(
            m["id"],
            m["title"],
            m["genre"],
            m["year"],
            m["rating"]
        ))

def apply_filter():
    genre_filter = filter_genre_entry.get().strip().lower()
    year_filter = filter_year_entry.get().strip()

    filtered_data = movies_list

    if genre_filter:
        filtered_data = [m for m in filtered_data if genre_filter in m["genre"].lower()]
    
    if year_filter:
        try:
            year_val = int(year_filter)
            filtered_data = [m for m in filtered_data if m["year"] == year_val]
        except ValueError:
            messagebox.showwarning("Внимание", "Год в фильтре должен быть числом")
            return

    refresh_table(filtered_data)

def reset_filter():
    filter_genre_entry.delete(0, tk.END)
    filter_year_entry.delete(0, tk.END)
    refresh_table()

def delete_movie():
    global movies_list
    
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Внимание", "Выберите фильм для удаления!")
        return
    
    item_values = tree.item(selected_item[0])["values"]
    movie_id = item_values[0]
    
    if messagebox.askyesno("Подтверждение", f"Удалить фильм ID {movie_id}?"):
        movies_list = [m for m in movies_list if m["id"] != movie_id]
        save_data()
        refresh_table()

def create_interface(root):
    global tree, title_entry, genre_entry, year_entry, rating_entry, filter_genre_entry, filter_year_entry

    root.title("Movie Library - Личная кинотека")
    root.geometry("900x600")

    input_frame = ttk.LabelFrame(root, text="Добавить фильм", padding=10)
    input_frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
    title_entry = ttk.Entry(input_frame, width=30)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Жанр:").grid(row=0, column=2, sticky="w")
    genre_entry = ttk.Entry(input_frame)
    genre_entry.grid(row=0, column=3, padx=5, pady=5)

    ttk.Label(input_frame, text="Год:").grid(row=0, column=4, sticky="w")
    year_entry = ttk.Entry(input_frame, width=10)
    year_entry.grid(row=0, column=5, padx=5, pady=5)

    ttk.Label(input_frame, text="Рейтинг (0-10):").grid(row=0, column=6, sticky="w")
    rating_entry = ttk.Entry(input_frame, width=10)
    rating_entry.grid(row=0, column=7, padx=5, pady=5)

    add_btn = ttk.Button(input_frame, text="Добавить", command=add_movie)
    add_btn.grid(row=0, column=8, padx=10)

    filter_frame = ttk.LabelFrame(root, text="Фильтр", padding=10)
    filter_frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(filter_frame, text="По жанру:").grid(row=0, column=0, sticky="w")
    filter_genre_entry = ttk.Entry(filter_frame)
    filter_genre_entry.grid(row=0, column=1, padx=5)

    ttk.Label(filter_frame, text="По году:").grid(row=0, column=2, sticky="w")
    filter_year_entry = ttk.Entry(filter_frame)
    filter_year_entry.grid(row=0, column=3, padx=5)

    filter_btn = ttk.Button(filter_frame, text="Применить", command=apply_filter)
    filter_btn.grid(row=0, column=4, padx=5)

    reset_btn = ttk.Button(filter_frame, text="Сброс", command=reset_filter)
    reset_btn.grid(row=0, column=5, padx=5)

    tree_frame = ttk.Frame(root)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

    columns = ("ID", "Название", "Жанр", "Год", "Рейтинг")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        if col == "Название":
            tree.column(col, width=300)
        else:
            tree.column(col, width=100)

    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    del_btn = ttk.Button(root, text="Удалить выбранный фильм", command=delete_movie)
    del_btn.pack(pady=5)

if __name__ == "__main__":
    load_data()
    root = tk.Tk()
    create_interface(root)
    refresh_table()
    root.mainloop()  