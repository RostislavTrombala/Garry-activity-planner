from pathlib import Path
from pypdf import PdfReader
from operator import itemgetter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
#clasic libraries
import os, re
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime, timedelta
from modules.Path_manager import PATH
from modules.logging_module import LOG
import requests
import json
load_dotenv()
ApK = os.getenv("OPENAI_API_KEY")

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
        input_messages_key="user_input",
        history_messages_key="history",
    )
    
def modelconv(ID: str, user_input: str, user_profile: str):
    agent = with_memory(rag_chain)
    reply = agent.invoke(
                {"ID": ID, "user_input": user_input, "user_profile": user_profile, "history": []},
        config={"configurable": {"session_id": ID}}
    )
    return reply

def modelnotes(ID: str, message: str, user_profile: str):
    agent = with_memory(rag_chain_NOTE)
    reply = agent.invoke(
                {"ID": ID, "message": message, "user_profile": user_profile},
        config={"configurable": {"session_id": ID}}
    )
    return reply

#function that will save info that model gathered into correct cathegories in JSON structure
def JSONmod(notes_values: dict, summary: dict) -> dict:
    for key, value in summary.items():
        
        if isinstance(value, str):
            value = value.strip()
        
        if value not in (None, "", "unknown"):  # ignore empty placeholders
            notes_values[key] = value
            
    return notes_values

NOTES_PROFILE = {
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

def Usercall(ID: str, UserImp: str, profile: str) -> None:  #USER IMPUT and call of the AI model writes whole conversation into txt file
        message = modelconv(ID, UserImp, profile)
        with open(PATH.Userdata_file.msg(ID), "a", encoding="utf-8") as f:
            f.write(f" User:{UserImp} \n Model:{message} \n ----- \n")
        return message

#loads file with conversation into file_content to pass it into another model that combines it with how notes looked at the begining and changes them to match the conversation. Passes output to Result that and Result is writen into JSON file. 
def Finalize (ID, profile) -> None:
    try:
        with open(PATH.Userdata_file.msg(ID), "r", encoding="utf-8") as f: 
            file_content = f.read()
        ModelOutput = modelnotes(ID, file_content, profile) # 
        ModelOutput = json.loads(ModelOutput)
        Result = JSONmod(profile, ModelOutput)
        with open(PATH.Userdata_file.profile(ID), "w", encoding="utf-8") as f:
            json.dump(Result, f, indent=4, ensure_ascii=False)
    except Exception:
        LOG.error_log.exception(f"Finalize ERROR for user {ID}")

def main(ID): 
    global PROMPT
    global llm
    global core_chain, rag_chain, core_chain_NOTE, rag_chain_NOTE

#    ID = input("Write you name")
    
#history and model system data preparation -*-*-*-*-
    try:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)
    except Exception:
        LOG.error_log.exception("Failed to initialize ChatOpenAI model")
        
    SYSTEM = (
    "You speak to {ID}. "
    "Keep your responses short (1–3 sentences). "
    "Your goal is to get to know the user and gather accurate personal information naturally through conversation. "
    "Ask friendly, context-aware questions that help you fill in the user's profile with real details — numbers, names, schedules, hobbies, and preferences. "
    "However, do not stay on the same topic for more than 2 questions or overanalyze minor details. "
    "Once you have asked user max three questions, immediately transition to a new topic in the structure unless user responds in long sentences."
        "For example If you asked user about his hobby and than 2 follow up questions change subject unless user responds in long sentences."
    "If the user gives short answers, shows disinterest, or avoids a question, politely change the topic. "
    "Avoid repeating questions or revisiting topics that are already covered. "
    "You may share a short interesting or fun fact about the current topic from time to time, to keep the chat natural. "
    "Never ask more than one question at a time. "
    "Be empathetic, curious, supportive, and sound like a natural conversational partner — not like an interviewer.\n\n"
    "Never ask sensitive personal information such as passwords, PIN codes, ID numbers, phone numbers, financial data, or details that could pose a security risk."
    "If the user shares such information, acknowledge it politely, warn user not to share such information online and change topic.\n" 
        
        "### FORMAT and SAVED PROFILE###\n"
        "Take note of what you already know about user."
        "Try to gather information to fill complete fallowing note structure\n"
        "{user_profile}"
)
    PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),    
    MessagesPlaceholder("history"),
    ("human", "{user_input}")
    ])

    rag_inputs = RunnableParallel(
    ID=RunnablePassthrough(),
    user_profile=RunnablePassthrough(),
    user_input=RunnablePassthrough(),
    history=itemgetter("history"), 
)

    core_chain   = PROMPT | llm | StrOutputParser()
    rag_chain    = rag_inputs | core_chain


    SYSTEM_NOTE = (
        "Your task is to extract and maintain brief, structured notes about the user based on the information you observe in conversation.\n"
        "Focus only on facts about the user that may be useful for personalization or context."
        "Ignore irrelevant chit-chat, temporary emotional states, and details about others unless directly related to the user.\n\n"
        "Always distinguish between **interests** (things the user enjoys voluntarily) "
        "and **work or duties** (things the user must do, such as a thesis, studies, or job tasks). "
        "If something sounds like an obligation or formal project, store it under 'Occupation' or 'Goals', not 'Interests'. "
        "Never store or record sensitive personal information such as passwords, PIN codes, ID numbers, phone numbers, financial data, or details that could pose a big security risk. "
        "If the user shares such information exclude it from the notes.\n"
        "Store general location information such as city, region, or neighborhood, but do not record exact street names, house numbers, apartment numbers.\n"
        "This is information you have. {user_profile} Expand it with new information you get."
    
        "### RULES ###\n"
        "- Be concise — summarize in short, factual statements.\n"
        "- Only include **confirmed or strongly implied** information.\n"
        "- Do not speculate or infer facts without clear evidence.\n"
        "- Keep text machine-friendly: avoid long sentences and filler words.\n"
        "- Do not include your reasoning or commentary — only facts about the user.\n\n"
        "- Avoid duplicating similar information — keep only the most current or accurate version of each fact."
       
        "### FORMAT ###\n"
        "You MUST respond ONLY with a valid JSON object.\n"
        "No explanation. No commentary. No surrounding text.\n"
        "Respond in this format:\n\n"
    
        "{{\n"
        "  \"Name\": \"...\",\n"
        "  \"Age\": \"...\",\n"
        "  \"Birthday\": \"...\",\n"
        "  \"Gender\": \"...\",\n"
        "  \"Location\": \"...\",\n"
        "  \"Relationship status\": \"...\",\n"
        "  \"Kids\": \"...\",\n"
        "  \"Kids hobbies\": \"...\",\n"
        "  \"Pets\": \"...\",\n"
        "  \"Occupation\": \"...\",\n"
        "  \"Work schedule\": \"...\",\n"
        "  \"Free time\": \"...\",\n"
        "  \"Hobbies\": \"...\",\n"
        "  \"Interests\": \"...\",\n"
        "  \"Personality traits\": \"...\",\n"
        "  \"Goals or aspirations\": \"...\",\n"
        "  \"Other facts\": \"...\"\n"
        "}}\n\n"
    
        "If information is missing, leave the field as \"unknown\".\n"
        "DO NOT write anything outside JSON."
    )

    PROMPT_NOTE = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_NOTE),
    ("human", "{message}")
    ])

    rag_inputs_NOTE = RunnableParallel(
    ID=RunnablePassthrough(),
    user_profile = RunnablePassthrough(),
    message=RunnablePassthrough(),
)

    core_chain_NOTE   = PROMPT_NOTE | llm | StrOutputParser()
    rag_chain_NOTE    = rag_inputs_NOTE | core_chain_NOTE

#Notesmodel    
    
    NOTES_PATH = Path(PATH.Userdata_file.profile(ID))
    try:
        #creating new NOTE file that saves info about user
        if not NOTES_PATH.exists():
            with open(NOTES_PATH, "w", encoding="utf-8") as f:
                json.dump(NOTES_PROFILE, f, indent=4, ensure_ascii=False)
            profile = NOTES_PROFILE.copy() # saves the structure so it can be modified
        else:
            with open(NOTES_PATH, "r", encoding="utf-8") as f:
                profile = json.load(f) # gives models look into info model already gathered in previous sessions.
    except Exception:
        LOG.error_log.exception(f"Error handling NOTES file for user {ID}")
        profile = NOTES_PROFILE.copy()
 
    return profile
#USER IMPUT and calling of the AImodel
if __name__ == "__main__":
    
    main()


# In[ ]:




