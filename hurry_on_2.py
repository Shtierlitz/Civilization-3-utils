import threading
import time
import tkinter as tk

import pyautogui
from pynput import keyboard


class AutoKeyPresser:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Key Presser")

        self.repeat_count = tk.IntVar(value=10)
        self.action_in_progress = threading.Event()

        tk.Label(root, text="Количество повторений:").pack(pady=5)
        self.repeat_entry = tk.Entry(root, textvariable=self.repeat_count)
        self.repeat_entry.pack(pady=5)

        self.status_label = tk.Label(root, text="Ожидание команды (Q+W+E)")
        self.status_label.pack(pady=5)

        self.start_button = tk.Button(root, text="Запустить слушатель", command=self.start_listener)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Остановить выполнение", command=self.stop_actions)
        self.stop_button.pack(pady=5)

        self.current_keys = set()

    def perform_actions(self):
        self.action_in_progress.set()
        count = self.repeat_count.get()
        self.status_label.config(text=f"Выполняется {count} повторений...")
        try:
            for _ in range(count):
                if not self.action_in_progress.is_set():
                    self.status_label.config(text="Выполнение прервано.")
                    return
                pyautogui.press('h')
                time.sleep(0.02)
                pyautogui.press('enter')
                time.sleep(0.02)
                pyautogui.press('right')
                time.sleep(0.02)
            self.status_label.config(text=f"Выполнено {count} повторений.")
        finally:
            self.action_in_progress.clear()

    def on_press(self, key):
        try:
            self.current_keys.add(key.char)
        except AttributeError:
            pass

        if {'q', 'w', 'e'}.issubset(self.current_keys) and not self.action_in_progress.is_set():
            threading.Thread(target=self.perform_actions).start()

    def on_release(self, key):
        try:
            self.current_keys.discard(key.char)
        except AttributeError:
            pass

        if key == keyboard.Key.insert:
            self.listener.stop()
            self.status_label.config(text="Слушатель остановлен.")

    def start_listener(self):
        self.status_label.config(text="Слушатель запущен. Ожидание Q+W+E.")
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def stop_actions(self):
        self.action_in_progress.clear()
        self.status_label.config(text="Выполнение остановлено.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoKeyPresser(root)
    root.mainloop()

# To create exe use: pyinstaller --name "CIV3 speed up" --onefile --noconsole --icon="Status_Effect-Speed_Up.ico" hurry_on_2.py
