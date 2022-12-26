class Day:
    def __init__(self, day_name):
        self.day_name = day_name
        self.degrees = []
        self.wind = []
        self.pressure = []
        self.humidity = []

    def add_degrees(self, degree_value):
        self.degrees.append(degree_value)

    def add_wind(self, wind_value):
        self.wind.append(wind_value)

    def add_pressure(self, pressure_value):
        self.pressure.append(pressure_value)

    def add_humidity(self, humidity_value):
        self.humidity.append(humidity_value)
