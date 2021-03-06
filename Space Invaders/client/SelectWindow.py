import sys
from multiprocessing import Process
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon

from client import Game
from utilities.sc_selection import SpaceshipSelection

from config import cfg


def __start_game_process__(player_id, player_spacecraft):
    process = Process(target=__start_game__, args=(player_id, player_spacecraft))
    # process.daemon = True
    process.start()


def __start_game__(player_id, player_spacecraft):
    app = QApplication(sys.argv)
    game = Game.Game(
        player_id=player_id,
        player_spacecraft=player_spacecraft
    )
    game.show()
    sys.exit(app.exec_())


def __start_mp_game_process__(player1_id, player1_spacecraft, player2_id, player2_spacecraft):
    process = Process(target=__start_game_mp__, args=(player1_id, player1_spacecraft, player2_id, player2_spacecraft))
    # process.daemon = True
    process.start()


def __start_game_mp__(player1_id, player1_spacecraft, player2_id, player2_spacecraft):
    app = QApplication(sys.argv)
    game = Game.Game(
        player_id=player1_id,
        player_spacecraft=player1_spacecraft,
        player2_id=player2_id,
        player2_spacecraft=player2_spacecraft
    )
    game.show()
    sys.exit(app.exec_())


class SelectWindow(QMainWindow):

    def __init__(self, players: int):
        super().__init__()
        self.num_of_players = players

        self.select_spaceship_thread = SpaceshipSelection(self.num_of_players)
        self.select_spaceship_thread.selection1_changed.connect(self.update_img)
        self.select_spaceship_thread.selection2_changed.connect(self.update_img2)
        self.select_spaceship_thread.start()

        self.init_ui()
        self.nickname_input.setFocus()

    @pyqtSlot(str)
    def update_img2(self, name: str):
        self.spacecraft2_preview.setPixmap(QPixmap(name))

    @pyqtSlot(str)
    def update_img(self, name: str):
        self.spacecraft_preview.setPixmap(QPixmap(name))

    def init_ui(self):
        self.setFixedSize(cfg.SELECT_WINDOW_WIDTH, cfg.SELECT_WINDOW_HEIGHT)
        self.setWindowTitle('SELECT - Space Invaders v1.0')
        self.setWindowIcon(QIcon('images/icon.png'))

        self.background = QLabel(self)
        # if bg is not shown then in line below change to '../images/bg-res...' in QPixmap
        self.background.setPixmap(QPixmap('images/bg-resized2.jpg'))
        self.background.setGeometry(0, 0, 950, 778)

        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(60, 20, 561, 401))
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)

        self.selected_spacecraft = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.selected_spacecraft.addItem("SILVER_X 177p")
        self.selected_spacecraft.addItem("purpleZ AAx9")
        self.selected_spacecraft.addItem("military-aircraft-POWER")
        self.selected_spacecraft.addItem("SpaceX-air4p66")

        self.select_spaceship_thread.spacecrafts1 = self.selected_spacecraft

        self.gridLayout_2.addWidget(self.selected_spacecraft, 2, 1, 1, 1)

        self.select_ship_label = QLabel(self)
        self.select_ship_label.setText('select spacecraft: ')
        self.select_ship_label.setStyleSheet("color: rgb(255, 237, 226);\n"
                                             "font: 20pt \"Bahnschrift SemiLight\";")
        self.gridLayout_2.addWidget(self.select_ship_label, 2, 0, 1, 1)

        self.nickname_input = QLineEdit(self)
        self.nickname_input.setStyleSheet(
            "background-color:transparent;font: 18pt \"Bahnschrift SemiLight\";color: rgb(255, 237, 226);")
        self.gridLayout_2.addWidget(self.nickname_input, 1, 1, 1, 1)

        self.name_label = QLabel(self)
        self.name_label.setText("player nickname: ")
        self.name_label.setStyleSheet("color: rgb(255, 237, 226);\n"
                                      "font: 20pt \"Bahnschrift SemiLight\";")
        self.gridLayout_2.addWidget(self.name_label, 1, 0, 1, 1)

        self.spacecraft_preview = QLabel(self)
        self.spacecraft_preview.setStyleSheet("border-color: rgb(255, 228, 206);\n"
                                              "border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
                                              "stop:0 rgba(0, 0, 0, 255), "
                                              "stop:1 rgba(255, 255, 255, 255));")
        self.spacecraft_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_2.addWidget(self.spacecraft_preview, 3, 1, 1, 1)

        if self.num_of_players == 2:
            self.nickname_input2 = QLineEdit(self)
            self.nickname_input2.setStyleSheet(
                "background-color:transparent;font: 18pt \"Bahnschrift SemiLight\";color: rgb(255, 237, 226);")
            self.gridLayout_2.addWidget(self.nickname_input2, 4, 1, 1, 1)

            self.name_label2 = QLabel(self)
            self.name_label2.setText("player 2 nickname: ")
            self.name_label2.setStyleSheet("color: rgb(255, 237, 226);\n"
                                           "font: 20pt \"Bahnschrift SemiLight\";")
            self.gridLayout_2.addWidget(self.name_label2, 4, 0, 1, 1)

            self.selected_spacecraft2 = QtWidgets.QComboBox(self.gridLayoutWidget)
            self.selected_spacecraft2.addItem("SILVER_X 177p")
            self.selected_spacecraft2.addItem("purpleZ AAx9")
            self.selected_spacecraft2.addItem("military-aircraft-POWER")
            self.selected_spacecraft2.addItem("SpaceX-air4p66")

            self.select_spaceship_thread.spacecrafts2 = self.selected_spacecraft2

            self.gridLayout_2.addWidget(self.selected_spacecraft2, 5, 1, 1, 1)

            self.select_ship_label2 = QLabel(self)
            self.select_ship_label2.setText('select spacecraft: ')
            self.select_ship_label2.setStyleSheet("color: rgb(255, 237, 226);\n"
                                                  "font: 20pt \"Bahnschrift SemiLight\";")
            self.gridLayout_2.addWidget(self.select_ship_label2, 5, 0, 1, 1)

            self.spacecraft2_preview = QLabel(self)
            self.spacecraft2_preview.setStyleSheet("border-color: rgb(255, 228, 206);\n"
                                                   "border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
                                                   "stop:0 rgba(0, 0, 0, 255), "
                                                   "stop:1 rgba(255, 255, 255, 255));")
            self.spacecraft2_preview.setAlignment(QtCore.Qt.AlignCenter)
            self.gridLayout_2.addWidget(self.spacecraft2_preview, 6, 1, 1, 1)

        self._button_start = QtWidgets.QPushButton(self)
        self._button_start.setText('-> start')
        self._button_start.setGeometry(QtCore.QRect(480, 420, 141, 51))
        self._button_start.setStyleSheet("border:2px solid beige; color: beige;font-size: 26px;")
        self._button_start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self._button_start.clicked.connect(self.on_start_button_clicked)

    def on_start_button_clicked(self):
        if self.num_of_players == 1:
            if self.nickname_input.text() == "" or self.nickname_input.text() == " ":
                msg = QMessageBox()
                msg.setText("please enter your nickname...")
                msg.setWindowTitle('Error')
                msg.exec_()
            else:
                player_id = self.nickname_input.text()
                player_spacecraft = self.selected_spacecraft.currentText()
                self.hide()
                __start_game_process__(player_id, player_spacecraft)
                self.nickname_input.setText('')
        elif self.num_of_players == 2:
            if self.nickname_input.text() == "" or self.nickname_input.text() == " " \
                    or self.nickname_input2.text() == "" or self.nickname_input2.text() == " ":
                msg = QMessageBox()
                msg.setText("please enter your nicknames...")
                msg.setWindowTitle('Error')
                msg.exec_()
            elif self.nickname_input.text() == self.nickname_input2.text():
                msg = QMessageBox()
                msg.setText("nicknames must be unique...")
                msg.setWindowTitle('Error')
                msg.exec_()
            else:
                player1_id = self.nickname_input.text()
                player1_spacecraft = self.selected_spacecraft.currentText()
                player2_id = self.nickname_input2.text()
                player2_spacecraft = self.selected_spacecraft2.currentText()
                self.hide()
                __start_mp_game_process__(player1_id, player1_spacecraft, player2_id, player2_spacecraft)
                self.nickname_input.setText('')
                self.nickname_input2.setText('')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SelectWindow()
    sys.exit(app.exec_())
