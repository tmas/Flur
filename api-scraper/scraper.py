import spotipy
from peewee import *
import pymysql.cursors
spotify = spotipy.Spotify()
songs = []
artistGenres = {}

db = pymysql.connect(host="162.243.5.44",user="root",password="M1ddl30ut!",db="flur",charset="utf8mb4_bin",cursorclass=pymysql.cursors.DictCursor)
class Song(Model):
    name=CharField()
    artists=CharField()
    album=CharField()
    popularity=SmallIntegerField()
    duration=BigIntegerField()
    genres=CharField()
    url=CharField()

    class Meta:
        database = db

results = spotify.search(q='track:' + '', limit=1, offset=0, type='track')
tracks = results['tracks']
items = tracks['items']
for track in items:
    artists = ""
    for artist in track['artists']:
        artists += artist['name'] + " && "
    artists = artists.rstrip(" && ")
    if (not artistGenres.has_key(track['artists'][0]['id'])):
        artistResult = spotify.artist(track['artists'][0]['uri'])
        artistGenres[track['artists'][0]['id']] = ""
        for genre in artistResult['genres']:
            artistGenres[track['artists'][0]['id']] += genre + ", "
        artistGenres[track['artists'][0]['id']] = artistGenres[track['artists'][0]['id']].rstrip(", ")
    songs.append({'name': track['name'], 'artists': artists, 'album': track['album']['name'], 'popularity': track['popularity'], 'duration': track['duration_ms'], 'genres': artistGenres[track['artists'][0]['id']], 'url': track['external_urls']['spotify']})
for song in songs:
    print(song['name'])
    print(song['genres'])
    print("\n")
