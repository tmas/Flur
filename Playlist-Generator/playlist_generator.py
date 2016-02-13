import pymysql.cursors
from peewee import *
import MySQLdb
#initialize data from front end
genre = ""
length = 0.0

db = MySQLdb.connect("localhost", "testuser", "test123", "flur")

sql = "SELECT * FROM  WHERE 'genre'= %s" % (genre)

cursor = db.cursor()

cursor.execute(sql)

data = cursor.fetchone()

print(data)
