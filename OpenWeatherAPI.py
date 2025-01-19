"""
Задание 2. Работа с параметрами запроса
1. Используйте API OpenWeather для получения данных о погоде.
2. Напишите программу, которая:
 принимает название города от пользователя,
 отправляет GET-запрос к API и выводит текущую температуру и описание погоды.
"""
# https://openweathermap.org

import requests
from personal import OPEN_WEATHER_API_KEY as API_KEY


class BaseAPI:
    """
    Базовый класс формирования строки запроса
    """
    _BASE_URL_PART = "http://api.openweathermap.org/"
    _SERVICE_URL_PART = ""

    def __init__(self, api_key: str):
        """
        Конструктор инициализации
        :param api_key: ключ авторизации
        """
        self._api_key = api_key

    @property
    def main_url(self) -> str:
        """
        базовая строка запроса
        """
        return self._BASE_URL_PART + self._SERVICE_URL_PART + f'appid={self._api_key}'


class LocationAPI(BaseAPI):
    """
    Класс формирования строки запроса для получения координат локации
    https://openweathermap.org/api/geocoding-api#direct_name_fields
    'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit={limit}&appid={API_KEY}'
    """
    _SERVICE_URL_PART = 'geo/1.0/direct?'

    def __init__(self, api_key: str, city_name: str, state_code: str = "", country_code: str = "RU"):
        """
        Конструктор инициализации
        :param api_key: ключ авторизации
        :param city_name: наименование города
        :param state_code: код штата/области
        :param country_code: код страны (2 знака)
        """
        super().__init__(api_key)
        self.city_name: str = city_name
        self.state_code: str = state_code
        self.country_code: str = country_code.upper()

    @property
    def url(self) -> str:
        """
        строка запроса
        """
        limit = 1
        return self.main_url + f'&q={self.city_name},{self.state_code},{self.country_code}&limit={limit}'


class WeatherAPI(BaseAPI):
    """
    Класс формирования строки запроса для получения погоды
    https://openweathermap.org/current#format
    'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&mode={mode}&units={units}&lang={country_code.lower()}&appid={API_KEY}'
    """
    _SERVICE_URL_PART = 'data/2.5/weather?'

    def __init__(self, api_key: str, lat: str, lon: str, mode: str = "", units: str = "metric", lang: str = "ru"):
        """
        Конструктор инициализации
        :param api_key: ключ авторизации
        :param lat: широта
        :param lon: долгота
        :param mode: вывод в формате xml или html (json по умолчанию)
        :param units: единица измерения (standard, metric, imperial)
        :param lang: язык выводимой информации
        """
        super().__init__(api_key)
        self.lat: str = lat
        self.lon: str = lon
        self.mode: str = mode
        self.units: str = units
        self.lang: str = lang.lower()

    @property
    def url(self) -> str:
        """
        строка запроса
        """
        mode = f"&mode={self.mode}" if self.mode else ""
        return self.main_url + f'&lat={self.lat}&lon={self.lon}{mode}&units={self.units}&lang={self.lang}'


def get_location_coordinates(city_name: str, state_code: str = "", country_code: str = "RU") -> dict[str, str]:
    """
    Получить координаты города (ширина, долгота)
    :param city_name: наименование города
    :param state_code: код штата/области
    :param country_code: код страны (2 знака)
    :return: Координаты найденного места dict(lat=ширина, lon=долгота, city=город)
    """
    result = None
    try:
        location_api = LocationAPI(API_KEY, city_name, state_code, country_code)
        response = requests.get(location_api.url)
        response.raise_for_status()
        locations = response.json()
        if len(locations) > 0:
            loc = locations[0]
            result = dict(lat=loc["lat"],
                          lon=loc["lon"],
                          city=loc["local_names"][country_code.lower()])
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Ошибка запроса: {err}")
    return result


def show_current_weather(city_name: str, state_code: str = "", country_code: str = "RU") -> None:
    """
    Показать текущую температуру и описание погоды для выбранного города
    :param city_name: наименование города
    :param state_code: код штата/области
    :param country_code: код страны (2 знака)
    """
    location = get_location_coordinates(city_name, state_code, country_code)
    if not location:
        print(f"Геопозиция не определена")
        return

    try:
        lat = location["lat"]
        lon = location["lon"]
        weather_api = WeatherAPI(API_KEY, lat, lon, lang=country_code.lower())

        response = requests.get(weather_api.url)
        response.raise_for_status()
        current_weather = response.json()
        if not current_weather:
            print("Данные по погоде не найдены")

        city_name = current_weather["name"]
        temperature = current_weather["main"]["temp"]
        description = current_weather["weather"][0]["description"]
        print(f"{city_name}, {temperature}℃, {description}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Ошибка запроса: {err}")


# print(get_location_coordinates("Moscow"))
show_current_weather("Moscow")
