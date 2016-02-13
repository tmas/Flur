import spotipy
from peewee import *
import pymysql.cursors
import time
import sys
spotify = spotipy.Spotify()
artistGenres = {}
current = 0
end = 0
update = 50
delay = 5
if(len(sys.argv)==3):
    current=sys.argv[1]
    end = sys.argv[2]
    update = 50
    delay = 5
elif(len(sys.argv)==4):
    current = sys.argv[1]
    end = sys.argv[2]
    update = sys.argv[3]
    delay = 5
elif(len(sys.argv)==5):
    current = sys.argv[1]
    end = sys.argv[2]
    update = sys.argv[3]
    delay = sys.argv[4]
else:
    print("Invalid number of arguments. Please try again.")

print("before databse connection")
db = MySQLDatabase(host="localhost",user="root",password="M1ddl30ut!",database="flur",charset="utf8mb4",cursorclass=pymysql.cursors.DictCursor)
print("after database connection")
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
print("after class creation")
#Song.create_table(True);
while (current < end):
    print("at beginning of loop!")
    results = spotify.search(q='track:' + '', limit=end, offset=current, type='track')
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
    current += update
    time.sleep(delay)
