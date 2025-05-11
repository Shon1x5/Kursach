from PyQt5 import uic, QtWidgets #импоротирование необходимых частей из PyQT

#импортирование своих файлов 
import registration
import login
import uwu
import saaaaaaaaaaaaaaaanes


#создание основного приложения
app = QtWidgets.QApplication([])

#создание окон на основе форм созданых в QtDesigner
registration_win = uic.loadUi("registration_form.ui")
login_win = uic.loadUi("login_form.ui")
uwu_win = uic.loadUi("uwu.ui")
sans_win = uic.loadUi("saaaaaaaaaaaaaaaanes.ui")

#создание списка окон и функций обрабатывающих их, чтобы упростить переход между ними. Список имеет формат [ (окно1, функция-обработчик1), (окно2, функция-обработчик2) ...]
wins = [(registration_win, registration.opened),
        (login_win, login.opened),
        (sans_win, saaaaaaaaaaaaaaaanes.opened),
        (uwu_win, uwu.opened)]