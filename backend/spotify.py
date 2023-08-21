from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import webbrowser
from urllib.parse import urlencode
import pandas as pd
from pandas import json_normalize
import database

class Spotify:
    def __init__(self, client_id, client_secret, token, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token
        self.refresh_token = refresh_token
        self.df = None

    def get_auth_header(self):
        return {"Authorization" : "Bearer " + self.token}

    def refresh_access_token(self):
        refresh_token = self.refresh_token
        client_id = self.client_id
        client_secret = self.client_secret

        refresh_data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': client_id,
            'client_secret': client_secret
        }

        response = post('https://accounts.spotify.com/api/token', data=refresh_data)

        if response.status_code == 200:
            response_data = response.json()
            new_access_token = response_data['access_token']
            self.token = new_access_token
            print('Access token refreshed successfully!')
        else:
            print('Error refreshing access token:', response.status_code)


    def search_for_artist(self, artist_name):
        url = "https://api.spotify.com/v1/search"
        headers = self.get_auth_header()
        query = f"?q={artist_name}&type=artist&limit=1"
        query_url = url + query
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)["artists"]["items"] 
        #print(json_result)
        if len(json_result) == 0:
            print("No artist with this name....")
            return None
        
        return json_result[0]

    def search_for_track(self, track_name, limit):
        url = "https://api.spotify.com/v1/search"
        headers = self.get_auth_header()
        query = f"?q={track_name}&type=track&limit={limit}"
        query_url = url + query
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)["tracks"]["items"] 
        #print(json_result)
        if len(json_result) == 0:
            print("No tracks with this name....")
            return None
        
        return json_result

    def get_songs_by_artist(self, artist_id, country):
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country={country}"
        headers = self.get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["tracks"]
        return json_result

    def get_current_playing_track(self):
        url = f"https://api.spotify.com/v1/me/player/currently-playing"
        headers = self.get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["item"]
        return json_result
    
    def get_track(self, id):
        url = f"https://api.spotify.com/v1/tracks/{id}"
        headers = self.get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        return json_result
    
    def skip_to_next(self):
        url = "https://api.spotify.com/v1/me/player/next"
        headers = self.get_auth_header()
        result = post(url, headers=headers)
        if result.status_code == 204:
            print('Skipped to the next song in queue!')
        elif result.status_code == 403:
            self.refresh_access_token()
            # Retry the request with the new access token
            print("new: ", self.token)
            self.skip_to_next()
        else:
            print('Error:', result.status_code)

    def skip_to_prev(self):
        url = "https://api.spotify.com/v1/me/player/previous"
        headers = self.get_auth_header()
        result = post(url, headers=headers)
        if result.status_code == 204:
            print('Skipped to the previous song in queue!')
        elif result.status_code == 403:
            self.refresh_access_token()
            # Retry the request with the new access token
            print("new: ", self.token)
            self.skip_to_next()
        else:
            print('Error:', result.status_code)


    def get_my_profile(self):
        url = f"https://api.spotify.com/v1/me"
        data = {"grant_type": "client_credentials"}
        headers = self.get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)

        df = json_normalize(json_result)
        print(df)

        return json_result

    def getPlaylist(self):
        url = f"https://api.spotify.com/v1/me/playlists?limit=20&offset=0"
        headers = self.get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["items"]
        return json_result

    def getPlaylistItems(self, limit, offset):
        url = f"https://api.spotify.com/v1/playlists/5Dww7ikBY4JDVUe5Csdpm8/tracks?limit={limit}&offset={offset}"
        headers = self.get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["items"]
        return json_result

    def getNthPlaylistNumTotal(self, n):        
        total = self.getPlaylist()[n]["tracks"]["total"]
        return total

    def create_new_playlist(self, user_id):
        pass
    def add_items_to_playlist(self, playlist_id, uris, position):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {
            'Authorization' : "Bearer " + self.token,
            'Content-Type': 'application/json',
            "scope": "user-library-read user-library-modify user-read-private user-read-email playlist-read-private playlist-modify-public playlist-modify-private user-top-read user-read-recently-played user-read-currently-playing user-modify-playback-state user-modify-playback-state"
            }

        data = {
            'uris': uris,
            'position': position
        }
        data_json = json.dumps(data)
        result = post(url, headers=headers, data=data_json)
        #json_result = json.loads(result.content)
        if result.status_code == 201:
            print('Items added to playlist successfully!')
        elif result.status_code == 403:
            print("Error 403 here inside add")
            self.refresh_access_token()
            # Retry the request with the new access token
            print("new: ", self.token)
            self.add_items_to_playlist(playlist_id, uris, position)
        else:
            print('Error:', result.status_code)

    def add_items_to_playlist_by_name(self, playlist_id, names):
        uris = [self.search_for_track(i, 1)[0]["uri"] for i in names]
        print("uris\n", uris)
        self.add_items_to_playlist(playlist_id, uris, 0)

    def get_user_top_tracks(self, limit, offset, range):
        url = f"https://api.spotify.com/v1/me/top/tracks?&limit={limit}&offset={offset}&time_range={range}"
        headers = self.get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["items"]
        return json_result
    
    def getArtistGenres(self, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        headers = self.get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["genres"]
        return json_result

    def getAudioFeatures(self, track_id):
        url = f"https://api.spotify.com/v1/audio-features/{track_id}"
        headers = self.get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        return json_result
    
    def getRecentTracks(self, limit):
        url = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}"
        headers = self.get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["items"]
        return json_result
    
    def getDefaultDataframe(self):
        total_num_of_songs = self.getNthPlaylistNumTotal(2)
        data_dict = {"track_id" : [], "track_name" : [], "album_name" : [],  "album_popularity" : [], "release_date": [], "artist_name" : [], "artist_genres" : [], "acousticness" : [], "danceability" : [], "energy": [], "instrumentalness" : [], "liveness" : [], "loudness" : [], "mode" : [], "speechiness" : [], "tempo" : [], "valence" : []}
        for n in range(total_num_of_songs // 100):
            tracks = self.getPlaylistItems(100, n * 100)
            for item in tracks:
                data_dict["track_id"].append(item["track"]["id"])
                data_dict["track_name"].append(item["track"]["name"])
                data_dict["album_name"].append(item["track"]["album"]["name"])
                data_dict["album_popularity"].append(item["track"]["popularity"])
                data_dict["release_date"].append(item["track"]["album"]["release_date"])
                data_dict["artist_name"].append(item["track"]["album"]["artists"][0]["name"])
                artist_genres = self.getArtistGenres(item["track"]["album"]["artists"][0]["id"])
                if len(artist_genres) == 0:
                    genres = "NaN"
                else:
                    genres = ",".join(artist_genres)
                data_dict["artist_genres"].append(genres)
                audio_features = self.getAudioFeatures(item["track"]["id"])
                data_dict["acousticness"].append(audio_features["acousticness"])
                data_dict["danceability"].append(audio_features["danceability"])
                data_dict["energy"].append(audio_features["energy"])
                data_dict["instrumentalness"].append(audio_features["instrumentalness"])
                data_dict["liveness"].append(audio_features["liveness"])
                data_dict["loudness"].append(audio_features["loudness"])
                data_dict["mode"].append(audio_features["mode"])
                data_dict["speechiness"].append(audio_features["speechiness"])
                data_dict["tempo"].append(audio_features["tempo"])
                data_dict["valence"].append(audio_features["valence"])
                

        offset = total_num_of_songs // 100 * 100
        limit = total_num_of_songs - offset
        tracks = self.getPlaylistItems(limit, offset)
        for item in tracks:
                data_dict["track_id"].append(item["track"]["id"])
                data_dict["track_name"].append(item["track"]["name"])
                data_dict["album_name"].append(item["track"]["album"]["name"])
                data_dict["album_popularity"].append(item["track"]["popularity"])
                data_dict["release_date"].append(item["track"]["album"]["release_date"])
                data_dict["artist_name"].append(item["track"]["album"]["artists"][0]["name"])
                artist_genres = self.getArtistGenres(item["track"]["album"]["artists"][0]["id"])
                if len(artist_genres) == 0:
                    genres = "NaN"
                else:
                    genres = ",".join(artist_genres)
                data_dict["artist_genres"].append(genres)
                audio_features = self.getAudioFeatures(item["track"]["id"])
                data_dict["acousticness"].append(audio_features["acousticness"])
                data_dict["danceability"].append(audio_features["danceability"])
                data_dict["energy"].append(audio_features["energy"])
                data_dict["instrumentalness"].append(audio_features["instrumentalness"])
                data_dict["liveness"].append(audio_features["liveness"])
                data_dict["loudness"].append(audio_features["loudness"])
                data_dict["mode"].append(audio_features["mode"])
                data_dict["speechiness"].append(audio_features["speechiness"])
                data_dict["tempo"].append(audio_features["tempo"])
                data_dict["valence"].append(audio_features["valence"])
        
        self.df = pd.DataFrame(data_dict)
        return self.df
        """
        for t in data_dict:
            print(t, data_dict[t])
        """