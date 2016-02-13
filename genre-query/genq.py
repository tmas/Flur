import spotipy
from peewee import *
import pymysql.cursors
import time
import sys
spotify = spotipy.Spotify()
db = MySQLDatabase(host="localhost",user="flur",password="KirklandSignature",database="flur",charset="utf8mb4",cursorclass=pymysql.cursors.DictCursor)
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
#for track in Song.select().where(Song.genres.contains("rock")):
#    print(track.name, " is a rock song! Genres: ", track.genres)
print(Song.select().where(Song.generes.contains("rock")))
