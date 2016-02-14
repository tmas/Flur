import spotipy
from peewee import *
import pymysql.cursors
import time
import sys
import pygn
clientID="1695637605-13D16BA47C77E34A73018ADC06BC3E36"
userID="26272556248669065-86D2A24F94C0BE016245F5E28DBD28C6"
spotify = spotipy.Spotify()
artistGenres = {}
start = 0
end = 0
update = 50
delay = 5

def gnGenre(track):
    genres=""
    result = pygn.search(clientID=clientID, userID=userID, album=track['album']['name'], track=track['name'])
    for gen in result['genre']:
        genres += result['genre'][gen]['TEXT']
        genres += ", "
    genres = genres.rstrip(", ");
    return genres

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
class BetterSong(Model):
    name=CharField()
    artists=CharField()
    album=CharField()
    popularity=IntegerField()
    duration=BigIntegerField()
    genres=CharField()
    url=CharField()

    class Meta:
        database = db
BetterSong.create_table(True);
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
            if artistGenres[track['artists'][0]['id']] == '':
                artistGenres[track['artists'][0]['id']] = gnGenre(track)
        if not artistGenres[track['artists'][0]['id']] == '':
            songtest = BetterSong(name=track['name'],artists=artists,album=track['album']['name'],popularity=track['popularity'],duration=track['duration_ms'],genres=artistGenres[track['artists'][0]['id']],url=track['external_urls']['spotify'])
            songtest.save();
            print("saved song with artistGenres: ", artistGenres[track['artists'][0]['id']])
        #else:
            #print("didn't save song with artistGenres: ", artistGenres[track['artists'][0]['id']])
    current += update
    print("Processed ", update, "songs!")
    time.sleep(delay)
print("Processed ", current - start, "songs! That's # ", current, ", going at ", float(current - start)/(time.time() - start_time), " songs per second!")
