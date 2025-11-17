import os
import json
from modules.logging_module import LOG

def loadJSON(Path) -> str:
    try:
        with open(Path, "r", encoding="utf-8") as f:
            Data = json.load(f)
            FData = json.dumps(Data, indent=4) # into lines instead of text blob
    except Exception as e:
        LOG.dataWarn_log.exception(f"loadJSON ERROR — Path: {Path}")
        FData = "No user info gathered"
    
    return FData       

def loadJSONcred(creds_path) -> str:
    try:
        if os.path.exists(creds_path):
            with open(creds_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        
            line1 = data.get("username", "")
            line2 = data.get("city", "")
        else:
            line1 = ""
            line2 = ""
    except:
        LOG.dataWarn_log.exception("loadJSONcred ERROR")
        line1 = ""
        line2 = ""
        
    return line1, line2