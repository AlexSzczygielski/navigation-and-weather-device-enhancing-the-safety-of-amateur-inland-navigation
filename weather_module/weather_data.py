#weather_module.py
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty



class WeatherData(QObject):
    def __init__(self):
        super().__init__()
        # weather_worker
        self._current_temp = float('nan')
        self._current_feels_like = float('nan')
        self._current_humidity = float('nan')
        self._current_condition = ""
        self._current_wind = float('nan')
        
        self._forecast = []  # list of dicts, each dict is a 3-hour forecast entry

        # location / city metadata
        self._message = ""
        self._city_name = ""
        self._country = ""
        self._lat = float('nan')
        self._lon = float('nan')
        self._timezone = -1

        self._fetch_timestamp = None

    # --- Update signals ---
    # weather_worker
    currentTempChanged = pyqtSignal(float)
    currentFeelsLikeChanged = pyqtSignal(float)
    currentHumidityChanged = pyqtSignal(int)
    currentConditionChanged = pyqtSignal(str)
    currentWindChanged = pyqtSignal(float)
    
    forecastChanged = pyqtSignal(list)

    # location metadata
    messageChanged = pyqtSignal(str)
    cityNameChanged = pyqtSignal(str)
    countryChanged = pyqtSignal(str)
    latChanged = pyqtSignal(float)
    lonChanged = pyqtSignal(float)
    timezoneChanged = pyqtSignal(int)

    fetchTimestampChanged = pyqtSignal(str)

    # --- Properties ---
    # weather_worker
    @pyqtProperty(float, notify=currentTempChanged)
    def current_temp(self):
        return self._current_temp

    @current_temp.setter
    def current_temp(self, value):
        if self._current_temp != value:
            self._current_temp = value
            self.currentTempChanged.emit(self._current_temp)

    @pyqtProperty(float, notify=currentFeelsLikeChanged)
    def current_feels_like(self):
        return self._current_feels_like

    @current_feels_like.setter
    def current_feels_like(self, value):
        if self._current_feels_like != value:
            self._current_feels_like = value
            self.currentFeelsLikeChanged.emit(self._current_feels_like)

    @pyqtProperty(int, notify=currentHumidityChanged)
    def current_humidity(self):
        return self._current_humidity

    @current_humidity.setter
    def current_humidity(self, value):
        if self._current_humidity != value:
            self._current_humidity = value
            self.currentHumidityChanged.emit(self._current_humidity)

    @pyqtProperty(str, notify=currentConditionChanged)
    def current_condition(self):
        return self._current_condition

    @current_condition.setter
    def current_condition(self, value):
        if self._current_condition != value:
            self._current_condition = value
            self.currentConditionChanged.emit(self._current_condition)

    @pyqtProperty(float, notify=currentWindChanged)
    def current_wind(self):
        return self._current_wind

    @current_wind.setter
    def current_wind(self, value):
        if self._current_wind != value:
            self._current_wind = value
            self.currentWindChanged.emit(self._current_wind)

    @pyqtProperty(list, notify=forecastChanged)
    def forecast(self):
        return self._forecast

    @forecast.setter
    def forecast(self, value):
        if self._forecast != value:
            self._forecast = value
            self.forecastChanged.emit(self._forecast)

    # location metadata
    @pyqtProperty(str, notify=messageChanged)
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        if self._message != value:
            self._message = value
            self.messageChanged.emit(self._message)

    @pyqtProperty(str, notify=cityNameChanged)
    def city_name(self):
        return self._city_name

    @city_name.setter
    def city_name(self, value):
        if self._city_name != value:
            self._city_name = value
            self.cityNameChanged.emit(self._city_name)

    @pyqtProperty(str, notify=countryChanged)
    def country(self):
        return self._country

    @country.setter
    def country(self, value):
        if self._country != value:
            self._country = value
            self.countryChanged.emit(self._country)

    @pyqtProperty(float, notify=latChanged)
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, value):
        if self._lat != value:
            self._lat = value
            self.latChanged.emit(self._lat)

    @pyqtProperty(float, notify=lonChanged)
    def lon(self):
        return self._lon

    @lon.setter
    def lon(self, value):
        if self._lon != value:
            self._lon = value
            self.lonChanged.emit(self._lon)

    @pyqtProperty(int, notify=timezoneChanged)
    def timezone(self):
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        if self._timezone != value:
            self._timezone = value
            self.timezoneChanged.emit(self._timezone)
    
    @pyqtProperty(str, notify=fetchTimestampChanged)
    def fetch_timestamp(self):
        return self._fetch_timestamp

    @fetch_timestamp.setter
    def fetch_timestamp(self, value):
        if self._fetch_timestamp != value:
            self._fetch_timestamp = value
            self.fetchTimestampChanged.emit(self._fetch_timestamp)