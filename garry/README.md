
# Garry — Personal AI Assistant (Weather, Events & User Profiling)

Prototype of intelligent ML assistant powered by LangChain, RAG, OpenAI models, and multi-source APIs. Built with Python and Tkinter.

---

## About This Project

**Garry** is a personal AI assistant that plans activities according to 
local weather, public events and user hobbies/personal info.

He has an integrated conversational model that retrieves user details through friendly and natural conversation while avoiding the collection of overly sensitive information.

The project includes a GUI built with Tkinter, a RAG pipeline using Chroma, and multiple modules for user management, embeddings, weather, event retrieval, and notes extraction.

---

## Features

### AI Conversation Engine
- Built using LangChain, ChatOpenAI, and RunnableWithMessageHistory  
- Has conversational memory and can retain information between sessions  

### Real-time Weather Integration
Uses OpenWeatherAPI to retrieve:  
- today’s temperature  
- sky conditions  
- wind speed  
- rain/snow intensity  
- UV index  

### Event Discovery system
Currently retrieves events from:  
- PredictHQ API  
- Google Custom Search (Facebook events)

Additional notes:  
- Filters events by distance, free events, and relevance  
- Filtering is not fully integrated yet, so some old events may slip through  

### Automated Note-Taking (Profile Builder)

A separate sub-agent (“Little Garry”) gathers user info through natural conversation:  
- hobbies, occupation, personality traits, schedule, goals, and more  
- works but still needs polishing, as it tends to narrow its focus  
- saved details are stored safely and structured in JSON  

### RAG Pipeline for Events
- Event documents are stored in user-specific files, then split  
- Embedded with text-embedding-3-small  
- Persisted and stored in ChromaDB  

### Tkinter GUI
- The main interface is simple Tkinter  
- The note-taking UI is more advanced and uses a grid-based layout instead of fixed positioning  

### Additional Modules

FileManager – Module that works with JSON.

Path_manager – Module dedicated to centralizing paths in one place.

logging_module – Module dedicated to handling logging.

dependencychecker – Module that assists in installing the prototype by checking for and installing missing dependencies.

---

## Project Architecture

```
/garry
│── Garry_GUI.py
│── GarryGUIcore.py
│── /modules
    │── /Userdata
    │     │── /embedings
    │     │     └── Gerry{ID}eventsEMB
    │     │── /uidata
    │     │     └── lastcred.json
    │     └── Gerry{ID}events.txt
    │     └── ...
    │── Garry_LocWeather_module
    │── Garry_Events_module
    │── G_Notebot
    │── FileManager
    │── Path_manager
    │── logging_module
    │── LitteGarryUI
    │── dependencychecker

```

---

## Tech Stack

- Python 3.10+  
- LangChain  
- OpenAI API  
- ChromaDB  
- Tkinter  
- PredictHQ API  
- Google Custom Search  
- OpenWeather OneCall API  
- Geopy + TimezoneFinder  

---

**Loading user data:**

<img width="856" height="513" alt="User_load_example" src="https://github.com/user-attachments/assets/32da1af8-1a2e-4500-bae8-01fd243a9f4c" />

**NoteBot: conversationally gathering user information**

<img width="935" height="660" alt="notebot_example" src="https://github.com/user-attachments/assets/e78f9c8d-484c-41a8-a87e-83c932fcfa8d" />

**Activity recommendation relevant to user's interests**

<img width="867" height="500" alt="completion_example" src="https://github.com/user-attachments/assets/21d51571-596c-4417-b1b9-313849d9ad09" />

**Event suggestion based on hobby and local data**

<img width="861" height="513" alt="completion_event_example" src="https://github.com/user-attachments/assets/b9079496-c1a6-4938-973e-ce18646b650b" />

