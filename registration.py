import sqlite3
import os
import windows

# Получаем путь к директории скрипта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'kirieshki.db')

first = True

def opened():
    active_win = windows.wins[0][0]
    
    # скрываем уведомления
    active_win.Zanyat.hide()
    active_win.Nesovpaw.hide()
    active_win.EmptyLog.hide()
    active_win.EmptyPass.hide()
    
    global first
    if first:
        active_win.Reg.clicked.connect(regs)
        active_win.Vhod.clicked.connect(open_vhod)
        first = False

def regs():
    ok = True
    
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute('SELECT Login FROM users')
        users = [i[0] for i in cursor.fetchall()]
        connection.close()
    except sqlite3.Error as e:
        print(f"Ошибка базы данных: {e}")
        return

    if windows.wins[0][0].Login.text() in users:
        ok = False
        windows.wins[0][0].Zanyat.show()
    else:
        windows.wins[0][0].Zanyat.hide()

    if windows.wins[0][0].Password.text() != windows.wins[0][0].Password_repeat.text():
        ok = False
        windows.wins[0][0].Nesovpaw.show()
    else:
        windows.wins[0][0].Nesovpaw.hide()

    if windows.wins[0][0].Login.text() == '':
        windows.wins[0][0].EmptyLog.show()
        ok = False
    else:
        windows.wins[0][0].EmptyLog.hide()

    if windows.wins[0][0].Password.text() == '':
        windows.wins[0][0].EmptyPass.show()
        ok = False
    else:
        windows.wins[0][0].EmptyPass.hide()

    if ok:
        try:
            connection = sqlite3.connect(DB_PATH)
            cursor = connection.cursor()
            cursor.execute('INSERT INTO users (Login, Password, Click_score, in_game_time) VALUES (?, ?, ?, ?)',
                         (windows.wins[0][0].Login.text(),
                          windows.wins[0][0].Password.text(),
                          0,
                          0))
            connection.commit()
            connection.close()

            windows.wins[0][0].hide()
            windows.wins[1][0].show()
            windows.wins[1][1](windows.wins[0][0].Login.text())
        except sqlite3.Error as e:
            print(f"Ошибка при сохранении данных: {e}")

def open_vhod():
    windows.wins[0][0].hide()
    windows.wins[1][0].show()
    windows.wins[1][1]()