import os
import tkinter as tk
from tkinter import ttk
from modules.G_Notebot import main, Usercall, Finalize
from modules.logging_module import LOG

class LitGGUI(tk.Toplevel):
    """Main application window for Gerry Assistant"""

    def __init__(self, parent, ID):
 #       super().__init__()
        super().__init__(parent)        # pass parent to Toplevel
        self.parent = parent   #sss
        try:
#    loading ID and profile data.
            self.ID = ID
            self.profile = main(ID)
        except Exception as e:
            LOG.error_log.exception("ERROR in Notemaking AI main(ID)")
            raise
        
        # Window Configuration 
        self.title("Main Window")
        self.config(bg="#E4E2E2")
        self.geometry("700x370")


        # Initialize styles, menu, and GUI widgets
        self._init_styles()
        self._init_menu()
        self._create_widgets()
        self._layout_widgets()

    # =====================================================
    # STYLE CONFIGURATION
    # =====================================================
    def _init_styles(self):
        """Define ttk widget styles."""
        style = ttk.Style(self)
        style.theme_use("clam")

        # Entry styles
        style.configure("entry.TEntry", fieldbackground="#fff", foreground="#000")

        #=== Button styles ===#
        for btn_style in ["Send.TButton"]:
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

        # Buttons
        self.Send_button = ttk.Button(self, text=">>", width=4, style="Send.TButton", command=self.Send_action)
        self.Back_button = ttk.Button(self, text="Save and return", width=4, style="Back.TButton", command=self.Back_action)

        # Text fields
        self.output_text = tk.Text(self, bg="#fff", fg="#000", wrap="word")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=self.scrollbar.set)

        # user input
        self.usermsg_entry = ttk.Entry(self)

        #keybind
        self.usermsg_entry.bind("<Return>", self.on_enter)

    # =====================================================
    # LAYOUT
    # =====================================================
    def _layout_widgets(self):
        #=== resizing of the widgets ===#    
        self.rowconfigure(0, weight=0, minsize=50)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0, minsize=50)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)


        #=== positioning of the widgets on the grid ===#  
        #= send button =#
        self.Send_button.grid(row=2, column=1, padx=(0, 15), pady=(0, 15), sticky="e")
        #= userimp =#
        self.usermsg_entry.grid(row=2, column=0, sticky="nsew", padx=(15, 15), pady=(0, 15), ipady=3)
        #= output window =#
        self.output_text.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(15, 15), pady=(15, 15))
        #= back button =#
        self.Back_button.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=(15, 15), pady=(15, 0))
        #= scrollbar =#
        self.scrollbar.grid(row=1, column=2, rowspan=2, sticky="ns", padx=(0, 0), pady=(5, 5))

    
    # =====================================================
    # EVENT HANDLERS (Button Commands)
    # =====================================================

    def on_enter(self, event):
        self.Send_action()
    
    def Send_action(self):
        user_message = self.usermsg_entry.get().strip()
        if not user_message:
            return
        try:
            msg = Usercall(self.ID, user_message, self.profile)
        except Exception:
            LOG.error_log.exception("Error in Usercall() during Send_action")
            msg = "[ERROR] Unable to process your message right now."
        self.output_text.insert("1.0", f"\n{user_message}\n")
        self.output_text.insert("1.0", f"\n{msg}\n")
        self.output_text.see("end")
        self.usermsg_entry.delete(0, "end")
    

    def Back_action(self):
        try:
            Finalize(self.ID, self.profile)
        except Exception:
            LOG.error_log.exception("Error in Finalize() during Back_action")
        finally:
            self.parent.deiconify()
            self.destroy()