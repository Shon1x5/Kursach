from PyQt5 import uic, QtWidgets
import os
import sys

# Импортирование своих модулей
import registration
import login
import uwu
import saaaaaaaaaaaaaaaanes

# Получение абсолютного пути к директории скрипта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Создание основного приложения
app = QtWidgets.QApplication([])

# Функция для загрузки UI-файлов с относительными путями
def load_ui_file(ui_filename):
    ui_path = os.path.join(BASE_DIR, ui_filename)
    if not os.path.exists(ui_path):
        print(f"Ошибка: файл {ui_path} не найден")
        sys.exit(1)
    return uic.loadUi(ui_path)

# Создание окон с использованием относительных путей
registration_win = load_ui_file("registration_form.ui")
login_win = load_ui_file("login_form.ui")
uwu_win = load_ui_file("uwu.ui")
sans_win = load_ui_file("saaaaaaaaaaaaaaaanes.ui")

# Список окон и их обработчиков
wins = [
    (registration_win, registration.opened),
    (login_win, login.opened),
    (sans_win, saaaaaaaaaaaaaaaanes.opened),
    (uwu_win, uwu.opened)
]