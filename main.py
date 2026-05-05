import tkinter as tk
# from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap import *

from views import login
from views import songlist

import configparser

class App:
    # Use this class to handle view routing and other high-level actions
    def __init__(self):
        self.root = ttk.Window()
        self.root.resizable(False, False)
        self.root.geometry("640x480")
        self.root.title("Simple Navidrome Client")
        self.startup()
        
    def startup(self):
        # Search for config values
        config = configparser.ConfigParser()
        config.read('config.ini')
        if 'domain_name' in config._sections['server']:
            # Previously authenticated, automatically jump to music screen
            self.show_songlist()
        else:
            # Create or open blank config file
            self.show_login()
        
    def clear_view(self):
        for child in self.root.winfo_children():
            child.destroy()
            
    def show_login(self):
        self.clear_view()
        form = login.Login(self.root, on_login_success=self.show_songlist)
        form.grid()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def show_songlist(self):
        self.clear_view()
        form = songlist.Songlist(self.root, on_logout_success=self.show_login)
        form.grid()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

def main():
    print("Hello from navidrome-music-player!")
    # The way we'll do this now is to initialize the App class
    app = App()
    app.root.attributes('-topmost', True) 
    app.root.mainloop()

if __name__ == "__main__":
    main()
