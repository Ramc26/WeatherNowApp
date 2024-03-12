import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
import datetime 
import pytz
from pytz import country_timezones

def get_local_timezone(country_code):
    timezones = country_timezones.get(country_code)
    if timezones:
        return timezones[0]  # Choose the first timezone for simplicity
    else:
        return None

def convert_unix_time_to_local(unix_time, country_code):
    timezone = get_local_timezone(country_code)
    if timezone:
        tz = pytz.timezone(timezone)
        date_time = datetime.datetime.fromtimestamp(unix_time, tz)
        local_time = date_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        return local_time
    else:
        return "Timezone not found for the given country code."
    
def MPS_MPH(meters_per_sec):
    miles_per_hour = meters_per_sec * 2.24
    return round(miles_per_hour, 1)


load_dotenv()

api_key = os.getenv('API_KEY')

@dataclass
class WeatherData:
    main: str
    desc: str
    icon: str
    temp: float
    humid:int
    feels: float
    rise: str
    set: str
    wspeed:float
    wdir:int

def getLatLon(city_name, state_code, country_code, API_key):
    resp = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}').json()
    lat, lon = resp[0].get('lat'), resp[0].get('lon')
    return lat, lon

def getWeather(lat, lon, API_key, country_code):
    resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric').json()
    print(resp)
    data = WeatherData(
        main=resp.get('weather')[0].get('main').title(),
        desc=resp.get('weather')[0].get('description').title(),
        icon=resp.get('weather')[0].get('icon'),
        humid=resp.get( 'main').get('humidity'),
        temp=resp.get('main').get('temp'),
        feels=resp.get('main').get('feels_like'),
        wspeed=MPS_MPH(resp.get('wind').get('speed')),
        wdir=resp.get('wind').get('deg'),
        rise=convert_unix_time_to_local(resp.get('sys').get('sunrise'), country_code),
        set=convert_unix_time_to_local(resp.get('sys').get('sunset'), country_code)
    )
    return data

def main(city_name, state_name, country_code):
    lat, lon = getLatLon(city_name, state_name, country_code, api_key)
    weather_data = getWeather(lat, lon, api_key, country_code)
    return weather_data

if __name__ == "__main__":
    city_name = 'Nayakampalli'
    state_name = 'AP'
    country_code = 'IN'
    weather_data = main(city_name, state_name, country_code)
    print("Weather Data:")
    print(weather_data) 
