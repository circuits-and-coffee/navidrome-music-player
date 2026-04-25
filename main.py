import tkinter as tk
from tkinter import ttk
import views.ui as ui
import views.login as login

def main():
    print("Hello from navidrome-music-player!")
    
    # Initialize main window
    root = tk.Tk()
    root.resizable(False, False)
    root.geometry("640x480")
    
    # form = ui.Songlist(root)
    
    # Start by initializing the login view
    form = login.Login(root)
    
    # Apply form to grid
    form.grid()
    root.title("Simple Navidrome Client")
    root.attributes('-topmost', True) 
    root.mainloop()

if __name__ == "__main__":
    main()
