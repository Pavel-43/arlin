import tkinter as tk
from tkinter import messagebox
import subprocess
import tkinter as tk
import tkinter.ttk as ttk

def create_window():
    root = tk.Tk()
    root.title("Главное меню")
    root.geometry("400x250")

    label = tk.Label(root, text="Выберите действие:", font=('Helvetica', 16))
    label.pack(pady=20)

    frame = tk.Frame(root)
    frame.pack()

    button_frame = tk.Frame(frame)
    button_frame.pack(side=tk.LEFT, padx=10)

    flight_button = tk.Button(button_frame, text="Рейсы", command=lambda: launch_flights())
    flight_button.pack(fill=tk.X, expand=True)

    client_button = tk.Button(button_frame, text="Клиенты", command=lambda: launch_klients())
    client_button.pack(fill=tk.X, expand=True)

    flight_button = tk.Button(button_frame, text="Авиакомпании", command=lambda: launch_airlines())
    flight_button.pack(fill=tk.X, expand=True)

    flight_button = tk.Button(button_frame, text="Пункты назначения", command=lambda: launch_city())
    flight_button.pack(fill=tk.X, expand=True)

    flight_button = tk.Button(button_frame, text="Бронирование", command=lambda: launch_booking())
    flight_button.pack(fill=tk.X, expand=True)

    root.mainloop()
def launch_flights():
    try:
        subprocess.run(["python", "flights.py"])
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить программу рейсов. Ошибка: {str(e)}")

def launch_klients():
    try:
        subprocess.run(["python", "klients.py"])
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить программу клиентов. Ошибка: {str(e)}")

def launch_airlines():
    try:
        subprocess.run(["python", "airlines.py"])
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить программу авиакомпаний. Ошибка: {str(e)}")

def launch_city():
    try:
        subprocess.run(["python", "city.py"])
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить программу пунктов назначения. Ошибка: {str(e)}")

def launch_booking():
    try:
        subprocess.run(["python", "booking.py"])
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить программу бронирования. Ошибка: {str(e)}")

def mn():
    root = tk.Tk()
    root.title("Выход")
    root.geometry("300x150")  # Увеличиваем размер окна для новой надписи
    root.minsize(250, 100)
    root.maxsize(400, 200)

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

    # Добавляем надпись
    exit_label = tk.Label(root, text="Вы точно хотите выйти?", font=('Helvetica', 12))
    exit_label.pack(pady=20)

    # Модифицируем кнопку выхода
    exit_button = ttk.Button(root, text="Да, выходить", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()
if __name__ == "__main__":
    create_window()