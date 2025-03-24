import pyautogui
import time

time.sleep(5)  # Move mouse to dropdown
point = pyautogui.position()
print(point)

dropdown_coords = (point.x, point.y)
level_coords = (dropdown_coords[0] - 86, dropdown_coords[1] + 63)
city_coords = (dropdown_coords[0] - 205, dropdown_coords[1] - 91)
add_button_coords = (dropdown_coords[0] - 75, dropdown_coords[1] - 110)

units_positions = {
    '1': ('БТР CV9040', 28, 5, False, False),
    '2': ('Инженер', 2, 5, False, False),
    '3': ('Черная Акула', 29, 3, False, False),
    '4': ('Ракетный крейсер', 19, 3, True, True),
    '5': ('Стелс Бомбардировщик', 17, 1, True, True),
    '6': ('Современный истребитель', 15, 2, True, False),
}

pageup = input("Использовать pageup? (1 - да, 0 - нет): ") == '1'
arrow_up = input("Стрелка вверх? (1 - вверх, 0 - вниз): ") == '1'
page_down_count = int(input("Сколько раз нажать pageup/pagedown?: "))
arrow_count = int(input("Сколько раз нажать вверх/вниз?: "))

unit_counts = {
    '1': int(input("Сколько БТРов?: ")),
    '2': int(input("Сколько инженеров?: ")),
    '4': int(input("Сколько Ракетных крейсеров?: ")),
    '3': int(input("Сколько Акул?: ")),
    '5': int(input("Сколько Бомбардировщиков?: ")),
    '6': int(input("Сколько истребителей?: ")),
}

city_position = (page_down_count, arrow_count, pageup, arrow_up)

level_page_down = 0
level_down = 3

def select_city():
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


def select_unit(unit_key, repeat_count):
    unit_name, page_down_presses, presses_count, invert_page, invert_arrow = units_positions[unit_key]

    for _ in range(repeat_count):
        pyautogui.click(*add_button_coords)
        print(f"Выбираем юнит: {unit_name}")

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

        select_city()

print("Запускаем автоматический выбор юнитов.")

for unit_key, count in unit_counts.items():
    if count > 0:
        select_unit(unit_key, count)

print("Выполнение завершено.")
