import sqlite3
import matplotlib.pyplot as plt
import windows
import os  # Импортируем модуль для работы с путями

# Получаем абсолютный путь к директории скрипта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Формируем путь к базе данных
DB_PATH = os.path.join(BASE_DIR, 'kirieshki.db')

username = ''
first = True

def labels(x, y, add=False):
    for i in range(len(x)):
        plt.text(i+1 if add else i, y[i], y[i], ha='center')

def opened(user):
    global username, first
    username = user
    active_win = windows.wins[3][0]
    if first:
        active_win.myrezult_test.clicked.connect(rez_test)
        active_win.Liderbord_test.clicked.connect(lid_test)
        active_win.vyhod.clicked.connect(vyhod)
        first = False

def rez_test():
    # Используем относительный путь к БД
    BD = sqlite3.connect(DB_PATH)
    cursor = BD.cursor()
    cursor.execute('SELECT Click_score, in_game_time FROM Users WHERE login = ?', (username,))
    Rez = [int(j) for j in cursor.fetchall()[0]]
    BD.close()
    
    plt.clf()
    points = [1, 2]
    labels = ['Клики', 'Время']
    
    plt.stem(points, Rez)
    plt.xticks(points, labels)
    
    for i, val in enumerate(Rez):
        plt.text(points[i], val, str(val), ha='center', va='bottom')
    
    plt.xlim(0, 3)
    plt.ylim(0, 10000)
    plt.show()

def lid_test():
    # Используем относительный путь к БД
    BD = sqlite3.connect(DB_PATH)
    cursor = BD.cursor()
    
    cursor.execute('SELECT login, Click_score, in_game_time FROM Users')
    er = cursor.fetchall()
    BD.close()
    
    logins = [i[0] for i in er]
    click_scores = [int(i[1]) for i in er]
    game_times = [int(i[2]) for i in er]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    ax1.bar(logins, click_scores)
    ax1.set_title('Рекорды кликов')
    ax1.set_ylabel('Количество кликов')
    ax1.set_xticks(range(len(logins)))
    ax1.set_xticklabels(logins, rotation=0, ha='center')
    
    ax2.bar(logins, game_times)
    ax2.set_title('Игровое время')
    ax2.set_ylabel('Время (секунды)')
    ax2.set_xticks(range(len(logins)))
    ax2.set_xticklabels(logins, rotation=0, ha='center')
    
    plt.tight_layout()
    plt.show()

def vyhod():
    windows.wins[3][0].hide()
    windows.wins[2][0].show()
    windows.wins[2][1](username)