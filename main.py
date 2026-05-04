import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "books.json"
books_list = []
tree = None
title_entry = None
author_entry = None
genre_entry = None
pages_entry = None
filter_genre_entry = None
filter_pages_entry = None

def load_data():
    global books_list
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                books_list = json.load(f)
        except json.JSONDecodeError:
            books_list = []
    else:
        books_list = []

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books_list, f, ensure_ascii=False, indent=4)

def validate_input(title, author, genre, pages_str):
    if not title or not author or not genre or not pages_str:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return False
    try:
        pages = int(pages_str)
        if pages <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Количество страниц должно быть положительным целым числом!")
        return False
    return True

def add_book():
    global books_list
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    genre = genre_entry.get().strip()
    pages_str = pages_entry.get().strip()

    if not validate_input(title, author, genre, pages_str):
        return

    new_book = {
        "id": len(books_list) + 1,
        "title": title,
        "author": author,
        "genre": genre,
        "pages": int(pages_str)
    }
    books_list.append(new_book)
    save_data()
    refresh_table()

    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    pages_entry.delete(0, tk.END)
    messagebox.showinfo("Успех", "Книга добавлена!")

def refresh_table(data=None):
    global tree
    for item in tree.get_children():
        tree.delete(item)
    display_data = data if data is not None else books_list
    for book in display
