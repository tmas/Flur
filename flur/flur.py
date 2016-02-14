import pymysql.cursors
from peewee import *
import sys
import random
#initialize data from front end
genre = "rock"
desired_length = 1.0
length = 0
playlist = []
ids = []
if(len(sys.argv)==2):
    genre=sys.argv[1]
elif(len(sys.argv)==3):
    genre=sys.argv[1]
    desired_length=float(sys.argv[2])
else:
    print("Invalid number of arguments. Please try again.")

desired_length = int(desired_length * 3600000);
db = pymysql.connect(host="localhost", user="flur", password="KirklandSignature", db="flur", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)

sql = "SELECT * FROM song WHERE INSTR(genres, %s) AND popularity >= 50"

cursor = db.cursor()

cursor.execute(sql, genre)

data = cursor.fetchall()

while (length < desired_length):
    rnd = random.randint(0, len(data))
    if not data[rnd]['url'] in playlist:
        playlist.append(data[rnd]['url'])
        getURL(data[rnd]['url]
        length += data[rnd]['duration']
print("Songs: ", playlist);
print("Duration: ", float(length)/3600000)
db.close()


def getURL(url)
{
    identification = url[31:]
    ids.append(identification)
}