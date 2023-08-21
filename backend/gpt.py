import openai
import spotify

def analyze_vibe(track_ids, spotify_interact):
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= [
                {"role": "user", "content":generate_prompt_for_top_n(track_ids, spotify_interact)},
                {"role": "system", "content": "do not give a vague answer and format your answers as an unordered list."}
            ]
        )
    #print(response)
    print("The response given:", response.choices[0].message.content)
    return response.choices[0].message.content

def generate_prompt_mood(audio_features, title, role):
    return f"""As a {role}, suggest my overall vibe and music preferences based 
            on these audio features of my favorite song, {title.capitalize()}:
            danceability: {audio_features["danceability"]},
            acousticness: {audio_features["acousticness"]},
            energy: {audio_features["energy"]},
            instrumentalness: {audio_features["instrumentalness"]},
            liveness: {audio_features["liveness"]},
            loudness: {audio_features["loudness"]},
            mode: {audio_features["mode"]},
            speechiness: {audio_features["speechiness"]},
            tempo: {audio_features["tempo"]},
            valence: {audio_features["valence"]}.
            """

def generate_prompt_for_top_n(track_ids, spotify_interact):
    prompt = f"""Based on the {len(track_ids)} songs and the corresponding audio features that I am listing below, 
            suggest my overall vibe and music preferences."""
    for i, id in enumerate(track_ids):
        prompt += f"{i + 1}. " + generate_description_for_one(id, spotify_interact)
    return prompt

def generate_description_for_one(track_id, spotify_interact):
    song = spotify_interact.get_track(track_id)
    title = song["name"]
    artist = song["artists"][0]["name"]
    audio_features = spotify_interact.getAudioFeatures(track_id)
    return f"""{title} by {artist} has following audio features:
            danceability: {audio_features["danceability"]},
            acousticness: {audio_features["acousticness"]},
            energy: {audio_features["energy"]},
            instrumentalness: {audio_features["instrumentalness"]},
            liveness: {audio_features["liveness"]},
            loudness: {audio_features["loudness"]},
            mode: {audio_features["mode"]},
            speechiness: {audio_features["speechiness"]},
            tempo: {audio_features["tempo"]},
            valence: {audio_features["valence"]}.
            """ 