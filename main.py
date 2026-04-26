import tkinter as tk
from tkinter import ttk
import views.ui as ui
import views.login as login
import configparser
from views.ui import Songlist


def main():
    print("Hello from navidrome-music-player!")
    # Initialize main window
    root = tk.Tk()
    root.resizable(False, False)
    root.geometry("640x480")
    
    # Search for config values
    config = configparser.ConfigParser()
    config.read('config.ini')
    if len(config.read('config.ini')) != 0:        
        # Automatically jump to music screen
        form = Songlist(root)
        # Apply form to grid
        form.grid()
    else:
        # Start from scratch, create new config file
        config_ini = open("config.ini", "x")
    
        # Start by initializing the login view
        form = login.Login(root)
        
        # Apply form to grid
        form.grid()
        root.title("Simple Navidrome Client")
    root.attributes('-topmost', True) 
    root.mainloop()

if __name__ == "__main__":
    main()
