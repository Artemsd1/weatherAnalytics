import re

from bs4 import BeautifulSoup
from flask import Flask, render_template, url_for
import requests
from requests import HTTPError

import Day


def parse_numeric(s: str) -> 'int or float':
    s = s.replace('−', '-').replace(',', '.')
    s = re.sub(r'[^\d.-]+', '', s)
    if '.' not in s:
        return int(s)
    else:
        return float(s)


def get_data() -> list[Day]:
    # --------------Gismeteo--------------
    url = "https://www.gismeteo.ru/weather-volgograd-5089/10-days/"

    headers = requests.utils.default_headers()

    headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
        }
    )

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except HTTPError as hp:
        print(hp)

    else:
        print("Gismeteo worked")

    soup = BeautifulSoup(response.text, "lxml")

    weather_tempr = soup.find("div", class_="widget-row-chart widget-row-chart-temperature-avg")
    tempr_degrees = weather_tempr.find_all("div", class_="value")

    weather_wind = soup.find("div", class_="widget-row widget-row-wind-speed")
    wind_speed = weather_wind.find_all("div", class_="row-item")

    weather_pressure = soup.find("div", class_="widget widget-pressure widget-days")
    pressure_max = weather_pressure.find_all("div", class_="value style_size_m")

    humidity = soup.find("div", class_="widget-row widget-row-humidity")
    humidity_arr = humidity.find_all("div", class_="row-item")

    # --------------Yandex--------------
    url_yandex = "https://yandex.ru/pogoda/details/10-day-weather?lat=48.707068&lon=44.516979&via=ms"

    response_yandex = requests.get(url_yandex, headers=headers)

    soup_yandex = BeautifulSoup(response_yandex.text, "lxml")

    print("--------Yandex----------")
    week_days = []
    days_yandex = soup_yandex.find_all("h2", class_="forecast-details__title")
    for i in days_yandex:
        week_days.append(i.find("span", class_="a11y-hidden").text)
    print(week_days)

    table_row_yandex = soup_yandex.find_all("tr", class_="weather-table__row")

    degrees_yandex_day = []
    degrees_yandex_night = []
    wind_yandex_night = []
    wind_yandex_day = []
    pressure_yandex_day = []
    pressure_yandex_night = []
    humidity_yandex_day = []
    humidity_yandex_night = []

    for i in table_row_yandex:
        day_part = i.find("div", class_="weather-table__daypart")
        if day_part.text == "днём":
            degrees_temp = i.find_all("div", class_="temp")
            degrees_yandex_day.append(
                parse_numeric(degrees_temp[0].find("span", class_="temp__value temp__value_with-unit").text))
            wind_yandex_day.append(i.find("span", class_="wind-speed").text)
            pressure_yandex_day.append(
                i.find("td", class_="weather-table__body-cell weather-table__body-cell_type_air-pressure").text)
            humidity_yandex_day.append(
                i.find("td", class_="weather-table__body-cell weather-table__body-cell_type_humidity").text.replace('%',
                                                                                                                    ''))
        if day_part.text == "ночью":
            degrees_temp = i.find_all("div", class_="temp")
            degrees_yandex_night.append(
                parse_numeric(degrees_temp[0].find("span", class_="temp__value temp__value_with-unit").text))
            wind_yandex_night.append(i.find("span", class_="wind-speed").text)
            pressure_yandex_night.append(
                i.find("td", class_="weather-table__body-cell weather-table__body-cell_type_air-pressure").text)
            humidity_yandex_night.append(
                i.find("td", class_="weather-table__body-cell weather-table__body-cell_type_humidity").text.replace('%',
                                                                                                                    ''))

    print(degrees_yandex_day)
    print(degrees_yandex_night)
    print(wind_yandex_day)
    print(wind_yandex_night)
    print(pressure_yandex_day)
    print(pressure_yandex_night)
    print(humidity_yandex_day)
    print(humidity_yandex_night)

    # --------------Mail--------------
    url_mail = "https://pogoda.mail.ru/prognoz/volgograd/14dney/"

    response_mail = requests.get(url_mail, headers=headers)

    soup_mail = BeautifulSoup(response_mail.text, "lxml")
    print("--------Mail----------")
    table_row_mail = soup_mail.find_all("div", class_="p-flex__column p-flex__column_percent-16")

    degrees_mail_day = []
    degrees_mail_night = []
    wind_mail_day = []
    wind_mail_night = []
    pressure_mail_day = []
    pressure_mail_night = []
    humidity_mail_day = []
    humidity_mail_night = []

    wind_temp = soup_mail.find_all("span", class_="link__text")
    for n in range(len(wind_temp)):
        if wind_temp[n].text.find("м/с") != -1 and n % 2 == 0:
            wind_mail_day.append(wind_temp[n].text[:2])

    for i in table_row_mail:
        day_part = i.find("span", class_="text text_block text_bold_normal text_fixed margin_bottom_10")
        if day_part.text == "день":
            degrees_mail_day.append(parse_numeric(
                i.find("span", class_="text text_block text_bold_medium margin_bottom_10").text.replace('°', '')))
            humidity_temp = i.find("span", class_="link link_block link_icon")
            humidity_mail_day.append(humidity_temp.find("span", class_="link__text").text[:2])
            pressure_temp = i.find("span", class_="link link_block link_icon margin_top_10")
            pressure_mail_day.append(pressure_temp.find("span", class_="link__text").text[:3])
        if day_part.text == "ночь":
            degrees_mail_night.append(parse_numeric(
                i.find("span", class_="text text_block text_bold_medium margin_bottom_10").text.replace('°', '')))
            humidity_temp = i.find("span", class_="link link_block link_icon")
            humidity_mail_night.append(humidity_temp.find("span", class_="link__text").text[:2])
            pressure_temp = i.find("span", class_="link link_block link_icon margin_top_10")
            pressure_mail_night.append(pressure_temp.find("span", class_="link__text").text[:3])

    print(degrees_mail_day)

    # --------------Создание Объектов--------------
    print("Объекты день:")

    date_weather = []
    for i in range(10):
        date = Day.Day(week_days[i])

        # Градусы
        date.add_degrees(degrees_yandex_day[i])
        date.add_degrees(degrees_yandex_night[i])
        date.add_degrees(degrees_mail_day[i])
        date.add_degrees(degrees_mail_night[i])
        date.add_degrees(parse_numeric(tempr_degrees[i].find("span", class_="unit unit_temperature_c").text))
        date.add_degrees(parse_numeric(tempr_degrees[i].find("span", class_="unit unit_temperature_c").text))

        # Ветер
        date.add_wind(wind_yandex_day[i])
        date.add_wind(wind_yandex_night[i])
        date.add_wind(wind_mail_day[i])
        date.add_wind(wind_mail_day[i])
        date.add_wind(wind_speed[i].find("span", class_="wind-unit unit unit_wind_m_s").text)
        date.add_wind(wind_speed[i].find("span", class_="wind-unit unit unit_wind_m_s").text)

        # Давление
        date.add_pressure(pressure_yandex_day[i])
        date.add_pressure(pressure_yandex_night[i])
        date.add_pressure(pressure_mail_day[i])
        date.add_pressure(pressure_mail_night[i])
        date.add_pressure(pressure_max[i].find("span", class_="unit unit_pressure_mm_hg_atm").text)
        date.add_pressure(pressure_max[i].find("span", class_="unit unit_pressure_mm_hg_atm").text)

        # Влажность
        date.add_humidity(humidity_yandex_day[i])
        date.add_humidity(humidity_yandex_night[i])
        date.add_humidity(humidity_mail_day[i])
        date.add_humidity(humidity_mail_night[i])
        date.add_humidity(humidity_arr[i].text)
        date.add_humidity(humidity_arr[i].text)

        date_weather.append(date)

    return date_weather

