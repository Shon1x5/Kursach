import windows  # импортирование модуля содержащего окна и приложение
import sqlite3  # импрортирование библиотеки для работы с БД
import subprocess  # для запуска внешних программ
import os  # для работы с путями
from games import run_game

# Получаем путь к директории с программой
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

first = True  # переменная для проверки первый ли раз запущенно окно

def opened(login=None):  # функция открытия окна
    active_win = windows.wins[1][0]  # записываем текущее окно в переменную для простоты

    # скрываем уведомления которые изначально ненужны
    active_win.NoLogin.hide()
    active_win.NoPassword.hide() 

    active_win.Password.setText('')  # очищаем поле пароля

    if login is not None: 
        windows.wins[1][0].Login.setText(login)  # если получили логин, устанавливаем его

    global first
    if first:  # если сработала в первый раз - привязываем функции на кнопки
        active_win.Vhod.clicked.connect(log)  # привязывает функцию log на кнопку Vhod
        active_win.Reg.clicked.connect(open_reg)  # привязывает функцию open_reg на кнопку Reg
        first = False  # указывает что первый запуск функции уже произошел

def log():  # функция логина
    login = windows.wins[1][0].Login.text()  # записываем введенный логин
    password = windows.wins[1][0].Password.text()  # записываем введенный пароль
    
    # Путь к БД относительно расположения скрипта
    db_path = os.path.join(BASE_DIR, 'kirieshki.db')
    
    connection = sqlite3.connect(db_path)  # подключаем БД
    cursor = connection.cursor()  # создаем "курсор" для запросов
    cursor.execute('SELECT Login, Password FROM users')  # запрос данных пользователей
    users = {i[0]:i[1] for i in cursor.fetchall()}  # создаем словарь пользователей
    connection.close()  # отключение БД

    if login in users.keys():  # если логин существует в БД
        windows.wins[1][0].NoLogin.hide()  # скрываем уведомление о неверном логине

        if users[login] == password:  # если пароль верный
            windows.wins[1][0].NoPassword.hide()
            windows.wins[1][0].hide()  # скрываем текущее окно
            windows.wins[2][0].show()
            windows.wins[2][1](login)
        else:
            windows.wins[1][0].NoPassword.show()  # неверный пароль

    else:
        windows.wins[1][0].NoLogin.show()  # логин не найден

def open_reg():  # функция перехода к регистрации
    windows.wins[1][0].hide()  # скрываем текущее окно
    windows.wins[0][0].show()  # открываем окно регистрации
    windows.wins[0][1]()  # запускаем его обработчик