from pathlib import Path
from pypdf import PdfReader
from operator import itemgetter
#Langchain
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
#weather libraries
from geopy.geocoders import Nominatim
from geopy.location import Location
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo
import requests
#clasic libraries
import os, re
import json
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime, timedelta
#program functions
from modules.Garry_LocWeather_module import get_weather, get_location
#both expect variable city and will returen current weather = get_weather 
#and coordinates.latitude & coordinates.longitude + timezone within two variables = get_location
from modules.Garry_Events_module import EventFinder
from modules.Path_manager import PATH
from modules.logging_module import LOG

# api key
load_dotenv()
ApK = os.getenv("OPENAI_API_KEY")
PREApK = os.getenv("predicthq_API_KEY")
GOOGApK = os.getenv("GOOGLE_API_KEY")
GOOGSE= "e526a0dd9052f4fee"
#"https://cse.google.com/cse.js?cx=e526a0dd9052f4fee"


global splitter


splitter = CharacterTextSplitter(
    separator= "--**--**--**--",  # your exact delimiter
    chunk_size=600,               # large enough for one event + metadata
    chunk_overlap=0,
    is_separator_regex=False       # make sure it's literal, not regex
)
    
_store = {}
def get_history(session_id: str):
    """LangChain passes just the session_id string here."""
    if session_id not in _store:
        _store[session_id] = ChatMessageHistory()
    return _store[session_id]

def with_memory(chain):
    return RunnableWithMessageHistory(
        chain,
        get_history,                 # expects session_id: str
        history_messages_key="history",
    )
    
def convers (date: str, weather: str, events: str, name: str, hobby: str, location: str, language: str = "Čeština"):
    LOG.data_log.info(weather)    
    agent = with_memory(rag_chain)
    reply = agent.invoke(
                {"DATE": date, "NAME": name, "HOBBY": hobby, "LOCATION": location, "LANGUAGE": language, "WEATHER": weather,"EVENTS": events, "history": []},
        config={"configurable": {"session_id": name}}
    )
    return reply

def clean_text(s: str) -> str:
    s = s.replace("\x00", "")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()

def embed (PERSIST_DIR, EVPATH, ID): #embeding text + retriever
    with open(EVPATH, "r", encoding="utf-8") as f:
        text = f.read()
    raw = clean_text(text)
    chunks = splitter.split_text(raw)
    docs = [Document(page_content=t, metadata={"source":EVPATH,"chunk":i})
            for i,t in enumerate(chunks)]

    emb = OpenAIEmbeddings(model="text-embedding-3-small") # save function to emb
    db = Chroma.from_documents(docs, embedding=emb, persist_directory=PERSIST_DIR)
    LOG.data_log.info(f"Chroma index ready at: {PERSIST_DIR} with {len(docs)} chunks")
    retriever = db.as_retriever(search_kwargs={"k": 4}) # retriever function prepared
    LOG.data_log.info("Retriever ready.")  

    
    LOG.chunks_log.info(f"Split into {len(chunks)} chunks\n")

    for i, chunk in enumerate(chunks, start=1):
        LOG.chunks_log.info(f"====== CHUNK {i} ======")
        LOG.chunks_log.info(chunk)
        LOG.chunks_log.info(f"========================\n")
    return retriever

def createfile(ID: str) -> str:
  # Check if the file exists
    if not os.path.exists(PATH.Userdata_file.profile(ID)):
        profile = {
            "Name": "unknown",
            "Age": "unknown",
            "Birthday": "unknown",
            "Gender": "unknown",
            "Location": "unknown",
            "Relationship status": "unknown",
            "Kids": "unknown",
            "Kids hobbies": "unknown",
            "Pets": "unknown",
            "Occupation": "unknown",
            "Work schedule": "unknown",
            "Free time": "unknown",
            "Hobbies": "unknown",
            "Interests": "unknown",
            "Personality traits": "unknown",
            "Goals or aspirations": "unknown",
            "Other facts": "unknown"
        } 
        
        with open(PATH.Userdata_file.profile(ID), "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=4, ensure_ascii=False)
    
        return json.dumps(profile, ensure_ascii=False)
    else:
        with open(PATH.Userdata_file.profile(ID), "r", encoding="utf-8") as f:
            profile = f.read() # gives models look into info models already gathered previous sessions.
        return json.dumps(profile, ensure_ascii=False)

def main(city, ID):
    global PROMPT
    global llm
    global core_chain, rag_chain
    global location
    global coordinates, timezone
    global DATE, WtodaySum, EventSum, profile
    coordinates, timezone = get_location(city)
    WtodaySum = get_weather(city)  
    DATE,_ = EventFinder(None, city).DATEAdd(0)
    EventSum = EventFinder(ID, city).get_event()
    PERDIR = str(PATH.embedings_file.eventsEMB(ID))
    EVPATH = str(PATH.Userdata_file.events(ID))
    Retriever = embed(PERDIR, EVPATH, ID)  
    profile = createfile(ID)
#history and model system data preparation -*-*-*-*-
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)
    SYSTEM = (
    "Today is {DATE}. Keep in mind time when planing activity."
    "You speak to {NAME}."
    "Be polite."
    "Offer some activity for today that someone with these hobbies {HOBBY} would enjoy and take into acount current weather that is {WEATHER}."
    "Use {LANGUAGE} language"
    "Keep replies to 1–5 sentences."
    "Try to avoid repeating activities."
    "On top of your activity sugestion you can offer one event from list of {EVENTS} for activity later this week (if they match hobies). But filter out events that already happened or are more than 1 week ahead. And check the weather on the day of the event. Never provide links"
)
    PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    MessagesPlaceholder("history"),
    ])

    rag_inputs = RunnableParallel(
    DATE=RunnablePassthrough(),
    NAME=RunnablePassthrough(),
    HOBBY=RunnablePassthrough(),
    LOCATION=RunnablePassthrough(),
    LANGUAGE=RunnablePassthrough(),
    WEATHER=RunnablePassthrough(),
    EVENTS=RunnablePassthrough(),   
    history=itemgetter("history"), 
)

    core_chain   = PROMPT | llm | StrOutputParser()
    rag_chain    = rag_inputs | core_chain

    return("input proccesed")

#USER IMPUT and calling of the AImodel
def callmodel(ID, city, imp=None):

    if imp.lower() == "exit":
        return "Session exited. No model call."
    else:
        ans = convers(DATE, WtodaySum, EventSum, ID, profile, city)
        LOG.data_log.info(f"Gerry: {ans} \n")
        return ans      