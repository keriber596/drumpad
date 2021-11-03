import sys
from PyQt5 import uic
from PyQt5 import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QPushButton
from math import sqrt
import simpleaudio

BTN_COLOR = "#0f2fff"
CLICKED_STYLE = f"background-color: {BTN_COLOR};transition: all 0.3s ease-in-out;" \
                f"border: none;color: white;transform:scale(1.1);" \
                f'cursor: pointer;' \
                f'font-size: 16px;' \
                f'border-radius: 5px;' \
                f'font-family: sans-serif;' \
                f'border: 2px solid {BTN_COLOR};' \
                f'color:  rgb(255, 255, 255);'
print(CLICKED_STYLE)

# "заплатка" до добаления баз данный
current_user = "guest"


# проигрыватель
def play(filename):
    wave_obj = simpleaudio.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('drum.ui', self)
        if current_user == "guest":
            self.presets_list = ["acoustic.txt"]
        self.open_preset(self.presets_list[0])
        self.x = int(sqrt(len(self.samples)))
        self.preset_change()
        for i in range(len(self.presets_list)):
            i1 = open(self.presets_list[i], "r", encoding="UTF-8").readline().strip("\n")
            self.comboBox.insertItem(i, i1)
        self.comboBox.currentIndexChanged.connect(self.preset_change)
        self.count = 1

    # открытие пресетов, по умолчанию откарывается 2 пресета
    def open_preset(self, fname):
        f = open(fname, mode="r", encoding="UTF-8")
        self.title = f.readline()
        self.samples = [i.strip("\n").split(";") for i in f.readlines()]

    def keyPressEvent(self, event):
        index = -1
        if not event.modifiers():
            for i in self.samples:
                if chr(event.key()) in i:
                    index = self.samples.index(i)
            if index != -1:
                play(self.samples[index][1])
                exec(f'self.button{index}.setStyleSheet("{CLICKED_STYLE}")')

    # изменение кнопок и размера окна при смене пресета
    def preset_change(self):
        if self.comboBox.currentIndex() < len(self.presets_list):
            self.open_preset(self.presets_list[self.comboBox.currentIndex()])
            self.setGeometry(300, 100, 20 + 130 * (self.x + 1), 90 + 70 * self.x)
            for i in range(1, len(self.samples)):
                exec(f"self.button{i} = QPushButton('{self.samples[i][0]}', self)")
                exec(f"self.button{i}.resize(120, 60)")
                exec(
                    f"self.button{i}.move({20 + int((i - 1) / self.x) * 130}, "
                    f"{90 + ((i - 1) % self.x) * 70})")
                exec(f'self.button{i}.setStyleSheet("outline: none;'
                     f'cursor: pointer;'
                     f'background: none;'
                     f'transition: .5s;'
                     f'font-size: 16px;'
                     f'border-radius: 5px;'
                     f'font-family: sans-serif;'
                     f'border: 2px solid {BTN_COLOR};'
                     f'color:  {BTN_COLOR};'
                     f'width:120px;'
                     f'height:60px;")')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
