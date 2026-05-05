import hashlib
import requests
from ttkbootstrap.dialogs import Messagebox
from tkinter import ttk
import tkinter as tk
from utils.hasher import *
# from views.login import Login
import keyring
import configparser
import pygame
import io

class Songlist(ttk.Frame):
    def __init__(self, root, on_logout_success=None):
        super().__init__(root, height=640, width=480, borderwidth=2, relief="groove")
        
        self.on_logout_success = on_logout_success
        
        # Load config values
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.server = config['server']['domain_name']
        self.username = config['server']['username']
        self.service_id = 'navidrome_sample_player'
        
        # Configure two columns that each take up 50% of the total window width
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1) # Top spacer row
        self.rowconfigure(1, weight=0) # Title row
        self.rowconfigure(2, weight=0) # Music list row
        self.rowconfigure(3, weight=0) # Button row
        self.rowconfigure(4, weight=1) # Bottom spacer row
        
        # Music List
        self.song_list_label = ttk.Label(self, text="Track List")
        self.song_list_label.grid(column=1, row=1)
        self.song_list = ttk.Treeview(self)
        self.song_list.column("#0", width=300, stretch=tk.NO)
        self.song_list.grid(column=1, row=2)
        
        # Buttons
        self.button_row_frame = ttk.Frame(self)
        self.button_row_frame.grid(row=3, column=1, sticky="nsew")
        
        # Shuffle
        self.shuffle_btn = ttk.Button(self.button_row_frame, text="Shuffle", command=self.populate_song_list)
        self.shuffle_btn.grid(column=0, row=0, sticky="nsew")
        
        # Play
        self.play_btn = ttk.Button(self.button_row_frame, text="Play", command=self.play_music)
        self.play_btn.grid(column=1, row=0, sticky="nsew")
        
        # Pause
        self.pause_btn = ttk.Button(self.button_row_frame, text="Pause", command=self.pause_music)
        self.pause_btn.grid(column=2, row=0, sticky="nsew")
        
        # Logout
        self.logout_btn = ttk.Button(self.button_row_frame, text="Logout", command=self.logout)
        self.logout_btn.grid(column=3, row=0, sticky="nsew")

        # Now Playing
        # Move this to its own class
        # style.configure('BlueFrame.TFrame', borderwidth=2, relief='solid', background='blue')
        # now_playing_frame = ttk.Frame(self,borderwidth=5, relief="ridge")
        # now_playing_frame.grid(row=0, column=1, sticky="nsew")
        # current_song_track_label = ttk.Label(now_playing_frame, text="Current Song")
        # current_song_track_label.grid(column=0, row=0, sticky="nsew")
        # current_song_track = ttk.Entry(now_playing_frame)
        # current_song_track.grid(column=1, row=0, sticky="nsew")
        # current_song_artist_label = ttk.Label(now_playing_frame, text="Current Artist")
        # current_song_artist_label.grid(column=0, row=1, sticky="nsew")
        # current_song_artist = ttk.Entry(now_playing_frame)
        # current_song_artist.grid(column=1, row=1, sticky="nsew")
        
        self.populate_song_list()
        
    def populate_song_list(self):
        # Populate random track list!
        password = keyring.get_password(self.service_id, self.username)  
        salt = hasher.salt_generator(self, 8)
        hashed_pw = hashlib.md5(f"{password}{salt}".encode("utf-8")).hexdigest()
        auth_url = f"https://{self.server}/rest/getRandomSongs?u={self.username}&t={hashed_pw}&s={salt}&v=1.13.0&c=myapp"
        response = requests.get(auth_url)
        decoded_response = hasher.response_parser(self, response)
        retrieved_songs = decoded_response['song']
        
        # Clear song_list (in case we're shuffling)
        self.song_list.delete(*self.song_list.get_children())

        for song in retrieved_songs:            
            self.song_list.insert("", 'end', text=song['@title'], values=(song['@title'],song['@id']))
        pass
    
    def play_music(self):
        # Check if we already initialized a pygame player
        if not pygame.mixer.get_init():
            # Start streaming playlist!
            password = keyring.get_password(self.service_id, self.username)  
            salt = hasher.salt_generator(self, 8)
            hashed_pw = hashlib.md5(f"{password}{salt}".encode("utf-8")).hexdigest()
            first_song_id = self.song_list.get_children()[0]
            first_song_data = self.song_list.item(first_song_id)
            subsonic_id = first_song_data['values'][1]
            auth_url = f"https://{self.server}/rest/stream?u={self.username}&t={hashed_pw}&s={salt}&v=1.13.0&c=myapp&id={subsonic_id}"
            response = requests.get(auth_url)
            audio_data = io.BytesIO(response.content)
            
            pygame.mixer.init()
            pygame.mixer.music.load(audio_data)
        pygame.mixer.music.play()

    
    def pause_music(self):
        pygame.mixer.music.pause()
    
    def logout(self):
        # Delete credentials from keyring and delete server info from config.ini
        # Keep all the other config settings for now, though
        config = configparser.ConfigParser()
        config.read('config.ini')
        username = config['server']['username']
        config['server'] = {}
        
        with open('config.ini', 'w') as configfile:
                config.write(configfile)
        
        # Attempt to clear password from keyring
        try:
            keyring.delete_password("navidrome_sample_player", username)
            print("Password deleted successfully.")
        except keyring.errors.PasswordDeleteError:
            print("Error: Password not found or could not be deleted.")
        
        self.on_logout_success()
        
class NowPlaying(ttk.Frame):
    def __init__(self):
        super().__init__(self)
        
        pass