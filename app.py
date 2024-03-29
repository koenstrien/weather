import streamlit as st
from datetime import datetime

import requests

from locations import LOCATIONS


def get_current_weather(latitude: float, longitude: float) -> tuple[float, int]:
    curl = f"https://api.open-meteo.com/v1/forecast?latitude={latitude:.2f}&longitude={longitude:.2f}&hourly=temperature_2m,weathercode&timeformat=unixtime&forecast_days=1"
    response = requests.get(curl)

    hourly_data = response.json()["hourly"]
    time_stamps = hourly_data["time"]
    now = datetime.now()
    dtime_stamps = [abs(datetime.fromtimestamp(time_stamp) - now) for time_stamp in time_stamps]
    now_idx = dtime_stamps.index(min(dtime_stamps))
    temperature = hourly_data["temperature_2m"][now_idx]
    weather_code = hourly_data["weathercode"][now_idx]
    return temperature, weather_code


def get_weather_code_description(code: int) -> str:
    weather_code_description = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Slight or moderate thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }
    return weather_code_description[code]


def get_weather_code_icon(code: int) -> str:
    weather_code_icon = {
        0: ":sun_with_face:",
        1: ":mostly_sunny:",
        2: ":barely_sunny:",
        3: ":barely_sunny:",
        45: ":fog:",
        48: ":fog:",
        51: ":rain_cloud:",
        53: ":rain_cloud:",
        55: ":rain_cloud:",
        56: ":snow_cloud:",
        57: ":snow_cloud:",
        61: ":rain_cloud:",
        63: ":rain_cloud:",
        65: ":rain_cloud:",
        66: ":snow_cloud:",
        67: ":snow_cloud:",
        71: ":snow_cloud:",
        73: ":snow_cloud:",
        75: ":snow_cloud:",
        77: ":snow_cloud:",
        80: ":rain_cloud:",
        81: ":rain_cloud:",
        82: ":rain_cloud:",
        85: ":snow_cloud:",
        86: ":snow_cloud:",
        95: ":lightning:",
        96: ":lightning:",
        99: ":lightning:",
    }
    return weather_code_icon[code]


def display_weather(latitude: float, longitude: float, title=None):
    (temperature, weather_code) = get_current_weather(latitude, longitude)
    description = get_weather_code_description(weather_code)
    icon = get_weather_code_icon(weather_code)
    st.header(title)
    st.subheader(f"{temperature}°C {icon} - {description}")

st.set_page_config(layout="wide")
for name, (latitude, longitude) in LOCATIONS.items():
    display_weather(latitude, longitude, title=name) 
