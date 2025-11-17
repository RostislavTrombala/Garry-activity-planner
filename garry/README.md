
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

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/garry
cd garry
```

### 2. Install dependencies
There is no need to manually install dependencies. Program will automatically 
check for missing dependencies and ask you if you want them installed.
```

### 3. Create .env file
```
OPENAI_API_KEY=your_key
OPENWEATHER_API_KEY=your_key
predicthq_API_KEY=your_key
GOOGLE_API_KEY=your_key
```

### 4. Run the app
```bash
python Garry_GUI.py or double-click Garry_GUI.py
```

