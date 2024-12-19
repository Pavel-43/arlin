import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import subprocess

# Пароль администратора
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"


def add_employee(username, password):
    conn = sqlite3.connect('users')
    conn.execute('''CREATE TABLE IF NOT EXISTS users
        (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    c = conn.cursor()

    # Проверяем, существует ли уже пользователь с таким именем
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует.")
        conn.close()
        return False

    # Шифруем пароль перед сохранением в базу данных
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Если пользователя нет, добавляем нового
    c.execute("INSERT INTO users (username, password) VALUES (?,?)",
              (username, hashed_password))
    conn.commit()
    conn.close()
    messagebox.showinfo("Успех", "Пользователь успешно зарегистрирован.")
    return True


def on_register(entry_username, entry_password, root):
    username = entry_username.get()
    password = entry_password.get()
    if add_employee(username, password):
        root.destroy()  # Закрываем окно после успешной регистрации


def on_login(entry_username, entry_password, root):
    username = entry_username.get()
    password = entry_password.get()

    conn = sqlite3.connect('users')
    c = conn.cursor()

    # Проверяем, существует ли пользователь с таким именем
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()

    if user:
        # Проверяем пароль
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if user[1] == hashed_password:
            messagebox.showinfo("Успех", "Вход выполнен успешно.")
            root.destroy()  # Закрываем текущее окно
            launch_gui()  # Запускаем gui.py
        else:
            messagebox.showerror("Ошибка", "Неверный пароль.")
    else:
        messagebox.showerror("Ошибка", "Пользователь не найден.")

    conn.close()


def show_login_window():
    root = tk.Tk()
    root.title("Авторизация")
    root.geometry("400x400")

    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10)

    label_username = tk.Label(main_frame, text="Имя пользователя:")
    label_username.grid(row=0, column=0, padx=5, pady=5)
    entry_username = tk.Entry(main_frame)
    entry_username.grid(row=0, column=1, padx=5, pady=5)

    label_password = tk.Label(main_frame, text="Пароль:")
    label_password.grid(row=1, column=0, padx=5, pady=5)
    entry_password = tk.Entry(main_frame, show="*")
    entry_password.grid(row=1, column=1, padx=5, pady=5)

    button_login = tk.Button(main_frame, text="Войти", command=lambda: on_login(
        entry_username,
        entry_password,
        root
    ))
    button_login.grid(row=2, column=0, columnspan=2, padx=5, pady=20)

    button_register = tk.Button(main_frame, text="Регистрация", command=lambda: [root.destroy(), show_register_window()])
    button_register.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()


def show_register_window():
    root = tk.Tk()
    root.title("Регистрация пользователя")
    root.geometry("350x200")

    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10)

    label_username = tk.Label(main_frame, text="Имя пользователя:")
    label_username.grid(row=0, column=0, padx=5, pady=5)
    entry_username = tk.Entry(main_frame)
    entry_username.grid(row=0, column=1, padx=5, pady=5)

    label_password = tk.Label(main_frame, text="Пароль:")
    label_password.grid(row=1, column=0, padx=5, pady=5)
    entry_password = tk.Entry(main_frame, show="*")
    entry_password.grid(row=1, column=1, padx=5, pady=5)

    button_register = tk.Button(main_frame, text="Зарегистрировать", command=lambda: on_register(
        entry_username,
        entry_password,
        root
    ))
    button_register.grid(row=2, column=0, columnspan=2, padx=5, pady=20)

    button_back = tk.Button(main_frame, text="Назад", command=lambda: [root.destroy(), show_login_window()])
    button_back.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()


def launch_gui():
    """Запускает файл gui.py в новом процессе."""
    try:
        subprocess.run(["python", "gui.py"])
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл gui.py не найден.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить gui.py: {str(e)}")


def initialize_admin():
    conn = sqlite3.connect('users')
    c = conn.cursor()

    # Проверяем, существует ли пользователь admin
    c.execute("SELECT * FROM users WHERE username=?", (ADMIN_USERNAME,))
    if not c.fetchone():
        # Если admin не существует, добавляем его
        hashed_password = hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest()
        c.execute("INSERT INTO users (username, password) VALUES (?,?)",
                  (ADMIN_USERNAME, hashed_password))
        conn.commit()
        print("Пользователь admin добавлен в базу данных.")
    conn.close()


def main():
    initialize_admin()  # Инициализируем пользователя admin
    show_login_window()


if __name__ == "__main__":
    main()
