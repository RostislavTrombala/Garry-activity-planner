#weather libraries
from geopy.geocoders import Nominatim
from geopy.location import Location
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo
import requests
#clasic libraries
import os
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta
from modules.logging_module import LOG

load_dotenv()
OWApK = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city: str) -> str:
    if "coordinates" not in globals(): 
        global coordinates, timezone
        try:
            coordinates,_ = get_location(city)
        except Exception:
            LOG.dataWarn_log.exception("faieled to execute get_locaion in weather module")
             
    if coordinates is None:
        dataWarn_log.error("Location not found") 
        return ("You don't have access to weather")
    else:
        OWeather_url= f"https://api.openweathermap.org/data/3.0/onecall?lat={coordinates.latitude}&lon={coordinates.longitude}&appid={OWApK}"
        Weatherdata = requests.get(OWeather_url)
        if Weatherdata.status_code == 200:
             Wdata = Weatherdata.json()
             WtodaySum = Wtoday(Wdata)
             return WtodaySum
        else:
            LOG.dataWarn_log.error(f"Failed to get data: {response.status_code}. error in data retrieval") 
            return ("You don't have access to weather")

def get_location(city: str) -> Location | None:
    try:
        if "coordinates" not in globals():
            global coordinates, timezone
            coordinates = None
        if coordinates != None:
            return coordinates, timezone
        else:
            geolocator = Nominatim(user_agent="gerry_the_app", timeout=7)
            coordinates = geolocator.geocode(city)
            timezone = TimezoneFinder().timezone_at(lat=coordinates.latitude, lng=coordinates.longitude)
            return coordinates, timezone
    except Exception:
        LOG.error_log.exception(f"get_location ERROR — city={city}")
        return None, None

#function that will return summary of todays weather        
def Wtoday(Weatherdata: dict) -> str:
    try:
        current = Weatherdata["current"]
    except Exception:
        LOG.dataWarn_log.exception("Weather data missing 'current' section")
        return "Weather data unavailable."

    try:
        Wsummary = f"[WEATHER SUMMARY]\n\n"
        Wsummary += f"Location: {Weatherdata.get('timezone', 'Unknown')}\n"
        Wsummary += f"Timezone Offset: {Weatherdata.get('timezone_offset', 0)}s\n\n"
        
        Wsummary += "== Today ==\n"
        Wsummary += f"Temp: {k_to_c(current['temp'])}°C (feels like {k_to_c(current['feels_like'])}°C)\n"
        Wsummary += f"Sky: {current['weather'][0]['description'].capitalize()} ({current['clouds']}% cloudiness)\n"
        Wsummary += f"UV Index: {current.get('uvi', 'N/A')}\n"
        Wsummary += f"Visibility: {round(current.get('visibility', 0) / 1000, 1)} km\n"
        Wsummary += f"Wind: {current['wind_speed']} m/s"
        if 'wind_gust' in current:
            Wsummary += f", gusts up to {current['wind_gust']} m/s\n"
        else:
            Wsummary += "\n"
        if 'rain' in current:
            Wsummary += f"Rain: {current['rain'].get('1h', 0)} mm/h\n"
        else:
            Wsummary += "Rain: None\n"
        if 'snow' in current:
            Wsummary += f"Snow: {current['snow'].get('1h', 0)} mm/h\n"
        else:
            Wsummary += "Snow: None\n"
        return(Wsummary)
        
    except Exception:
        LOG.error_log.exception("Wtoday formatting failed")
        return "Weather data unavailable."

def k_to_c(k): #Kelvin to celsius
    try:
        return round(k - 273.15, 1)
    except Exception:
        LOG.dataWarn_log.warning(f"k_to_c failed for value: {k}")
        return "Unknown"