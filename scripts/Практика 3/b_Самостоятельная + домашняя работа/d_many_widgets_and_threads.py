"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""
from PySide6 import QtWidgets
from a_threads import SystemInfo, WeatherHandler
from b_systeminfo_widget import MyWidget as SystemInfoWidget
from c_weatherapi_widget import WindowWeather as WeatherWidget


class CombinedWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.system_info_thread = SystemInfo()
        self.weather_handler = None

        self.system_info_widget = SystemInfoWidget()
        self.weather_widget = WeatherWidget()

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.system_info_widget)
        layout.addWidget(self.weather_widget)

        self.system_info_thread.systemInfoReceived.connect(self.system_info_widget.update_info)

        self.weather_widget.ui_s.pushButtonGetData.clicked.connect(self.start_weather_thread)
        self.weather_widget.ui_s.pushButtonStopGetData.clicked.connect(self.stop_weather_thread)

    def start_weather_thread(self):
        if not self.weather_handler:
            lat = float(self.weather_widget.ui_s.lineEditLatitude.text())
            lon = float(self.weather_widget.ui_s.lineEditLongitude.text())
            self.weather_handler = WeatherHandler(lat, lon)
            self.weather_handler.weatherInfoReceived.connect(self.weather_widget.upgradeWeatherInfo)
            self.weather_handler.start()
            self.weather_widget.ui_s.textEditData.clear()
            self.weather_widget.ui_s.pushButtonGetData.setEnabled(False)
            self.weather_widget.ui_s.pushButtonStopGetData.setEnabled(True)

    def stop_weather_thread(self):
        if self.weather_handler:
            self.weather_handler.setStatus(None)
            self.weather_widget.ui_s.pushButtonStopGetData.setEnabled(False)
            self.weather_widget.ui_s.pushButtonGetData.setEnabled(True)
            self.weather_handler = None


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = CombinedWindow()
    window.show()

    app.exec()
