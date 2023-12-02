import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        res = sqlite3.connect("coffee.sqlite").cursor().execute("""SELECT * FROM coffee""").fetchall()
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ['id', 'название', 'обжарка', 'молотое/зерна', 'вкус', 'цена в Р.', 'объём в МЛ'])
        for i, row in enumerate(res):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
