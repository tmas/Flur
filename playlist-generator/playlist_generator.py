import pymysql.cursors
from peewee import *
import MySQLdb
#initialize data from front end
genre = ""
length = 0.0

sql = "SELECT * FROM  WHERE 'genre'= %s" % \ (genre)
