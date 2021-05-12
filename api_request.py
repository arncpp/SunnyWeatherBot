import requests

from Functions import buttons_in_weather, print_weather
from Globals import api_key, bot, Globals, url_openweather, url_forecast


def weather_now_api(message):
    """
    Отправляет сайту API запрос, получает json файл с погодай в данном городе
    либо стране на данный момент
    Выводит пользователю погоду
    :param message: сообщение пользователя
    :return: текст с погодой
    """
    keyboard = buttons_in_weather()
    city_name = message.text
    try:
        params = {Globals.api_id: api_key, Globals.city_name_api: city_name,
                  Globals.units_settings: Globals.units_measuring,
                  Globals.language: Globals.rus_language}
        result = requests.get(url_openweather, params=params)
        weather = result.json()
        print(weather)
        city = weather[Globals.city_name_for_search]
        city_temperature = float(
            weather[Globals.json_main][Globals.json_temperature])
        city_descr = weather[Globals.json_weather][0][
            Globals.json_weather_description]
        city_temp_feels = float(
            weather[Globals.json_main][Globals.json_temp_feels])
        city_pressure = weather[Globals.json_main][Globals.json_pressure]
        city_humidity = weather[Globals.json_main][Globals.json_humidity]
        city_wind = weather[Globals.json_wind][Globals.json_wind_speed]
        weather_text = bot.send_message(message.chat.id,
                                        print_weather(city, city_temperature,
                                                      city_temp_feels,
                                                      city_pressure,
                                                      city_humidity, city_wind,
                                                      city_descr),
                                        reply_markup=keyboard)

    except KeyError:
        weather_text = bot.send_message(message.chat.id,
                                        f"{Globals.city_not_found}: {city_name} :(",
                                        reply_markup=keyboard)
    return weather_text


def weather_5days_api(message):
    """
    Отправляет сайту API запрос, получает json файл с погодай в данном городе
    либо стране на 5 дней
    Выводит пользователю погоду
    :param message: сообщение пользователя
    :return: текст с погодой
    """
    city_name = message.text
    keyboard = buttons_in_weather()
    try:
        params = {Globals.api_id: api_key, Globals.city_name_api: city_name,
                  Globals.units_settings: Globals.units_measuring,
                  Globals.language: Globals.rus_language}
        result = requests.get(url_forecast, params=params)
        weather = result.json()
        for weather_list_element in weather[Globals.json_weather_list]:
            print(weather_list_element[Globals.json_dt_txt])
        city = weather[Globals.json_weather_city][Globals.city_name_for_search]
        text = ""
        for num, weather_list_element in enumerate(weather[Globals.json_weather_list]):
            if num % Globals.continue_num == 0:
                text += f"{weather_list_element[Globals.json_dt_txt][Globals.json_txt_crop_from:Globals.json_txt_crop_to]}" \
                        f"\t\t\t {weather_list_element[Globals.json_dt_txt][Globals.json_txt_crop_to:Globals.json_txt_crop_end]} " \
                        f"\t\t\t {float(weather_list_element[Globals.json_main][Globals.json_temperature])} ℃\n"
            if (num + 1) % Globals.space_num == 0:
                text += "\n"
        weather_text = bot.send_message(message.chat.id, f" {city}:\n{text}",
                                        reply_markup=keyboard)
    except KeyError:
        weather_text = bot.send_message(message.chat.id,
                                        f"Город {city_name} не найден :(",
                                        reply_markup=keyboard)
    return weather_text
