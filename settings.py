import tkinter as tk
import json
import os
import sys


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = get_base_dir()
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")


def load():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return {"days": 30, "folder": "OldFiles"}


def save():
    data = {
        "days": int(days.get()),
        "folder": folder.get()
    }

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    status.config(text="Налаштування збережені")


config = load()

root = tk.Tk()
root.title("Налаштування очищення")
root.geometry("320x180")

tk.Label(root, text="Файли старші ніж (днів)").pack()

days = tk.Entry(root)
days.insert(0, config["days"])
days.pack()

tk.Label(root, text="Назва папки для архіву").pack()

folder = tk.Entry(root)
folder.insert(0, config["folder"])
folder.pack()

tk.Button(root, text="Зберегти", command=save).pack(pady=10)

status = tk.Label(root, text="")
status.pack()

root.mainloop()