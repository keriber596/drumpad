import sys
from PyQt5 import uic
from PyQt5 import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, \
    QColorDialog
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from math import sqrt
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import simpleaudio
import os

BTN_COLOR = "#0f2fff"

DEFAULT_STYLE = f'outline: none;' \
                f'cursor: pointer;' \
                f'background: none;' \
                f'transition: .5s;' \
                f'font-size: 16px;' \
                f'border-radius: 5px;' \
                f'font-family: sans-serif;' \
                f'border: 2px solid {BTN_COLOR};' \
                f'color:  {BTN_COLOR};' \
                f'width:120px;' \
                f'height:60px;'

# "заплатка" до добаления баз данный
current_user = "Гость"
color = "rgb(255, 255, 255)"
connect = sqlite3.connect('main.sqlite')
default_presets = "acoustic.txt;roland-808.txt"


# проигрыватель
def play(filename):
    wave_obj = simpleaudio.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DRUMPAD")
        uic.loadUi('drum.ui', self)
        if current_user == "Гость":
            self.presets_list = ["acoustic.txt", "roland-808.txt"]
        self.label.setText(current_user)
        self.preset_change()
        for i in range(len(self.presets_list)):
            i1 = open(self.presets_list[i], "r", encoding="UTF-8").readline().strip("\n")
            self.comboBox.insertItem(i, i1)
        self.comboBox.currentIndexChanged.connect(self.preset_change)
        self.pushButton.clicked.connect(self.menu_open)

    # открытие пресетов, по умолчанию откарывается 2 пресета
    def open_preset(self, fname):
        f = open(fname, mode="r", encoding="UTF-8")
        self.title = f.readline()
        self.samples = [i.strip("\n").split(";") for i in f.readlines()]

    def keyPressEvent(self, event):
        self.index = -1
        if not event.modifiers():
            for i in range(len(self.samples)):
                if chr(event.key()) in self.samples[i]:
                    self.index = i
            if self.index != -1:
                play(self.samples[self.index][0])
        else:
            pass

    def clicked(self):
        name = self.sender().text()
        for i in range(len(self.samples)):
            if name in self.samples[i]:
                index = i
                play(self.samples[index][0])
                break

    def preset_change(self):
        self.open_preset(self.presets_list[self.comboBox.currentIndex()])
        self.x = int(sqrt(len(self.samples)))
        self.open_preset(self.presets_list[self.comboBox.currentIndex()])
        if self.x == sqrt(len(self.samples)):
            self.setGeometry(300, 100, 20 + 130 * self.x, 90 + 70 * self.x)
        else:
            self.setGeometry(300, 100, 20 + 130 * (self.x + 1), 90 + 70 * self.x)
        for i in range(len(self.samples)):
            exec(f"self.button{i} = QPushButton('{self.samples[i][1]}', self)")
            exec(f"self.button{i}.resize(120, 60)")
            exec(
                f"self.button{i}.move({20 + int((i) / self.x) * 130}, "
                f"{90 + ((i) % self.x) * 70})")
            exec(f'self.button{i}.setStyleSheet("{DEFAULT_STYLE}")')
            exec(f'self.button{i}.clicked.connect(self.clicked)')

    def menu_open(self):
        self.menu_window = MenuWindow()
        self.menu_window.show()


# окно меню
class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("menu.ui", self)
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.color_change)

    def login(self):
        self.login_window = LoginWindow()
        self.login_window.show()

    def color_change(self):
        color = QColorDialog.getColor().getRgb()
        self.setStyleSheet(f"background-color:rgb({color[0]}, {color[1]}, {color[2]})")
        ex.setStyleSheet(f"background-color:rgb({color[0]}, {color[1]}, {color[2]})")


# окно входа
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("login_form.ui", self)
        self.pushButton_2.clicked.connect(self.register)
        self.id = 0

    def register(self):
        self.label.hide()
        self.pushButton_2.hide()
        self.pushButton.resize(165, 31)
        self.pushButton.move(100, 180)
        self.pushButton.setText("Зарегистрироваться")
        self.pushButton.clicked.connect(self.add_user)

    def add_user(self):
        login = self.lineEdit.text()
        pwd = self.lineEdit_2.text()
        cursor = connect.cursor()
        c = cursor.execute(f"INSERT INTO users"
                           f" (id, username, password, presets_list)"
                           f"VALUES"
                           f"({self.id}, '{login}', '{generate_password_hash(pwd)}', "
                           f"'{default_presets}')")
        connect.commit()
        self.id += 1


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
