import hashlib
import requests
from ttkbootstrap.dialogs import Messagebox
from tkinter import ttk
from utils.hasher import *
from views.ui import Songlist
import keyring
import configparser


class Login(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        # Will change the UI
        self.columnconfigure(0, weight=0, minsize=400)  # Left column (server details)
        self.columnconfigure(1, weight=0, minsize=600)  # Right column (music list)
        self.rowconfigure(0, weight=0, minsize=300)     # Top row
        self.rowconfigure(1, weight=0, minsize=180)     # Bottom row (now playing)
        
        # Main Server Details
        server_details_frame = ttk.Frame(self, width=400, height=300)
        server_details_frame.grid(row=0, column=0)

        self.server_url_label = ttk.Label(server_details_frame, text="Enter Server URL")
        self.server_url_label.grid(column=0, row=0)
        self.server_url = ttk.Entry(server_details_frame)
        self.server_url.grid(column=1, row=0)
        self.username_label = ttk.Label(server_details_frame, text="Enter Username")
        self.username_label.grid(column=0, row=1)
        self.username_input = ttk.Entry(server_details_frame)
        self.username_input.grid(column=1, row=1)
        self.password_label = ttk.Label(server_details_frame, text="Enter Password")
        self.password_label.grid(column=0, row=2)
        self.password_input = ttk.Entry(server_details_frame, show="*")
        self.password_input.grid(column=1, row=2)
        self.login_btn = ttk.Button(server_details_frame, text="Login", command=self.initiate_login)
        self.login_btn.grid(column=0, row=3)
        self.quit_btn = ttk.Button(server_details_frame, text="Quit", command=root.destroy)
        self.quit_btn.grid(column=0, row=5)
        
        # server_details_frame.grid(row=0, column=0, sticky="nsew")
        # self.music_list_frame.grid(row=0, column=1, sticky="nsew")
        # now_playing_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        
        self.root = root
        
    def initiate_login(self):
        # Use this method to authenticate
        
        # Capture input parameters
        server = self.server_url.get()
        if server.startswith("https://"):
            server = server.lstrip("https://")
        un = self.username_input.get()
        pw = self.password_input.get()
        
        # Generate salt & hashed combination
        salt = hasher.salt_generator(self, 8)
        hashed_pw = hashlib.md5(f"{pw}{salt}".encode("utf-8")).hexdigest()
        
        # Build the auth URL
        auth_url = f"https://{server}/rest/ping?u={un}&t={hashed_pw}&s={salt}&v=1.13.0&c=myapp"
        
        # Call the auth URL
        response = requests.get(auth_url) # Always returns <200>'s by design.
        # Need to examine the "subsonic-response" in the response for errors
        decoded_response = hasher.response_parser(self, response)
        
        # Handle response
        if decoded_response['@status'] == 'failed':
            Messagebox.show_error(message=f"Error: {decoded_response['@message']}")
        else:
            # Store server info to config.ini & credentials to keyring
            config = configparser.ConfigParser()
            config['server'] = {
                'domain_name': server,
                'username': un
            }

            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            
            service_id = 'navidrome_sample_player'
            keyring.set_password(service_id, un, pw)
            
            # Load the SongList view      
            self.destroy()
            form = Songlist(self.root)
            # Apply form to grid
            form.grid()