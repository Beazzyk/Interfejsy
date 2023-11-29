from weather_forecast import WeatherForecast

def run_program(weather_forecast: WeatherForecast):
    while True:
        date = input("Podaj datę (YYYY-MM-DD) lub 'exit', aby zakończyć: ")
        if date.lower() == 'exit':
            break

        weather = weather_forecast[date]

        print(f"Pogoda dla {city}: {date}: {weather}")

if __name__ == "__main__":
    city = input("Podaj nazwę miasta: ")
    weather_forecast = WeatherForecast(city)
    run_program(weather_forecast)