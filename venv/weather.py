import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass


load_dotenv()

api_key=os.getenv('API_KEY')
@dataclass
class WeatherData:
    main : str
    desc: str
    icon: str
    temp: float
    feels:float

def getLatLon(city_name, state_code,country_code,API_key):
    resp=requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}').json()

    lat,lon = resp[0].get('lat'),resp[0].get('lon')

    return lat,lon


def getWeather(lat,lon,API_key):
    resp=requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric').json()
    # print(resp)
    data = WeatherData(
        main = resp.get('weather')[0].get('main'),
        desc=resp.get('weather')[0].get('description'),
        icon=resp.get('weather')[0].get('icon'),
        temp=resp.get('main').get('temp'),
        feels=resp.get('main').get('feels_like')
    )
    # print(data)
    return data

# getLatLon('peddapuram','AP','IN',api_key)

def main(city_name, state_name, country_code):
    # print(city_name, state_name, country_code)
    lat,lon=getLatLon(city_name, state_name, country_code,api_key)    
    # print(lat,lon)
    weather_data=getWeather(lat,lon,api_key)
    return weather_data


# main('Hammond','IN','US')
if __name__=="__main__":
    print('inside main')
    lat,lon=getLatLon('Hammond','IN','US',api_key)
    print(lat,lon)
    getWeather(lat,lon,api_key)
    
