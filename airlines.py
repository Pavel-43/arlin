import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog

def create_airlines_table():
    conn, cur = connect_to_db()
    cur.execute('''CREATE TABLE IF NOT EXISTS Airlines (
                    AirlineID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT NOT NULL,
                    Country TEXT NOT NULL,
                    Founded DATE NOT NULL,
                    Headquarters TEXT NOT NULL)''')
    conn.commit()
    close_connection(conn)

def connect_to_db(db_route='airline_sales.db'):
    conn = sqlite3.connect(db_route)
    cur = conn.cursor()
    return conn, cur

def close_connection(conn):
    conn.close()

def insert_airline(name, country, founded, headquarters):
    conn, cur = connect_to_db()
    sql = '''INSERT INTO Airlines (Name, Country, Founded, Headquarters) VALUES (?, ?, ?, ?)'''
    try:
        cur.execute(sql, (name, country, founded, headquarters))
        conn.commit()
        messagebox.showinfo("Успешно", f"Авиакомпания '{name}' добавлена в базу данных.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при добавлении авиакомпании: {e}")
    close_connection(conn)

def withdraw_airlines():
    conn, cur = connect_to_db()
    cur.execute("SELECT * FROM Airlines")
    rows = cur.fetchall()
    close_connection(conn)
    return rows

def delete_airline(airline_id):
    conn, cur = connect_to_db()
    sql = '''DELETE FROM Airlines WHERE AirlineID = ?'''
    try:
        cur.execute(sql, (airline_id,))
        conn.commit()
        if cur.rowcount > 0:
            messagebox.showinfo("Успешно", f"Авиакомпания с id {airline_id} удалена.")
        else:
            messagebox.showwarning("Внимание", f"Авиакомпания с id {airline_id} не найдена.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при удалении авиакомпании: {e}")
    close_connection(conn)

def add_airlines():
    airline = tk.Toplevel()
    airline.title("Добавить авиакомпанию")
    airline.geometry("400x400")
    airline.configure(bg="#f0f0f0")

    tk.Label(airline, text="Введите название:", bg="#f0f0f0", fg="#333", font=("Helvetica", 12)).pack(pady=5)
    name_entry = tk.Entry(airline, font=("Helvetica", 12))
    name_entry.pack(pady=5, padx=20, fill=tk.X)

    tk.Label(airline, text="Введите страну:", bg="#f0f0f0", fg="#333", font=("Helvetica", 12)).pack(pady=5)
    country_entry = tk.Entry(airline, font=("Helvetica", 12))
    country_entry.pack(pady=5, padx=20, fill=tk.X)

    tk.Label(airline, text="Введите дату основания:", bg="#f0f0f0", fg="#333", font=("Helvetica", 12)).pack(pady=5)
    founded_entry = tk.Entry(airline, font=("Helvetica", 12))
    founded_entry.pack(pady=5, padx=20, fill=tk.X)

    tk.Label(airline, text="Введите место расположения штаб-квартиры:", bg="#f0f0f0", fg="#333", font=("Helvetica", 12)).pack(pady=5)
    headquarters_entry = tk.Entry(airline, font=("Helvetica", 12))
    headquarters_entry.pack(pady=5, padx=20, fill=tk.X)

    def submit():
        name = name_entry.get()
        country = country_entry.get()
        founded = founded_entry.get()
        headquarters = headquarters_entry.get()
        if not name or not country or not founded or not headquarters:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
            return

        insert_airline(name, country, founded, headquarters)
        airline.destroy()

    tk.Button(airline, text="Добавить авиакомпанию", command=submit, bg="#2980b9", fg="white", font=("Helvetica", 12), relief=tk.FLAT).pack(pady=20)

def show_airlines():
    airlines = withdraw_airlines()
    if not airlines:
        messagebox.showinfo("Список авиакомпаний", "Список авиакомпаний пуст.")
    else:
        airlines_list = "\n".join(
            [f"ID: {row[0]}, Название: {row[1]}, Страна: {row[2]}, Дата основания: {row[3]}, Штаб-квартира: {row[4]}" for row in airlines])
        messagebox.showinfo("Список авиакомпаний", airlines_list)

def clear_airline():
    airline_id = simpledialog.askinteger("Удалить авиакомпанию", "Введите id авиакомпании для удаления:")
    if airline_id is not None:
        delete_airline(airline_id)

def main():
    create_airlines_table()

    # Запрашиваем логин
    login = simpledialog.askstring("Вход", "Введите ваш логин:")
    if login != "admin":
        messagebox.showinfo("Доступ", "У вас нет прав для добавления или удаления авиакомпаний.")

    root = tk.Tk()
    root.title("Управление авиакомпаниями")
    root.geometry("350x250")
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
        tk.Button(root, text="Добавить авиакомпанию", command=add_airlines, bg="#2980b9", fg="white", font=("Helvetica", 12), relief=tk.FLAT).pack(pady=10, fill=tk.X, padx=20)
        tk.Button(root, text="Удалить авиакомпанию", command=clear_airline, bg="#e74c3c", fg="white", font=("Helvetica", 12), relief=tk.FLAT).pack(pady=10, fill=tk.X, padx=20)

    tk.Button(root, text="Показать авиакомпании", command=show_airlines, bg="#27ae60", fg="white", font=("Helvetica", 12), relief=tk.FLAT).pack(pady=10, fill=tk.X, padx=20)
    tk.Button(root, text="Выход", command=root.quit, bg="#7f8c8d", fg="white", font=("Helvetica", 12), relief=tk.FLAT).pack(pady=10, fill=tk.X, padx=20)

    root.mainloop()

if __name__ == "__main__":
    main()