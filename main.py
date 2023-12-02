import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.show_table()
        self.edit_genre.clicked.connect(self.edit_coffee)
        self.add_genre.clicked.connect(self.add_coffee)

    def show_table(self):
        res = self.connection.cursor().execute("""SELECT * FROM coffee""").fetchall()
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ['id', 'название', 'обжарка', 'молотое/зерна', 'вкус', 'цена в Р.', 'объём в МЛ'])
        for i, row in enumerate(res):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

    def edit_coffee(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        if rows:
            self.edit_genre_widget = AddOrEdit(self.connection, 1, parent=self)
            self.edit_genre_widget.show()

    def add_coffee(self):
        self.add_genre_widget = AddOrEdit(self.connection, 0, parent=self)
        self.add_genre_widget.show()


class AddOrEdit(QMainWindow):
    def __init__(self, connection, n, parent=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.tableWidget = parent.tableWidget
        self.connection = connection
        self.queue = -1
        self.type = n
        if n == 1:
            rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
            ids1 = [
                [self.tableWidget.item(i, 0).text(), self.tableWidget.item(i, 1).text(),
                 self.tableWidget.item(i, 2).text(),
                 self.tableWidget.item(i, 3).text(), self.tableWidget.item(i, 4).text(),
                 self.tableWidget.item(i, 5).text(), self.tableWidget.item(i, 6).text()] for i in rows]
            self.queue = int(ids1[0][0])
            self.name.setPlainText(ids1[0][1])
            self.amount_of_roasting.setPlainText(ids1[0][2])
            self.amount_of_ml.setPlainText(ids1[0][6])
            self.value.setPlainText(ids1[0][5])
            self.taste.setPlainText(ids1[0][4])
            self.way.setPlainText(ids1[0][3])
        self.confirmation.clicked.connect(self.change_or_edit)

    def change_or_edit(self):
        if self.queue == -1:
            queue = tuple(self.connection.cursor().execute("""SELECT id FROM coffee"""))[-1][0] + 1
        else:
            queue = self.queue
        if self.type == 1:
            self.connection.cursor().execute(
                f"""UPDATE coffee SET name_of_sort='{self.name.toPlainText()}', 
                amount_of_roasting='{self.amount_of_roasting.toPlainText()}', a_wy_of_coffee='{self.way.toPlainText()}',
                value='{self.value.toPlainText()}', packaging_volume='{self.amount_of_ml.toPlainText()}', 
                taste='{self.taste.toPlainText()}' WHERE id={queue}""")
        else:
            self.connection.cursor().execute(
                f"""INSERT INTO 
                coffee(id, name_of_sort, amount_of_roasting, a_wy_of_coffee, taste, value, packaging_volume) VALUES 
                {queue, self.name.toPlainText(), self.amount_of_roasting.toPlainText(), self.way.toPlainText(),
                self.taste.toPlainText(), self.value.toPlainText(), self.amount_of_ml.toPlainText()}""")
        self.connection.commit()
        self.close()
        self.parent().show_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
