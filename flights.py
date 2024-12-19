import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog


def create():
    conn, cur = connect_db()
    cur.execute('''CREATE TABLE IF NOT EXISTS fligh
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Route TEXT NOT NULL,
                    departure_airport TEXT NOT NULL,
                    arrival_airport TEXT NOT NULL,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL,
                    departure_date DATE NOT NULL,
                    FOREIGN KEY (departure_airport) REFERENCES destinations(airport_code),
                    FOREIGN KEY (arrival_airport) REFERENCES destinations(airport_code))''')
    conn.commit()
    close_connection(conn)


def connect_db(db_route='airline_sales.db'):
    conn = sqlite3.connect(db_route)
    cur = conn.cursor()
    return conn, cur


def close_connection(conn):
    conn.close()


def insert_flight(route, price, quantity, departure_airport, arrival_airport, departure_date):
    conn, cur = connect_db()
    sql = '''INSERT INTO fligh (route, price, quantity, departure_airport, arrival_airport, departure_date) VALUES (?, ?, ?, ?, ?, ?)'''
    try:
        cur.execute(sql, (route, price, quantity, departure_airport, arrival_airport, departure_date))
        conn.commit()
        messagebox.showinfo("Успешно", f"Рейс '{route}' добавлен в базу данных.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при добавлении рейса: {e}")
    close_connection(conn)


def withdraw_flight():
    conn, cur = connect_db()
    cur.execute("SELECT * FROM fligh")
    rows = cur.fetchall()
    close_connection(conn)
    return rows


def delete_flight(flight_id):
    conn, cur = connect_db()
    sql = '''DELETE FROM fligh WHERE id = ?'''
    try:
        cur.execute(sql, (flight_id,))
        conn.commit()
        if cur.rowcount > 0:
            messagebox.showinfo("Успешно", f"Рейс с id {flight_id} удален.")
        else:
            messagebox.showwarning("Внимание", f"Рейс с id {flight_id} не найден.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при удалении рейса: {e}")
    close_connection(conn)


def add_flights():
    fly = tk.Toplevel()
    fly.title("Добавить рейс")
    fly.geometry("400x450")
    fly.configure(bg="#f0f0f0")

    tk.Label(fly, text="Введите маршрут рейса:", bg="#f0f0f0", fg="#333", font=("Helvetica", 12)).pack(pady=5)
    route_entry = tk.Entry(fly, font=("Helvetica", 12))
    route_entry.pack(pady=5, padx=20, fill=tk.X)

    tk.Label(fly, text="Введите аэропорт отправления:", bg="#f0f0f0", fg="#333", font=("Helvetica", 12)).pack(pady=5)
    departure_airport_entry = tk.Entry(fly, font=("Helvetica", 12))
    departure_airport_entry.pack(pady=5, padx=20, fill=tk.X)

    tk.Label(fly, text="Введите аэропорт прибытия:", bg="#f0f0f0", fg="#333", font=("Helvetica", 12)).pack(pady=5)
    arrival_airport_entry = tk.Entry(fly, font=("Helvetica", 12))
    arrival_airport_entry.pack(pady=5, padx=20, fill=tk.X)

    tk.Label(fly, text="Введите цену:", bg="#f0f0f0", fg="#333", font=("Helvetica", 12)).pack(pady=5)
    price_entry = tk.Entry(fly, font=("Helvetica", 12))
    price_entry.pack(pady=5, padx=20, fill=tk.X)

    tk.Label(fly, text="Введите количество билетов:", bg="#f0f0f0", fg="#333", font=("Helvetica", 12)).pack(pady=5)
    quantity_entry = tk.Entry(fly, font=("Helvetica", 12))
    quantity_entry.pack(pady=5, padx=20, fill=tk.X)

    tk.Label(fly, text="Введите дату вылета (YYYY-MM-DD):", bg="#f0f0f0", fg="#333", font=("Helvetica", 12)).pack(pady=5)
    departure_date_entry = tk.Entry(fly, font=("Helvetica", 12))
    departure_date_entry.pack(pady=5, padx=20, fill=tk.X)

    def submit():
        route = route_entry.get()
        departure_airport = departure_airport_entry.get()
        arrival_airport = arrival_airport_entry.get()
        try:
            price = float(price_entry.get())
            quantity = int(quantity_entry.get())
            departure_date = departure_date_entry.get()

            if not route or price <= 0 or quantity <= 0 or not departure_date:
                messagebox.showerror("Ошибка", "Пожалуйста, введите корректные данные.")
                return

            insert_flight(route, price, quantity, departure_airport, arrival_airport, departure_date)
            fly.destroy()
            messagebox.showinfo("Успех", "Рейс успешно добавлен в базу данных.")
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные данные.")

    tk.Button(fly, text="Добавить рейс", command=submit, bg="#2980b9", fg="white", font=("Helvetica", 12), relief=tk.FLAT).pack(pady=20)


def show_flight():
    flights = withdraw_flight()
    if not flights:
        messagebox.showinfo("Список рейсов", "Список рейсов пуст.")
    else:
        flights_list = "\n".join(
            [f"ID: {row[0]}, Маршрут: {row[1]}, Аэропорт отправления: {row[2]}, "
             f"Аэропорт прибытия: {row[3]}, Цена: {row[4]}₽, Количество билетов: {row[5]}, "
             f"Дата вылета: {row[6]}" for row in flights])
        messagebox.showinfo("Список рейсов", flights_list)


def clear_flight():
    flight_id = simpledialog.askinteger("Удалить рейс", "Введите id рейса для удаления:")
    if flight_id is not None:
        delete_flight(flight_id)


def main():
    create()

    # Запрашиваем логин
    login = simpledialog.askstring("Вход", "Введите ваш логин:")
    if login != "admin":
        messagebox.showinfo("Доступ", "У вас нет прав для добавления или удаления рейсов.")

    root = tk.Tk()
    root.title("Управление рейсами")
    root.geometry("400x350")
    root.configure(bg="#f0f0f0")

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TButton",
                    font=('Helvetica', 12, 'bold'),
                    foreground='white',
                    background='#2980b9',
                    borderwidth=0,
                    relief='flat',
                    padding=10)

    style.map("TButton",
              foreground=[('!active', 'white')],
              background=[('!active', '#3498db')])

    if login == "admin":
        tk.Button(root, text="Добавить рейс", command=add_flights, bg="#2980b9", fg="white", font=("Helvetica", 12), relief=tk.FLAT).pack(pady=10, fill=tk.X, padx=20)
        tk.Button(root, text="Удалить рейс", command=clear_flight, bg="#e74c3c", fg="white", font=("Helvetica", 12), relief=tk.FLAT).pack(pady=10, fill=tk.X, padx=20)

    tk.Button(root, text="Показать рейсы", command=show_flight, bg="#27ae60", fg="white", font=("Helvetica", 12), relief=tk.FLAT).pack(pady=10, fill=tk.X, padx=20)
    tk.Button(root, text="Выход", command=root.quit, bg="#7f8c8d", fg="white", font=("Helvetica", 12), relief=tk.FLAT).pack(pady=10, fill=tk.X, padx=20)

    root.mainloop()


if __name__ == "__main__":
    main()