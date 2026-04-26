import hashlib
import requests
from ttkbootstrap.dialogs import Messagebox
from tkinter import ttk
from utils.hasher import *
import keyring
import configparser


class Songlist(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        
        # Music List
        self.music_list_frame = ttk.Frame(self)
        self.music_list_frame.grid(row=0, column=1)

        self.song_list_label = ttk.Label(self.music_list_frame, text="Songlist")
        self.song_list_label.grid(column=0, row=0)
        self.song_list = ttk.Treeview(self.music_list_frame)
        self.song_list.grid(column=0, row=1)

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
        
        self.populate_song_list(root)
        
    def populate_song_list(self, root):
        # Populate random track list!
        # We'll eventually just store a token and run the below through a "Shuffle" button
        service_id = 'navidrome_sample_player'
        config = configparser.ConfigParser()
        config.read('config.ini')
        server = config['server']['domain_name']
        username = config['server']['username']
        password = keyring.get_password(service_id, username)  
        salt = hasher.salt_generator(self, 8)
        hashed_pw = hashlib.md5(f"{password}{salt}".encode("utf-8")).hexdigest()
        auth_url = f"https://{server}/rest/getRandomSongs?u={username}&t={hashed_pw}&s={salt}&v=1.13.0&c=myapp"
        response = requests.get(auth_url)
        decoded_response = hasher.response_parser(self, response)
        retrieved_songs = decoded_response['song']
        for song in retrieved_songs:            
            self.song_list.insert("", 'end', text=song['@title'], values=(song['@title'],song['@id']))

    