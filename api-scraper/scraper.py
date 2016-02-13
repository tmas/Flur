import spotipy
from peewee import *
import pymysql.cursors
import time
spotify = spotipy.Spotify()
artistGenres = {}
n = 0

db = MySQLDatabase(host="localhost",user="root",password="M1ddl30ut!",database="flur",charset="utf8mb4",cursorclass=pymysql.cursors.DictCursor)
class Song(Model):
    name=CharField()
    artists=CharField()
    album=CharField()
    popularity=IntegerField()
    duration=BigIntegerField()
    genres=CharField()
    url=CharField()

    class Meta:
        database = db
#Song.create_table(True);
while (n < 250):
    results = spotify.search(q='track:' + '', limit=50, offset=n, type='track')
    tracks = results['tracks']
    items = tracks['items']
    for track in items:
        artists = ""
        for artist in track['artists']:
            artists += artist['name'] + " && "
        artists = artists.rstrip(" && ")
        if (not track['artists'][0]['id'] in artistGenres):
            artistResult = spotify.artist(track['artists'][0]['uri'])
            artistGenres[track['artists'][0]['id']] = ""
            for genre in artistResult['genres']:
                artistGenres[track['artists'][0]['id']] += genre + ", "
            artistGenres[track['artists'][0]['id']] = artistGenres[track['artists'][0]['id']].rstrip(", ")
        songtest = Song(name=track['name'],artists=artists,album=track['album']['name'],popularity=track['popularity'],duration=track['duration_ms'],genres=artistGenres[track['artists'][0]['id']],url=track['external_urls']['spotify'])
        print("Appended ", songtest.save(), "songs!")
    n += 50
    time.sleep(5)
