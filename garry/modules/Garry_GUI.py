print("Script started!")
input()

from pathlib import Path  
import sys, os

# to run script with doubleclick
BASE = Path(__file__).resolve().parent
os.chdir(BASE)
sys.path.insert(0, str(BASE))

import tkinter as tk
from tkinter import ttk
from GarryGUIcore import main, callmodel
from modules.FileManager import loadJSON, loadJSONcred
from modules.Path_manager import PATH


class GerryApp(tk.Tk):
    """Main application window for Gerry Assistant"""

    def __init__(self):
        super().__init__()

        # -------- Window Configuration --------
        self.title("Main Window")
        self.config(bg="#E4E2E2")
        self.geometry("700x370")

        # Initialize styles, menu, and GUI widgets
        self._init_styles()
        self._init_menu()
        self._create_widgets()
        self._layout_widgets()

    # =====================================================
    # login retainer
    # =====================================================
        self.ID, self.city = loadJSONcred(str(PATH.uidata_file.cred()))
        self.username_entry.insert(0, self.ID)
        self.city_entry.insert(0, self.city)
    # =====================================================
    # STYLE CONFIGURATION
    # =====================================================
    def _init_styles(self):
        """Define ttk widget styles."""
        style = ttk.Style(self)
        style.theme_use("clam")

        # Entry styles
        style.configure("entry.TEntry", fieldbackground="#fff", foreground="#000")
        style.configure("entry1.TEntry", fieldbackground="#fff", foreground="#000")

        # Label styles
        style.configure("citylabel.TLabel", background="#E4E2E2", foreground="#000", anchor="center")
        style.configure("usernamebutton.TLabel", background="#E4E2E2", foreground="#000", anchor="center")

        # Button styles
        for btn_style in [
            "insertbutton.TButton",
            "runbutton.TButton",
            "cancelbutton.TButton",
            "notesbutton.TButton",
        ]:
            style.configure(btn_style, background="#E4E2E2", foreground="#000")
            style.map(
                btn_style,
                background=[("active", "#E4E2E2")],
                foreground=[("active", "#000")],
            )

    # =====================================================
    # MENU BAR
    # =====================================================
    def _init_menu(self):
        """Create the menu bar."""
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=lambda: print("New clicked"))
        file_menu.add_command(label="Open", command=lambda: print("Open clicked"))

        # Add dropdown to the menu bar
        menu_bar.add_cascade(label="File", menu=file_menu)

    # =====================================================
    # WIDGET CREATION
    # =====================================================
    def _create_widgets(self):
        """Create all widgets used in the interface."""

        # Labels
        self.city_label = ttk.Label(self, text="City:", style="citylabel.TLabel")
        self.username_label = ttk.Label(self, text="Username", style="usernamebutton.TLabel")

        # Entry fields
        self.city_entry = ttk.Entry(self, style="entry.TEntry")
        self.username_entry = ttk.Entry(self, style="entry1.TEntry")

        # Buttons
        self.insert_button = ttk.Button(self, text="Insert", style="insertbutton.TButton", command=self.insert_action)
        self.run_button = ttk.Button(self, text="Run", style="runbutton.TButton", command=self.run_action)
        self.cancel_button = ttk.Button(self, text="Cancel", style="cancelbutton.TButton", command=self.cancel_action)
        self.notes_button = ttk.Button(self, text="Questionare", style="notesbutton.TButton", command=self.show_questionnaire)

        # Text fields
        self.output_text = tk.Text(self, bg="#fff", fg="#000")
        self.persona_notes = tk.Text(self, bg="#fff", fg="#000")

    # =====================================================
    # LAYOUT
    # =====================================================
    def _layout_widgets(self):
        """Position all widgets on the window using absolute coordinates (same as original)."""

        # City input
        self.city_label.place(x=5, y=10, width=80, height=40)
        self.city_entry.place(x=87, y=8, width=130, height=40)

        # Username input
        self.username_label.place(x=7, y=61, width=80, height=40)
        self.username_entry.place(x=88, y=60, width=130, height=40)

        # Buttons
        self.insert_button.place(x=228, y=36, width=100, height=40)
        self.run_button.place(x=30, y=139, width=87, height=40)
        self.cancel_button.place(x=129, y=139, width=105, height=40)
        self.notes_button.place(x=503, y=22, width=132, height=36)

        # Text areas
        self.output_text.place(x=31, y=210, width=390, height=104)
        self.persona_notes.place(x=454, y=78, width=225, height=229)
       


    # =====================================================
    # EVENT HANDLERS (Button Commands)
    # =====================================================
    
    def insert_action(self):
        if os.path.exists(PATH.uidata_file.cred()):
            os.remove(PATH.uidata_file.cred())
        self.city = self.city_entry.get()
        self.ID = self.username_entry.get()
        self.validation = main(self.city, self.ID)
        NOTES_text = loadJSON(PATH.Userdata_file.profile(self.ID))
        self.persona_notes.delete("1.0", "end")
        self.persona_notes.insert("end", NOTES_text)
        try:
            with open(PATH.uidata_file.cred(), "w", encoding="utf-8") as f:
                json.dump({
                    "username": self.ID,
                    "city": self.city
                }, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("did not work", e)
    

    def run_action(self):
        if self.validation != None:
            ans = callmodel("RUN" ,self.ID , self.city)
            self.output_text.delete("1.0", "end") 
            self.output_text.insert("end", ans)  
        else: 
            self.insert_action(self)
      
    def cancel_action(self):
        callmodel("exit")
        self.output_text.delete("1.0", "end") 
        self.output_text.insert("end", " ") 
 

    def show_questionnaire(self):
        from modules.LitteGarryUI import LitGGUI
        """Triggered when 'Questionare' button is pressed."""
        try:
            self.withdraw()                # hide main window
            LitGGUI(self, self.ID)   
        except:
            self.output_text.delete("1.0", "end") 
            self.output_text.insert("end", "Frist write your username and press insert")        
        

# =====================================================
# APP ENTRY POINT
# =====================================================
if __name__ == "__main__":
    try:
        app = GerryApp()
        app.mainloop()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("\n\nERROR! Press Enter to close...")



