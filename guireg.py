
from pathlib import Path
from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from register_app import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def launch_gui():
    """Запускает файл gui.py в новом процессе и закрывает текущее окно."""
    try:
        # Закрываем текущее окно
        window.destroy()
        # Запускаем gui.py
        subprocess.run(["python", "gui.py"])
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл gui.py не найден.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить gui.py: {str(e)}")

window = Tk()
window.title("Авторизация")
window.geometry("388x241")
window.configure(bg = "#EFD0D0")


canvas = Canvas(
    window,
    bg = "#EFD0D0",
    height = 241,
    width = 388,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    32.0,
    33.0,
    anchor="nw",
    text="Логин",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    32.0,
    82.0,
    anchor="nw",
    text="Пароль",
    fill="#000000",
    font=("Inter", 20 * -1)
)

entry_reg_1 = PhotoImage(
    file=relative_to_assets("entry1_reg.png"))
entry_bg_1 = canvas.create_image(
    218.5,
    48.0,
    image=entry_reg_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=131.0,
    y=33.0,
    width=175.0,
    height=28.0
)

entry_reg_2 = PhotoImage(
    file=relative_to_assets("entry2_reg.png"))
entry_bg_2 = canvas.create_image(
    218.5,
    95.0,
    image=entry_reg_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=131.0,
    y=80.0,
    width=175.0,
    height=28.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_reg1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=launch_gui,
    relief="flat"
)

button_1.place(
    x=131.0,
    y=139.0,
    width=135.0,
    height=35.0
)


button_image_2 = PhotoImage(
    file=relative_to_assets("button_reg2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=show_register_window,
    relief="flat"
)
button_2.place(
    x=107.0,
    y=186.0,
    width=183.0,
    height=35.0
)

window.resizable(False, False)
window.mainloop()


