import windows # импортирование модуля содержащего окна и приложение
import sqlite3 # импрортирование библиотеки для работы с БД
import subprocess # для запуска внешних программ
from games import run_game

first = True # переменная для проверки первый ли раз запущенно окно
def opened(login = None): # функция открытия окна, имеет возможность получить на вход лигин (не обязательно, т.к. есть значение поумолчанию)
    active_win = windows.wins[1][0] # записываем текущее окно в переменную для простоты

    # скрываем уведомления которые изначально ненужны
    active_win.NoLogin.hide()
    active_win.NoPassword.hide() 

    active_win.Password.setText('') # очищаем поле пароля для предотвращения, получения доступа другими людьми

    if login != None : windows.wins[1][0].Login.setText(login) # если получили логин, устанавливаем его в поле логина

    global first
    if first: # если сработала в первый раз - призязывает фунции на кновки
        active_win.Vhod.clicked.connect(log) # привязывает функцию log на кнопку Vhod
        active_win.Reg.clicked.connect(open_reg) # привязывает функцию open_reg на кнопку Reg
        first = False # указывает что первый запуск функции уже произошел

def log(): # функция логина
    login = windows.wins[1][0].Login.text() # записываем введенный логин в переменную для удобства
    password = windows.wins[1][0].Password.text() # записываем введеный пароль в переменную для удобства

    connection = sqlite3.connect('kirieshki.db') # подключаем БД
    cursor = connection.cursor() # создаем "курсор" для запросов
    cursor.execute('SELECT Login, Password FROM users') # создаем запрос получение логинов и паролей из БД
    users = {i[0]:i[1] for i in cursor.fetchall()} # создаем из полученных данных словарь пользователей формата {логин:пароль}
    connection.close() # отключение БД

    if login in users.keys(): # если введеный логин существует в БД продолжаем вход
        windows.wins[1][0].NoLogin.hide() # скрываем уведомление о неверном логине

        if users[login] == password: # если введенный пароль подходит - входим
            windows.wins[1][0].NoPassword.hide() # скрываем уведомление о неверном пароле
            windows.wins[1][0].hide() # скрываем текущее окно

            run_game(login)
            windows.app.quit()

        else:
            windows.wins[1][0].NoPassword.show() # если пароль не подошел уведомляем об этом

    else:
        windows.wins[1][0].NoLogin.show() # если логин не обнаружен уведомляем о этом

def open_reg(): # функция обработчик кнопки перехода к регистрации
    windows.wins[1][0].hide() # скрвываем текущее окно
    windows.wins[0][0].show() # открываем окно регистрации
    windows.wins[0][1]() # запускаем его обработчик

