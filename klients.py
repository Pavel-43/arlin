import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog

def create_passenger_table():
    conn, cur = connect_to_db()
    cur.execute('''CREATE TABLE IF NOT EXISTS Passengers (
                    PassengerID INTEGER PRIMARY KEY AUTOINCREMENT,
                    FirstName TEXT NOT NULL,
                    LastName TEXT NOT NULL,
                    Email TEXT UNIQUE NOT NULL)''')
    conn.commit()
    close_connection(conn)

def connect_to_db(db_route='airline_sales.db'):
    conn = sqlite3.connect(db_route)
    cur = conn.cursor()
    return conn, cur

def close_connection(conn):
    conn.close()

def insert_passenger(first_name, last_name, email):
    conn, cur = connect_to_db()
    sql = '''INSERT INTO Passengers (FirstName, LastName, Email) VALUES (?, ?, ?)'''
    try:
        cur.execute(sql, (first_name, last_name, email))
        conn.commit()
        messagebox.showinfo("Всё выполнено верно", f"Пассажир '{last_name}, {first_name}' добавлен в базу данных.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при добавлении пассажира: {e}")
    close_connection(conn)

def withdraw_passengers():
    conn, cur = connect_to_db()
    cur.execute("SELECT * FROM Passengers")
    rows = cur.fetchall()
    close_connection(conn)
    return rows

def delete_passenger(passenger_id):
    conn, cur = connect_to_db()
    sql = '''DELETE FROM Passengers WHERE PassengerID = ?'''
    try:
        cur.execute(sql, (passenger_id,))
        conn.commit()
        if cur.rowcount > 0:
            messagebox.showinfo("Всё выполнено верно", f"Пассажир с id {passenger_id} удален.")
        else:
            messagebox.showwarning("Внимание", f"Пассажир с id {passenger_id} не найден.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при удалении пассажира: {e}")
    close_connection(conn)

def add_passengers():
    passenger = tk.Toplevel()
    passenger.title("Добавить пассажира")

    tk.Label(passenger, text="Введите имя:").pack()
    first_name_entry = tk.Entry(passenger)
    first_name_entry.pack()

    tk.Label(passenger, text="Введите фамилию:").pack()
    last_name_entry = tk.Entry(passenger)
    last_name_entry.pack()

    tk.Label(passenger, text="Введите email:").pack()
    email_entry = tk.Entry(passenger)
    email_entry.pack()

    def submit():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        try:
            email = email_entry.get()
            if not first_name or not last_name or not email:
                messagebox.showerror("Ошибка", "Пожалуйста, введите все поля.")
                return

            insert_passenger(first_name, last_name, email)
            passenger.destroy()
            messagebox.showinfo("Успех", "Пассажир успешно добавлен в базу данных.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Пожалуйста, введите корректные данные: {e}")
    tk.Button(passenger, text="Добавить пассажира", command=submit).pack()

def show_passengers():
    passengers = withdraw_passengers()
    if not passengers:
        messagebox.showinfo("Список пассажиров", "Список пассажиров пуст.")
    else:
        passengers_list = "\n".join(
            [f"ID: {row[0]}, Имя: {row[1]}, Фамилия: {row[2]}, Email: {row[3]}" for row in passengers])
        messagebox.showinfo("Список пассажиров", passengers_list)

def clear_passenger():
    passenger_id = simpledialog.askinteger("Удалить пассажира", "Введите id пассажира для удаления:")
    if passenger_id is not None:
        delete_passenger(passenger_id)

def main():
    create_passenger_table()

    # Запрашиваем логин
    login = simpledialog.askstring("Вход", "Введите ваш логин:")
    if login != "admin":
        messagebox.showinfo("Доступ", "У вас нет прав для удаления пассажиров.")

    root = tk.Tk()
    root.title("Управление пассажирами")
    root.geometry("350x250")  # Устанавливаем начальный размер 800x600 пикселей
    root.minsize(100, 100)  # Устанавливаем минимальный размер
    root.maxsize(1200, 900)
    style = ttk.Style()
    style.theme_use("clam")  # Используем тему clam для более современного вида

    # Настройка стиля кнопок
    style.configure("TButton",
                    font=('Helvetica', 12, 'bold'),
                    foreground='white',
                    background='#3498db',
                    borderwidth=0,
                    relief='flat',
                    padding=10)

    style.map("TButton",
              foreground=[('!active', '#ecf0f1')],
              background=[('!active', '#2980b9')])

    add_button = tk.Button(root, text="Добавить пассажира", command=add_passengers, bg="#3498db",
                               fg="white", font=("Arial", 12), relief="flat")
    add_button.pack(pady=10)

    show_button = tk.Button(root, text="Показать пассажиров", command=show_passengers, bg="#27ae60",
                            fg="white", font=("Arial", 12), relief="flat")
    show_button.pack(pady=10)

    # Отображаем кнопку удаления только для администратора
    if login == "admin":
        remove_button = tk.Button(root, text="Удалить пассажира", command=clear_passenger, bg="#e74c3c",
                            fg="white", font=("Arial", 12), relief="flat")
        remove_button.pack(pady=10)

    exit_button = tk.Button(root, text="Выход", command=root.quit, bg="#95a5a6", fg="white", font=("Arial", 12),
                            relief="flat")
    exit_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()