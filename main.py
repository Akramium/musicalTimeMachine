import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

URL = "https://www.billboard.com/charts/hot-100/"

date_input = input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DAY: ")
response = requests.get(url=f"{URL}{date_input}")
billboard_web_page = response.text

soup = BeautifulSoup(billboard_web_page, 'html.parser')
songs_tags = soup.find_all(name="span", class_="chart-element__information__song")
songs_titles = [song.get_text() for song in songs_tags]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user().get("id")
print(user_id)
song_uris = []
year = date_input.split("-")[0]
for song in songs_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date_input} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
