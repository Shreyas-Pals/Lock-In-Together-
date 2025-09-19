from flask import Flask, request,render_template,session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

# =None as its a dict
token_info = None

master_token,master_id = None , None

users = {}

app = Flask(__name__)

redirect_uri = "http://127.0.0.1:5000/callback"

print("CLIENT_ID from env:", os.getenv("CLIENT_ID"))

sp_oauth = SpotifyOAuth(
    client_id = os.getenv("CLIENT_ID"),
    client_secret = os.getenv("CLIENT_SECRET"),
    redirect_uri=redirect_uri,
    scope="user-modify-playback-state user-read-playback-state",
    show_dialog=True,
    cache_path = '.cache_new'
)


@app.route("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return f'<a href="{auth_url}">Login with Spotify</a>'

@app.route("/callback")
def callback():
    code = request.args.get("code")

    if not code:
        return "No code received"
    
    try:
        global token_info
        # Get token from code
        token_info = sp_oauth.get_access_token(code, check_cache=False)
        """
               This is for one user: access_token = token_info['access_token']
               For multi users, i gotta isolate everyone's token, so we import session which does that
               for us by setting a cookie for every user.
        """
        session['token_info'] = token_info

        return render_template("index.html")

    except Exception as e:
        print("Error in callback:", e)
        return f"Callback failed: {e}"
    
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    global master_token,master_id
    sp = spotipy.Spotify(auth=token_info["access_token"])
    me = sp.current_user()
    user_id = me["id"]
    username = me["display_name"]

    users[user_id] = {"Name": username, "Picks":[]}

    if master_token is None:
        master_token = token_info
        master_id = user_id
        session['is_master'] = True
        # sp_master = spotipy.Spotify(auth=master_token['access_token'])

    else:
        session['is_master'] = False    

    return render_template("home.html")

if __name__ == "__main__":

    app.run(port=5000,debug = True)

