"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets, QtCore


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

        self.dial.valueChanged.connect(self.slider.setValue)
        self.slider.valueChanged.connect(self.dial.setValue)
        self.dial.valueChanged.connect(self.lcdNumber.display)

        self.comboBox.currentIndexChanged.connect(self.update_lcd_number_format)
        self.dial.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.dial.keyPressEvent = self.keyPressEvent

        self.load_settings()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.dial = QtWidgets.QDial(self)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.lcdNumber = QtWidgets.QLCDNumber(self)
        self.comboBox = QtWidgets.QComboBox(self)

        self.comboBox.addItems(["Bin", "Oct", "Hex", "Dec"])

        layout.addWidget(self.dial)
        layout.addWidget(self.slider)
        layout.addWidget(self.lcdNumber)
        layout.addWidget(self.comboBox)

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Plus:
            self.dial.setValue(self.dial.value() + 1)
        elif key == QtCore.Qt.Key_Minus:
            self.dial.setValue(self.dial.value() - 1)
        print(f"New Dial Value: {self.dial.value()}")

    def update_lcd_number_format(self, index):
        format_options = [bin, oct, hex, int]
        value = self.lcdNumber.value()
        conversion_func = format_options[index]
        self.lcdNumber.display(conversion_func(value))

    def save_settings(self):
        settings = QtCore.QSettings("MyCompany", "MyApp")
        settings.setValue("DisplayMode", self.comboBox.currentIndex())
        settings.setValue("LCDValue", self.lcdNumber.value())

    def load_settings(self):
        settings = QtCore.QSettings("MyCompany", "MyApp")
        display_mode = settings.value("DisplayMode", 0, int)
        self.comboBox.setCurrentIndex(display_mode)
        lcd_value = settings.value("LCDValue", 0, int)
        self.lcdNumber.display(lcd_value)

    def closeEvent(self, event):
        self.save_settings()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
