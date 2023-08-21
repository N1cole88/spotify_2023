import openai
from spotify import Spotify
import database
from gpt import *
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import webbrowser
from urllib.parse import urlencode
import pandas as pd
from pandas import json_normalize
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import threading

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global code

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Extract the authentication code from the query parameters
        query_params = parse_qs(urlparse(self.path).query)
        code = query_params.get("code", [""])[0]

        # Close the server once the code is received
        #print("\nReceived code", code)
        # Close the server once the code is received
        threading.Thread(target=self.server.shutdown).start()

def get_token(client_id, client_secret, code):
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code" : code,
        "redirect_uri": "http://localhost:7777/callback"
    }
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    refresh_token = json_result["refresh_token"]
    return token, refresh_token

    

def getAnalysis(limit, timeRange):
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    auth_headers = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": "http://localhost:7777/callback",
        "scope": "user-library-read user-library-modify user-read-private user-read-email playlist-read-private playlist-modify-public playlist-modify-private user-top-read user-read-recently-played user-read-currently-playing user-modify-playback-state user-modify-playback-state user-top-read"
    }

    # Start the local server
    server_address = ("localhost", 7777)
    httpd = HTTPServer(server_address, AuthHandler)

    # Start listening for the callback
    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))
    httpd.handle_request()
    #webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))
    #code = input("Please insert the authentication code: \n")
    print("\nReceived code", code)

    token, refresh_token = get_token(client_id, client_secret, code)
    spotifyInteract = Spotify(client_id, client_secret, token, refresh_token)
    #analyze_vibe("Ghost", spotifyInteract)
    recent_top_tracks = spotifyInteract.get_user_top_tracks(limit, 0, timeRange)
    # Extract all the track ids
    track_ids = []
    for i, item in enumerate(recent_top_tracks):
        print(f"{i + 1}. {item['name']} by {item['artists'][0]['name']}. track_id: {item['id']}")
        track_ids.append(item['id'])
    
    #print(spotifyInteract.get_track("4SykS8RWkF6eK6xeua7XLP")["name"])
    analysis = analyze_vibe(track_ids, spotifyInteract)
    return analysis

