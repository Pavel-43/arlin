from pathlib import Path
from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from BD import *
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = Path(r"assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.title("Продажа Авиабилетов")
window.geometry("838x605")
window.configure(bg = "#4D0B2B")


canvas = Canvas(
    window,
    bg = "#4D0B2B",
    height = 605,
    width = 838,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    206.0,
    155.0,
    image=image_image_1
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=mn,
    relief="flat"
)
button_1.place(
    x=633.0,
    y=519.0,
    width=168.0,
    height=51.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=116.0,
    y=519.0,
    width=168.0,
    height=55.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=launch_city,
    relief="flat"
)
button_3.place(
    x=632.0,
    y=412.0,
    width=168.0,
    height=51.0
)

canvas.create_text(
    475.0,
    39.0,
    anchor="nw",
    text="Добро Пожаловать!",
    fill="#FFFFFF",
    font=("Inter SemiBold", 32 * -1)
)

canvas.create_text(
    400.0,
    226.0,
    anchor="nw",
    text="Выберите пожалуйста, то что хотели бы сделать или узнать\n",
    fill="#FFFFFF",
    font=("Inter SemiBold", 16 * -1)
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=launch_flights,
    relief="flat"
)
button_4.place(
    x=116.0,
    y=412.0,
    width=168.0,
    height=58.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=launch_klients,
    relief="flat"
)
button_5.place(
    x=370.0,
    y=412.0,
    width=168.0,
    height=55.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=launch_airlines,
    relief="flat"
)
button_6.place(
    x=137.0,
    y=538.0,
    width=126.0,
    height=30.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=launch_booking,
    relief="flat"
)
button_7.place(
    x=370.0,
    y=519.0,
    width=168.0,
    height=55.0
)
window.resizable(False, False)
window.mainloop()
