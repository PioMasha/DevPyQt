"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""

from PySide6 import QtWidgets, QtCore
from a_threads import SystemInfo


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.system_info_thread = SystemInfo()

        self.delay_input = QtWidgets.QLineEdit()
        self.cpu_info_display = QtWidgets.QLabel()
        self.ram_info_display = QtWidgets.QLabel()

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("Задержка:"))
        layout.addWidget(self.delay_input)
        layout.addWidget(QtWidgets.QLabel("Информация о CPU:"))
        layout.addWidget(self.cpu_info_display)
        layout.addWidget(QtWidgets.QLabel("Информация о RAM:"))
        layout.addWidget(self.ram_info_display)

        self.delay_input.textChanged.connect(self.update_delay)
        self.system_info_thread.systemInfoReceived.connect(self.update_info)

        # Запускаем поток
        self.system_info_thread.start()

    def update_delay(self, text):
        try:
            delay = float(text)
            self.system_info_thread.delay = delay
        except ValueError:
            pass

    def update_info(self, info):
        cpu_value, ram_value = info
        self.cpu_info_display.setText(f"CPU: {cpu_value}%")
        self.ram_info_display.setText(f"RAM: {ram_value}%")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyWidget()
    window.show()
    app.exec()

