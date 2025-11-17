import os
from pathlib import Path
import json


class PathLoad:
    def __init__(self):
        self.base = Path.home() / "garry" # PATH.base
        self.logs = self.base / "logs" # PATH.logs
        self.Userdata = self.base / "Userdata"  # PATH.Userdata
        self.uidata = self.Userdata / "uidata" # PATH.uidata 
        self.embedings = self.Userdata / "embedings" # PATH.embedings

        #creating paths for files and folders that require variable + all others files. All files are this way for consistency.
        self.Userdata_file = UserdataPaths(self.Userdata)
        self.uidata_file = UserdataPaths(self.uidata)
        self.logs_file = UserdataPaths(self.logs)
        self.embedings_file = UserdataPaths(self.embedings)

class UserdataPaths:
    def __init__(self, root: Path):
        self.root = root
        
    def msg(self, ID: str):
        return self.root / f"GerryprofileMSG{ID}.txt" # PATH.Userdata_file.msg(ID)

    def profile(self, ID: str):
        return self.root / f"Gerryprofile{ID}.json" # PATH.Userdata_file.profile(ID)

    def notes(self, ID: str):
        return self.root / f"GerryprofileNOTES{ID}.json" # PATH.Userdata_file.notes(ID)

    def cred(self):
        return self.root / "lastcred.json"  # PATH.uidata_file.cred()

    def log_errors(self):
        return self.root / "log_errors.txt" # PATH.logs_file.log_errors()
    def log_data(self):
        return self.root / "log_data.txt"  # PATH.logs_file.log_data()
    def log_dataWarn(self):
        return self.root / "log_dataWarn.txt" # PATH.logs_file.log_dataWarn()
    def log_chunks(self):
        return self.root / "log_chunks.txt" # PATH.logs_file.log_chunks()
        
    def events(self, ID: str):
        return self.root / f"Gerry{ID}events.txt"  # PATH.Userdata_file.events(ID)

    def eventsEMB(self, ID: str):
        return self.root / f"Gerry{ID}eventsEMB"  # PATH.embedings_file.eventsEMB(ID)




PATH = PathLoad()


