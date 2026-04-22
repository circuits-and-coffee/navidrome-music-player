import tkinter as tk
from tkinter import ttk
import views.ui as ui

def main():
    print("Hello from navidrome-music-player!")
    
    # Initialize main window
    root = tk.Tk()
    
    # Login will be the top left, songlist will be top right, player will be bottom half
    form = ui.Login(root)
    
    # Apply form to grid
    form.grid()
    root.title("Simple Navidrome Client")
    root.attributes('-topmost', True) 
    root.mainloop()

if __name__ == "__main__":
    main()
