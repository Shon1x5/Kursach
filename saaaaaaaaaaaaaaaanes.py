import windows
import games
import os

# Получаем базовый путь
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USER = ''
first = True

def opened(UserName):
    global USER, first
    active_win = windows.wins[2][0]
    USER = UserName
    active_win.UserName.setText(UserName)
    if first:       
        active_win.Igra.clicked.connect(Igra)
        active_win.Graphics.clicked.connect(Graphics)
        active_win.Vyhod.clicked.connect(Vyhod)
        first = False

def Igra():
    windows.wins[2][0].hide()
    # Убираем параметр base_dir, так как run_game его не принимает
    games.run_game(USER)  
    windows.wins[2][0].show()

def Graphics():
    windows.wins[2][0].hide()
    windows.wins[3][0].show()
    windows.wins[3][1](USER)

def Vyhod():
    windows.wins[2][0].hide()
    windows.wins[1][0].show()
    windows.wins[1][1]()