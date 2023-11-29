import json
import requests
from geopy.geocoders import Nominatim

API_URL = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}" \
          "&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}"

class WeatherForecast:

    def __init__(self, city):
        self.city = city
        self.data = self.load_data()

    def load_data(self):
        try:
            with open('weather_results.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def find_cords(self):
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(self.city)
        return location.latitude, location.longitude

    def retrieve_data(self, latitude, longitude, date):
        response = requests.get(API_URL.format(latitude=latitude, longitude=longitude, searched_date=date))
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def check_rain(self, data):
        try:
            rain_sum = data['daily']['rain_sum'][0]
            if rain_sum > 0.0:
                return "Bedzie padac"
            elif rain_sum == 0.0:
                return "Nie bedzie padac"
            else:
                return "Nie wiem"
        except (IndexError, KeyError):
            return "Nie wiem"

    def save_to_file(self):
        with open('weather_results.json', 'w') as file:
            json.dump(self.data, file)

    def __setitem__(self, date, result):
        self.data[date] = result
        self.save_to_file()

    def __getitem__(self, date):
        if date not in self.data:
            latitude, longitude = self.find_cords()
            api_data = self.retrieve_data(latitude, longitude, date)
            if api_data:
                self.data[date] = self.check_rain(api_data)
                self.save_to_file()
            else:
                self.data[date] = "Nie można uzyskać danych"
        return self.data[date]

    def __iter__(self):
        return iter(self.data)

    def items(self):
        for date, weather in self.data.items():
            yield date, weather