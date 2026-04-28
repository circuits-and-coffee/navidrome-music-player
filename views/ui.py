import hashlib
import requests
from ttkbootstrap.dialogs import Messagebox
from tkinter import ttk
from utils.hasher import *
import keyring
import configparser
import pygame
import io

class Songlist(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        
        # Load config values
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.server = config['server']['domain_name']
        self.username = config['server']['username']
        self.service_id = 'navidrome_sample_player'
        
        # Configure two columns that each take up 50% of the total window width
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)
        
        style = ttk.Style()
        style.configure('CustomRed.TFrame', background='red', borderwidth=2, relief='solid')
        style.map('CustomRed.TFrame', background=[('active', 'red')])  # Ensure it applies on interaction
        
        # Music List
        self.music_list_frame = ttk.Frame(self,borderwidth=5, relief="ridge")
        self.music_list_frame.grid(row=0, column=0, sticky="nsew")

        self.song_list_label = ttk.Label(self.music_list_frame, text="Songlist")
        self.song_list_label.grid(column=0, row=0)
        self.song_list = ttk.Treeview(self.music_list_frame)
        self.song_list.grid(column=0, row=1)
        
        # Buttons
        self.button_row_frame = ttk.Frame(self)
        self.button_row_frame.grid(row=2, column=0, sticky="nsew")
        
        # Shuffle
        self.shuffle_btn = ttk.Button(self.button_row_frame, text="Shuffle", command=self.populate_song_list)
        self.shuffle_btn.grid(column=0, row=0)
        
        # Play
        self.shuffle_btn = ttk.Button(self.button_row_frame, text="Play", command=self.play_music)
        self.shuffle_btn.grid(column=1, row=0)
        
        # Pause
        self.shuffle_btn = ttk.Button(self.button_row_frame, text="Pause", command=self.pause_music)
        self.shuffle_btn.grid(column=2, row=0)
        
        # Logout
        self.shuffle_btn = ttk.Button(self.button_row_frame, text="Logout", command=self.logout)
        self.shuffle_btn.grid(column=3, row=0)

        # Now Playing
        style.configure('BlueFrame.TFrame', borderwidth=2, relief='solid', background='blue')
        now_playing_frame = ttk.Frame(self,borderwidth=5, relief="ridge")
        now_playing_frame.grid(row=0, column=1, sticky="nsew")
        current_song_track_label = ttk.Label(now_playing_frame, text="Current Song")
        current_song_track_label.grid(column=0, row=0, sticky="nsew")
        current_song_track = ttk.Entry(now_playing_frame)
        current_song_track.grid(column=1, row=0, sticky="nsew")
        current_song_artist_label = ttk.Label(now_playing_frame, text="Current Artist")
        current_song_artist_label.grid(column=0, row=1, sticky="nsew")
        current_song_artist = ttk.Entry(now_playing_frame)
        current_song_artist.grid(column=1, row=1, sticky="nsew")
        
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
            
            decoded_response = hasher.response_parser(self, response) # There's a bug with this I'll have to debug later
            audio_data = io.BytesIO(response.content)
            
            pygame.mixer.init()
            pygame.mixer.music.load(audio_data)
            pygame.mixer.music.play()
        else:
            # Resume music playback?
            pygame.mixer.music.play()
    
    def pause_music(self):
        pygame.mixer.music.pause()
    
    def logout():
        # Delete credentials from keyring and delete server info from config.ini
        # Keep all the other config settings for now, though
        
        pass