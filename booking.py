import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog

def create_bookings_table():
    conn, cur = connect_to_db()
    cur.execute('''CREATE TABLE IF NOT EXISTS Bookings (
                    BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
                    FlightID INTEGER NOT NULL,
                    PassengerID INTEGER NOT NULL,
                    SeatNumber TEXT NOT NULL,
                    DateOfBooking DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (FlightID) REFERENCES Flights(FlightID),
                    FOREIGN KEY (PassengerID) REFERENCES Passengers(PassengerID))''')
    conn.commit()
    close_connection(conn)

def connect_to_db(db_route='airline_sales.db'):
    conn = sqlite3.connect(db_route)
    cur = conn.cursor()
    return conn, cur

def close_connection(conn):
    conn.close()


def insert_booking(flight_id, passenger_id, seat_number):
    conn, cur = connect_to_db()
    sql = '''INSERT INTO Bookings (FlightID, PassengerID, SeatNumber) VALUES (?,?,?)'''
    try:
        cur.execute(sql, (flight_id, passenger_id, seat_number))

        # Получаем текущее количество билетов для данного рейса
        cur.execute("SELECT quantity FROM fligh WHERE id = ?", (flight_id,))
        current_quantity = cur.fetchone()[0]

        # Уменьшаем количество билетов на 1
        new_quantity = max(0, current_quantity - 1)

        # Обновляем количество билетов в таблице Flights
        cur.execute("UPDATE fligh SET quantity = ? WHERE id = ?", (new_quantity, flight_id))

        conn.commit()
        messagebox.showinfo("Всё выполнено верно", "Бронь успешно добавлена в базу данных.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при добавлении бронирования: {e}")
    finally:
        close_connection(conn)


def check_availability(flight_id):
    conn, cur = connect_to_db()
    try:
        cur.execute("SELECT quantity FROM fligh WHERE id = ?", (flight_id,))
        current_quantity = cur.fetchone()[0]

        if current_quantity <= 0:
            messagebox.showerror("Ошибка", f"К сожалению, на рейс {flight_id} больше нет доступных мест.")
            return False

        return True
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при проверке доступности: {e}")
        return False
    finally:
        close_connection(conn)

def delete_booking(booking_id):
    conn, cur = connect_to_db()
    sql = '''DELETE FROM Bookings WHERE BookingID = ?'''
    try:
        cur.execute(sql, (booking_id,))
        conn.commit()
        if cur.rowcount > 0:
            messagebox.showinfo("Всё выполнено верно", f"авиабилет с id {booking_id} удалён.")
        else:
            messagebox.showwarning("Внимание", f"авиабилет с id {booking_id} не найден.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при удалении авиабилета: {e}")
    close_connection(conn)

def add_booking():
    flight_id = simpledialog.askinteger("Выберите рейс", "Введите ID рейса для добавления авиабилета:")
    if flight_id is None:
        return

    if check_availability(flight_id):
        booking_window = tk.Toplevel()
        booking_window.title("Добавить авиабилет")


        passenger_label = tk.Label(booking_window, text="Введите ID пассажира:")
        passenger_label.pack()
        passenger_entry = tk.Entry(booking_window)
        passenger_entry.pack()

        seat_label = tk.Label(booking_window, text="Введите номер места:")
        seat_label.pack()
        seat_entry = tk.Entry(booking_window)
        seat_entry.pack()



        def submit():
            try:
                passenger_id = int(passenger_entry.get())
                seat_number = seat_entry.get()

                if not passenger_id or not seat_number:
                    messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
                    return

                insert_booking(flight_id, passenger_id, seat_number)
                booking_window.destroy()
                messagebox.showinfo("Успех", "Авиабилет успешно добавлен в базу данных.")
            except ValueError as e:
                messagebox.showerror("Ошибка", f"Пожалуйста, введите корректные данные: {e}")

        tk.Button(booking_window, text="Добавление авиабилета", command=submit).pack()
    else:
        messagebox.showwarning("Внимание", "На выбранном рейсе нет доступных мест.")





def withdraw_bookings():
    conn, cur = connect_to_db()
    cur.execute("SELECT * FROM Bookings ORDER BY BookingID DESC")
    rows = cur.fetchall()
    close_connection(conn)
    return rows


def show_bookings():
    bookings = withdraw_bookings()
    if not bookings:
        messagebox.showinfo("Список броней", "Список броней пуст.")
    else:
        bookings_list = []
        for row in bookings:
            formatted_row = [
                f"ID: {row[0]}",
                f"Рейс: {row[1]}",
                f"Пассажир: {row[2]}",
                f"Место: {row[3]}"

            ]

            # Если дата есть, добавляем ее в конец списка
            if len(row) >= 6:
                formatted_row.append(f"Дата бронирования: {row[5]}")

            bookings_list.append(", ".join(formatted_row))

        result = "\n".join(bookings_list)
        messagebox.showinfo("Список броней", result)

def clear_booking():
    booking_id = simpledialog.askinteger("Удалить бронь", "Введите ID бронирования для удаления:")
    if booking_id is not None:
        delete_booking(booking_id)

def main():
    create_bookings_table()

    root = tk.Tk()
    root.title("Управление бронями")
    root.geometry("350x250")
    root.minsize(100, 100)
    root.maxsize(1200, 900)
    style = ttk.Style()
    style.theme_use("clam")

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

    add_button = tk.Button(root, text="Добавить Авиабилет", command=add_booking, bg="#3498db",
                               fg="white", font=("Arial", 12), relief="flat")
    add_button.pack(pady=10)

    show_button = tk.Button(root, text="Показать брони", command=show_bookings, bg="#2ecc71",
                            fg="white", font=("Arial", 12), relief="flat")
    show_button.pack(pady=10)

    remove_button = tk.Button(root, text="Удалить бронь", command=clear_booking,bg="#e74c3c",
                                  fg="white", font=("Arial", 12), relief="flat")
    remove_button.pack(pady=10)

    exit_button = tk.Button(root, text="Выход", command=root.quit,bg="#95a5a6", fg="white", font=("Arial", 12),
                            relief="flat")
    exit_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()

