import spotipy
from peewee import *
import pymysql.cursors
import time
import sys
spotify = spotipy.Spotify()
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
for track in Song.select().where("rock" in Song.genres):
    print(Song.name, " is a rock song! Genres: ", genres)
