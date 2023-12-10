"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""


from PySide6 import QtWidgets, QtCore
from generated_ui import Ui_Form


class Window(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.screen = QtWidgets.QApplication.primaryScreen()
        self.setGeometry(100, 100, 640, 480)

        self.init_ui()

    def init_ui(self):
        self.move(100, 100)
        self.setWindowTitle("Состояние окна")

        self.plainTextEdit = QtWidgets.QPlainTextEdit(self)
        self.plainTextEdit.setReadOnly(True)

    def moveEvent(self, event):
        old_pos = event.oldPos()
        new_pos = event.pos()
        self.plainTextEdit.appendPlainText(f"Позиция окна: {new_pos.x()}, {new_pos.y()}")
        event.accept()

    def resizeEvent(self, event):
        new_size = event.size()
        self.plainTextEdit.appendPlainText(f"Размер окна: {new_size.width()}, {new_size.height()}")
        event.accept()

    def showEvent(self, event):
        screen_count = len(QtWidgets.QApplication.screens())
        screen_geometry = self.screen.geometry()
        window_geometry = self.geometry()

        self.plainTextEdit.appendPlainText(f"Кол-во экранов: {screen_count}")
        self.plainTextEdit.appendPlainText(
            f"Разрешение экрана: {screen_geometry.width()} x {screen_geometry.height()}")
        self.plainTextEdit.appendPlainText(f"Размер окна: {window_geometry.width()} x {window_geometry.height()}")

        event.accept()

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            state = self.windowState()
            if state & QtCore.Qt.WindowMinimized:
                self.plainTextEdit.appendPlainText("Окно свернуто")
            elif state & QtCore.Qt.WindowMaximized:
                self.plainTextEdit.appendPlainText("Окно развернуто")
            elif state & QtCore.Qt.WindowActive:
                self.plainTextEdit.appendPlainText("Окно активно")
            elif state & QtCore.Qt.WindowFullScreen:
                self.plainTextEdit.appendPlainText("Окно находится в полноэкранном режиме")
            else:
                self.plainTextEdit.appendPlainText("Окно отображено")


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
