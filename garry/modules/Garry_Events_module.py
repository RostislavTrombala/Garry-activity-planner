#!/usr/bin/env python
# coding: utf-8

# In[17]:


#RAG libraries
from pathlib import Path
from pypdf import PdfReader
from operator import itemgetter
#weather libraries
from geopy.geocoders import Nominatim
from geopy.location import Location
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo
import requests
#clasic libraries
import os, re
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime, timedelta
#program functions
from modules.Garry_LocWeather_module import get_weather, get_location
#both expect variable city and will returen current weather = get_weather 
#and coordinates.latitude & coordinates.longitude + timezone within two variables = get_location
from modules.Path_manager import PATH
from modules.logging_module import LOG


# api key
load_dotenv()
PREApK = os.getenv("predicthq_API_KEY")
GOOGApK = os.getenv("GOOGLE_API_KEY")
GOOGSE= "e526a0dd9052f4fee"

class EventFinder:
    def __init__(self, ID, city):
        self.ID = ID
        self.city = city
        self.timezone = None
    
    
    def DATEAdd(self, plusdays: float) -> tuple[str, str]:
        _, self.timezone = get_location (self.city)
        exact = (datetime.now(ZoneInfo(self.timezone))) + timedelta(days=plusdays)
        day = exact.date()

        
        return exact.strftime("%Y-%m-%dT%H:%M:%S"), day.strftime("%Y-%m-%d")
        
    #Public event retrieval
    def get_event(self) -> str:
        try:
            _, today = self.DATEAdd(0)  
            _, week = self.DATEAdd(7) 
            coordinates, _ = get_location(self.city)
            EventsPH = requests.get( #PH predicthh
            url="https://api.predicthq.com/v1/events/",
            headers={
              "Authorization": f"Bearer {PREApK}",
              "Accept": "application/json"
            },
            params={
                "within": f"20km@{coordinates.latitude},{coordinates.longitude}",
                "start.gte": today,
                "start.lte": week,
                "price.free": True,
                "limit": 50,
                "sort": "start"
            }
            )
        except Exception:
            LOG.error_log.exception(f"EventFinder API call failed for city '{self.city}'")
            # fallback for failure
            return []
        try:
            data = EventsPH.json()
        except Exception:
            LOG.dataWarn_log.exception("Failed to decode events JSON")
            return "No events available"

        try:
            events = data.get("results", [])
        except Exception:
            LOG.dataWarn_log.exception("JSON structure in event module failed (no 'results' key)")
            events = []
            
        if not events:
            for item in data.get("items", []):
                    Esummary = (f"[EVENT SUMMARY]\n\nNo upcoming public events found near {self.city} in the selected time range.")
                    try:
                        with open(PATH.Userdata_file.events(self.ID), "w", encoding="utf-8") as f:
                            f.write(Esummary)     
                            return (Esummary)
                    except Exception:
                        LOG.error_log.exception(f"Failed to write event summary for ID={self.ID}")
                        return (Esummary)
                        
        Esummary = f"[EVENT SUMMARY]\n\n"
        Esummary += f"Location: {self.city}\n"
        Esummary += f"Upcoming events found: {len(events)}\n\n"
        Esummary += "== Next 7 Days ==\n"
    
        try:
            for e in events[:30]:  # show top 30 events
                title = e.get("title", "Unnamed event")
                category = e.get("category", "Unknown category").capitalize()
                start = e.get("start_local", e.get("start", "Unknown time"))
                end = e.get("end_local", e.get("end", "Unknown time"))
                address = (
                    e.get("geo", {})
                    .get("address", {})
                    .get("formatted_address", "Location unknown")
                )
                attendance = e.get("phq_attendance", None)
        
                Esummary += f"{title}\n"
                Esummary += f"{start} → {end}\n"
                Esummary += f"{category}\n"
                Esummary += f"{address}\n"
                if attendance:
                    Esummary += f"Estimated attendance: {attendance}\n"
                Esummary += "--**--**--**--\n"
                
        except Exception:
            LOG.dataWarn_log.exception("Error while formatting events block")
            Esummary += "Error in loading some events.\n--**--**--**--\n"
    
        try:
            query = f"site:facebook.com/events {self.city}"
            url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGApK}&cx={GOOGSE}&dateRestrict=m4"
            
            response = requests.get(url)
            data = response.json()
        
            
            for item in data.get("items", []):
                    Esummary += (
                        f"Title: {item['title']}\n"
                        f"URL: {item['link']}\n"
                        f"Snippet: {item['snippet']}\n"
                        "--**--**--**--\n"
                    )

        except Exception:
            LOG.dataWarn_log.exception("Google search failed")
            Esummary += "Google event search unavailable.\n--**--**--**--\n"
        try:
            
            with open(PATH.Userdata_file.events(self.ID), "w", encoding="utf-8") as f:
                    f.write(Esummary) 
        except Exception:
            LOG.error_log.exception(f"Failed to write events file for user {self.ID}")
            
        return (Esummary)