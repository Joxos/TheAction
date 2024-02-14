import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import Slot
from the_action import main

ui_file_path = "main_window.ui"

Ui_MainWindow, QMainWindow = loadUiType(ui_file_path)


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.button_exit.clicked.connect(sys.exit)
        self.button_start_game.clicked.connect(self.start_game)

    @Slot()
    def start_game(self):
        self.hide()
        main()
        self.show()


app = QApplication(sys.argv)
main_window = MyMainWindow()
main_window.show()
sys.exit(app.exec())
