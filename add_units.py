import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import time
import threading
import keyboard

# Global variables
dropdown_coords = level_coords = city_coords = add_button_coords = None
stop_flag = False

units_positions = {
    '1': ('БТР CV9040', 28, 5, False, False),
    '2': ('Инженер', 2, 5, False, False),
    '3': ('Черная Акула', 29, 3, False, False),
    '4': ('Ракетный крейсер', 19, 3, True, True),
    '5': ('Стелс Бомбардировщик', 17, 1, True, True),
    '6': ('Современный истребитель', 15, 2, True, False),
}

level_page_down = 0
level_down = 3

def set_coords():
    global dropdown_coords, level_coords, city_coords, add_button_coords
    time.sleep(5)
    point = pyautogui.position()

    dropdown_coords = (point.x, point.y)
    level_coords = (dropdown_coords[0] - 86, dropdown_coords[1] + 63)
    city_coords = (dropdown_coords[0] - 205, dropdown_coords[1] - 91)
    add_button_coords = (dropdown_coords[0] - 75, dropdown_coords[1] - 110)

    messagebox.showinfo("Координаты", "Координаты успешно записаны!")

def select_city(city_position):
    city_pagedown, city_down, invert_page, invert_arrow = city_position

    pyautogui.click(*city_coords)
    pyautogui.press('end' if invert_page else 'home')
    if city_pagedown:
        for _ in range(city_pagedown):
            pyautogui.press('pageup' if invert_page else 'pagedown')

    if city_down:
        for _ in range(city_down):
            pyautogui.press('up' if invert_arrow else 'down')

    pyautogui.press('enter')


def select_unit(unit_key, repeat_count, city_position):
    global stop_flag
    unit_name, page_down_presses, presses_count, invert_page, invert_arrow = units_positions[unit_key]

    for _ in range(repeat_count):
        if stop_flag:
            break

        pyautogui.click(*add_button_coords)

        pyautogui.click(*dropdown_coords)
        pyautogui.press('end' if invert_page else 'home')
        for _ in range(page_down_presses):
            pyautogui.press('pageup' if invert_page else 'pagedown')
        for _ in range(presses_count):
            pyautogui.press('up' if invert_arrow else 'down')
        pyautogui.press('enter')

        pyautogui.click(*level_coords)
        pyautogui.press('home')
        for _ in range(level_page_down):
            pyautogui.press('pagedown')
        for _ in range(level_down):
            pyautogui.press('down')
        pyautogui.press('enter')

        select_city(city_position)

    if stop_flag:
        messagebox.showinfo("Прерывание", "Работа программы остановлена пользователем!")

def process_thread():
    global stop_flag
    stop_flag = False

    pageup = pageup_var.get()
    arrow_up = arrow_var.get()
    page_down_count = int(page_down_entry.get())
    arrow_count = int(arrow_count_entry.get())

    unit_counts = {
        '1': int(btr_entry.get()),
        '2': int(eng_entry.get()),
        '3': int(shark_entry.get()),
        '4': int(cruiser_entry.get()),
        '5': int(bomber_entry.get()),
        '6': int(fighter_entry.get()),
    }

    city_position = (page_down_count, arrow_count, pageup, arrow_up)

    keyboard.add_hotkey('esc', lambda: globals().update(stop_flag=True))

    for unit_key, count in unit_counts.items():
        if stop_flag:
            break
        if count > 0:
            select_unit(unit_key, count, city_position)

    if not stop_flag:
        messagebox.showinfo("Готово", "Выполнение завершено!")

    keyboard.remove_all_hotkeys()

def start_process():
    threading.Thread(target=process_thread).start()

# GUI
root = tk.Tk()
root.title("Unit Selector")
root.geometry("350x500")

tk.Button(root, text="Записать координаты (5 сек)", command=set_coords).pack(pady=10)

pageup_var = tk.BooleanVar()
arrow_var = tk.BooleanVar()
tk.Checkbutton(root, text="Использовать pageup", variable=pageup_var).pack()
tk.Checkbutton(root, text="Стрелка вверх", variable=arrow_var).pack()

page_down_entry = ttk.Entry(root)
page_down_entry.insert(0, "0")
tk.Label(root, text="Сколько раз pageup/pagedown:").pack()
page_down_entry.pack()

arrow_count_entry = ttk.Entry(root)
arrow_count_entry.insert(0, "0")
tk.Label(root, text="Сколько раз вверх/вниз:").pack()
arrow_count_entry.pack()

entries = []
labels = ["Сколько БТРов:", "Сколько инженеров:", "Сколько Акул:",
          "Сколько крейсеров:", "Сколько бомбардировщиков:", "Сколько истребителей:"]

for label in labels:
    tk.Label(root, text=label).pack()
    entry = ttk.Entry(root)
    entry.insert(0, "0")
    entry.pack()
    entries.append(entry)

btr_entry, eng_entry, shark_entry, cruiser_entry, bomber_entry, fighter_entry = entries

tk.Button(root, text="Запустить", command=start_process).pack(pady=15)

root.mainloop()


# To create exe use: pyinstaller --name "CIV3 add units" --onefile --noconsole --icon="add_units_icon.ico" add_units.py