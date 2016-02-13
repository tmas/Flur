import spotipy
from peewee import *
import pymysql.cursors
import time
import sys
spotify = spotipy.Spotify()
artistGenres = {}
start = 0
end = 0
update = 50
delay = 5
if(len(sys.argv)==3):
    start=int(sys.argv[1])
    end = int(sys.argv[2])
    update = 50
    delay = 5
elif(len(sys.argv)==4):
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    update = int(sys.argv[3])
    delay = 5
elif(len(sys.argv)==5):
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    update = int(sys.argv[3])
    delay = int(sys.argv[4])
else:
    print("Invalid number of arguments. Please try again.")
current = start
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
start_time = time.time();
while (current < end):
    results = spotify.search(q='track:' + '', limit=update, offset=current, type='track')
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
        if not artistGenres[track['artists'][0]['id']] == '';
            songtest = Song(name=track['name'],artists=artists,album=track['album']['name'],popularity=track['popularity'],duration=track['duration_ms'],genres=artistGenres[track['artists'][0]['id']],url=track['external_urls']['spotify'])
            songtest.save();
            print("saved song with artistGenres: ", artistGenres)
        else:
            print("didn't save song with artistGenres: ", artistGenres)
    current += update
    print("Appended ", update, "songs!")
    time.sleep(delay)
print("Appended ", current - start, "songs! That's # ", current, ", going at ", float(current - start)/(time.time() - start_time), " songs per second!")
