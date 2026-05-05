import hashlib
import requests
from ttkbootstrap.dialogs import Messagebox
from tkinter import ttk
from ttkbootstrap import *
from utils.hasher import *
import keyring
import configparser


class Login(ttk.Frame):
    
    def __init__(self, root, on_login_success=None):
        super().__init__(root, height=640, width=480, borderwidth=2, relief="groove")
        
        self.on_login_success = on_login_success
        
        # Main Server Details        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1) # Top row spacer
        self.rowconfigure(1, weight=0) # "Login" text row
        self.rowconfigure(2, weight=0) # Server domain row
        self.rowconfigure(3, weight=0) # Username row
        self.rowconfigure(4, weight=0) # Password row
        self.rowconfigure(5, weight=0) # Button row
        self.rowconfigure(6, weight=1) # Bottom row spacer
        
        
        self.server_url_label = ttk.Label(self, text="Login to your Navidrome/Subsonic Instance")
        self.server_url_label.grid(column=1, row=1, columnspan=2)
        self.server_url_label = ttk.Label(self, text="Enter Server URL")
        self.server_url_label.grid(column=1, row=2)
        self.server_url = ttk.Entry(self)
        self.server_url.grid(column=2, row=2)
        self.username_label = ttk.Label(self, text="Enter Username")
        self.username_label.grid(column=1, row=3)
        self.username_input = ttk.Entry(self)
        self.username_input.grid(column=2, row=3)
        self.password_label = ttk.Label(self, text="Enter Password")
        self.password_label.grid(column=1, row=4)
        self.password_input = ttk.Entry(self, show="*")
        self.password_input.grid(column=2, row=4)
        self.login_btn = ttk.Button(self, text="Login", command=self.initiate_login)
        self.login_btn.grid(column=1, row=5)
        self.quit_btn = ttk.Button(self, text="Quit", command=root.destroy)
        self.quit_btn.grid(column=2, row=5)
        
        self.root = root
        
        
    def initiate_login(self):
        # Use this method to authenticate
        
        # Capture input parameters
        server = self.server_url.get()
        if server.startswith("https://"):
            server = server.removeprefix("https://")
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
            
            # Attempt to add password to keyring
            service_id = 'navidrome_sample_player'
            try:
                keyring.set_password(service_id, un, pw)
                print("Password added successfully.")
            except keyring.errors.Password:
                print("Error: Unable to add password")
            
            # Call our on_login_success function
            self.on_login_success()
