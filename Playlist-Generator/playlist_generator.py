import pymysql.cursors
from peewee import *
import MySQLdb
#initialize data from front end
genre = ""
length = 0.0

db = MySQLdb.connect("localhost", "flur", "KirklandSignature", "flur")

sql = "SELECT * FROM flur WHERE 'genre'= %s" % (genre)

cursor = db.cursor()

cursor.execute(sql)

data = cursor.fetchone()

print(data)
