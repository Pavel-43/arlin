import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog


# Функция подключения к базе данных
def connect_go_db(db_route='airline_sales.db'):
    conn = sqlite3.connect(db_route)
    cur = conn.cursor()
    return conn, cur


# Функция закрытия соединения с базой данных
def close_connection(conn):
    conn.close()


# Создание таблицы Destinations если она еще не существует
def create_destinations_table():
    conn, cur = connect_go_db()
    cur.execute('''CREATE TABLE IF NOT EXISTS destinations (
                    destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    airport_code TEXT NOT NULL,
                    city TEXT NOT NULL,
                    country TEXT NOT NULL,
                    timezone INTEGER NOT NULL
                )''')
    conn.commit()
    close_connection(conn)


# Вставка нового пункта назначения
def insert_destination(airport_code, city, country, timezone):
    conn, cur = connect_go_db()
    sql = '''INSERT INTO destinations (airport_code, city, country, timezone) 
            VALUES (?, ?, ?, ?)'''
    try:
        # Проверка входных данных
        if not airport_code or not city or not country or not str(timezone):
            raise ValueError("Пожалуйста, заполните все поля.")

        # Преобразование timezone в строку, если это целое число
        if isinstance(timezone, int):
            timezone = str(timezone)

        cur.execute(sql, (airport_code, city, country, timezone))
        conn.commit()

        # Проверка успешного добавления
        if cur.rowcount > 0:
            messagebox.showinfo("Всё выполнено верно",
                                f"Новый пункт назначения '{city}, {country}' добавлен в базу данных.")
        else:
            messagebox.showwarning("Внимание", "Пункт назначения не был добавлен в базу данных.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Ошибка", "Указанный код аэропорта уже существует в базе данных.")
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))
    except Exception as e:
        messagebox.showerror("Ошибка", f"Неизвестная ошибка при добавлении пункта назначения: {e}")
    finally:
        close_connection(conn)


# Извлечение всех пунктов назначения из таблицы
def withdraw_destinations():
    conn, cur = connect_go_db()
    cur.execute("SELECT * FROM destinations")
    rows = cur.fetchall()
    close_connection(conn)
    return rows


# Удаление пункта назначения по ID
def delete_destination(destination_id):
    conn, cur = connect_go_db()
    sql = '''DELETE FROM destinations WHERE destination_id = ?'''
    try:
        cur.execute(sql, (destination_id,))
        conn.commit()
        if cur.rowcount > 0:
            messagebox.showinfo("Всё выполнено верно", f"Пункт назначения с id {destination_id} удален.")
        else:
            messagebox.showwarning("Внимание", f"Пункт назначения с id {destination_id} не найден.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при удалении пункта назначения: {e}")
    close_connection(conn)


# Добавление нового пункта назначения
def add_destinations():
    dest = tk.Toplevel()
    dest.title("Добавить пункт назначения")
    dest.configure(bg="#f0f0f0")  # Светлый фон

    tk.Label(dest, text="Введите код аэропорта", bg="#f0f0f0", fg="#333", font=("Arial", 12)).pack(pady=5)
    airport_code_entry = tk.Entry(dest, font=("Arial", 12))
    airport_code_entry.pack(pady=5)

    tk.Label(dest, text="Введите город", bg="#f0f0f0", fg="#333", font=("Arial", 12)).pack(pady=5)
    city_entry = tk.Entry(dest, font=("Arial", 12))
    city_entry.pack(pady=5)

    tk.Label(dest, text="Введите страну", bg="#f0f0f0", fg="#333", font=("Arial", 12)).pack(pady=5)
    country_entry = tk.Entry(dest, font=("Arial", 12))
    country_entry.pack(pady=5)

    tk.Label(dest, text="Введите часовой пояс", bg="#f0f0f0", fg="#333", font=("Arial", 12)).pack(pady=5)
    timezone_entry = tk.Entry(dest, font=("Arial", 12))
    timezone_entry.pack(pady=5)

    def submit():
        try:
            if not airport_code_entry.get() or not city_entry.get() or not country_entry.get() or not timezone_entry.get():
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
                return

            insert_destination(airport_code_entry.get(), city_entry.get(), country_entry.get(),
                               int(timezone_entry.get()))
            dest.destroy()
            messagebox.showinfo("Успех", "Новый пункт назначения успешно добавлен в базу данных.")
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные данные для часового пояса.")

    tk.Button(dest, text="Добавить пункт назначения", command=submit, bg="#3498db", fg="white", font=("Arial", 12),
              relief="flat").pack(pady=10)


# Отображение всех пунктов назначения
def show_destinations():
    destinations = withdraw_destinations()
    if not destinations:
        messagebox.showinfo("Список пунктов назначений", "Список пунктов назначений пуст.")
    else:
        destinations_list = "\n".join(
            [f"ID: {row[0]}, Код аэропорта: {row[1]}, Город: {row[2]}, Страна: {row[3]}, Часовой пояс: {row[4]}" for row
             in destinations])
        messagebox.showinfo("Список пунктов назначений", destinations_list)


# Очистка списка пунктов назначений
def clear_destinations():
    destination_id = simpledialog.askinteger("Удалить пункт назначения", "Введите ID пункта назначения для удаления:")
    if destination_id is not None:
        delete_destination(destination_id)


# Основная функция
def main():
    create_destinations_table()

    # Запрашиваем логин
    login = simpledialog.askstring("Вход", "Введите ваш логин:")
    if login != "admin":
        messagebox.showinfo("Доступ", "У вас нет прав для добавления или удаления пунктов назначения.")

    root = tk.Tk()
    root.title("Управление пунктами назначений")
    root.geometry("500x300")
    root.configure(bg="#f0f0f0")  # Светлый фон
    root.minsize(400, 300)
    root.maxsize(1200, 900)

    # Заголовок
    tk.Label(root, text="Управление пунктами назначений", bg="#f0f0f0", fg="#333", font=("Arial", 16, "bold")).pack(
        pady=20)

    # Кнопки
    if login == "admin":
        add_button = tk.Button(root, text="Добавить пункт назначения", command=add_destinations, bg="#3498db",
                               fg="white", font=("Arial", 12), relief="flat")
        add_button.pack(pady=10)

        remove_button = tk.Button(root, text="Удалить пункт назначения", command=clear_destinations, bg="#e74c3c",
                                  fg="white", font=("Arial", 12), relief="flat")
        remove_button.pack(pady=10)

    show_button = tk.Button(root, text="Показать пункты назначений", command=show_destinations, bg="#2ecc71",
                            fg="white", font=("Arial", 12), relief="flat")
    show_button.pack(pady=10)

    exit_button = tk.Button(root, text="Выход", command=root.quit, bg="#95a5a6", fg="white", font=("Arial", 12),
                            relief="flat")
    exit_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()