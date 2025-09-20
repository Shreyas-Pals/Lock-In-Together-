import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import client

load_dotenv()

sp_oauth = SpotifyOAuth(
    client_id = os.getenv("CLIENT_ID"),
    client_secret = os.getenv("CLIENT_SECRET"),
    redirect_uri=redirect_uri,
    scope="user-modify-playback-state user-read-playback-state",
    show_dialog=True,
    cache_path = '.cache_new'
)

if master_role.set():
    

    master_role.clear()