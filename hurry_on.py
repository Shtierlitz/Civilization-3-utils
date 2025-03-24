from pynput import keyboard
import pyautogui
import threading

repeat_count = int(input("Введи количество повторений: "))  # Задай нужное количество повторений

current_keys = set()
action_in_progress = threading.Event()


def perform_actions():
    action_in_progress.set()
    try:
        for _ in range(repeat_count):
            if not action_in_progress.is_set():
                print("Выполнение прервано.")
                break
            pyautogui.press('h')
            pyautogui.press('enter')
            pyautogui.press('right')
        else:
            print(f"Выполнено {repeat_count} повторений.")
    finally:
        action_in_progress.clear()


def on_press(key):
    try:
        current_keys.add(key.char)
    except AttributeError:
        pass

    if {'q', 'w', 'e'}.issubset(current_keys) and not action_in_progress.is_set():
        threading.Thread(target=perform_actions).start()


def on_release(key):
    try:
        current_keys.discard(key.char)
    except AttributeError:
        pass

    if key == keyboard.Key.insert:
        return False


print("Скрипт запущен. Для выхода нажми Insert.")

try:
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
except KeyboardInterrupt:
    action_in_progress.clear()
    print("Скрипт принудительно остановлен.")
