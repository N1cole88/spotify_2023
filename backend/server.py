from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
#from trail import main
import datetime
import json
#from trail import getAnalysis, authenticate
from flask_cors import CORS
from spotify import Spotify
from gpt import analyze_vibe
from dotenv import load_dotenv
import os
import openai
from authhandler import AuthHandler
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode
from requests import post, get
import base64

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

date = datetime.datetime.now()

app = Flask(__name__)
app.secret_key = 'spot_12y'
CORS(app)


@app.route("/data", methods=["POST"])
def processData():
   argument = request.json
   print(argument)
   #response = getAnalysis(argument["limit"], argument["timeRange"])
   recent_top_tracks = spotifyInteract.get_user_top_tracks(argument["limit"], 0, argument["timeRange"])
   track_ids = []
   for i, item in enumerate(recent_top_tracks):
        print(f"{i + 1}. {item['name']} by {item['artists'][0]['name']}. track_id: {item['id']}")
        track_ids.append(item['id'])
   response = analyze_vibe(track_ids, spotifyInteract)
   response_data = {"date": date, 
                    "message": response}
   return jsonify(response_data), 200

if __name__ == "__main__":
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
    httpd.server_close()
    code = AuthHandler.getCode()
    print("\nReceived code", code)
    token, refresh_token = get_token(client_id, client_secret, code)
    global spotifyInteract 
    spotifyInteract = Spotify(client_id, client_secret, token, refresh_token)
    app.run(debug=True)
    