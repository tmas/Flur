import pymysql.cursors
from peewee import *
#initialize data from front end
genre = "rock"
length = 0.0

db = pymysql.connect(host="localhost", user="flur", password="KirklandSignature", db="flur", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)

sql = "SELECT * FROM flur WHERE 'genre' CONTAINS %s" % (genre)

cursor = db.cursor()

cursor.execute(sql)

data = cursor.fetchone()

print(data)

db.close()
