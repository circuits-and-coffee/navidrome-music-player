import tkinter as tk    
from tkinter import ttk
from controllers.login_controller import login_controller
from utils.hasher import *
import hashlib
import random
import string
import requests


class Login(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

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
        
        # Music List
        self.music_list_frame = ttk.Frame(self, width=300, height=600)
        self.music_list_frame.grid(row=0, column=1)

        self.song_list_label = ttk.Label(self.music_list_frame, text="Songlist")
        self.song_list_label.grid(column=0, row=0)
        self.song_list = ttk.Treeview(self.music_list_frame)
        self.song_list.grid(column=0, row=1)
        # song_list.place(height=600, width=500)

        # Now Playing
        now_playing_frame = ttk.Frame(self)
        now_playing_frame.grid(row=1, column=0, columnspan=2)
        current_song_track_label = ttk.Label(now_playing_frame, text="Current Song")
        current_song_track_label.grid(column=0, row=0)
        current_song_track = ttk.Entry(now_playing_frame)
        current_song_track.grid(column=1, row=0)
        current_song_artist_label = ttk.Label(now_playing_frame, text="Current Song")
        current_song_artist_label.grid(column=0, row=1)
        current_song_artist = ttk.Entry(now_playing_frame)
        current_song_artist.grid(column=1, row=1)
        
    def initiate_login(self):
        # Use this method to authenticate
        
        # Capture input parameters
        server = self.server_url.get() # Need to get just the domain/subdomain
        un = self.username_input.get()
        pw = self.password_input.get()
        
        """ From Subsonic API docs
    Starting with API version 1.13.0, the recommended authentication scheme is to send an
    authentication token, calculated as a one-way salted hash of the password.

    This involves two steps:

    1) For each REST call, generate a random string called the salt. Send this as parameter s.
        - Use a salt length of at least six characters.
    2) Calculate the authentication token as follows: token = md5(password + salt). The md5() function takes a string and returns the 32-byte ASCII hexadecimal representation of the MD5 hash, using lower case characters for the hex values. The '+' operator represents concatenation of the two strings. Treat the strings as UTF-8 encoded when calculating the hash. Send the result as parameter t.

    For example: if the password is sesame and the random salt is c19b2d, then token = md5("sesamec19b2d") = 26719a1196d2a940705a59634eb18eab. The corresponding request URL then becomes:
    http://your-server/rest/ping.view?u=joe&t=26719a1196d2a940705a59634eb18eab&s=c19b2d&v=1.13.0&c=myapp

        """
        
        # Generate salt & hashed combination
        salt = hasher.salt_generator(self, 8)
        # token = hashlib.md5(f"{pw}{salt}")
        hashed_pw = hashlib.md5(f"{pw}{salt}".encode("utf-8")).hexdigest()
        
        # Build the auth URL
        auth_url = f"{server}/rest/ping.view?u={un}&t={hashed_pw}&s={salt}&v=1.13.0&c=myapp"
        
        # Call the auth URL
        response = requests.get(auth_url) # Hmm, this is always returning <200>'s...
        
        # Handle response code
        
        pass