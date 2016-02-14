from flask import Flask, render_template, request, redirect
import pymysql.cursors
from peewee import *
import sys
import random
from string import Template

flur = Flask(__name__)
flur.jinja_env.add_extension('jinja2.ext.do')


	#returns ids of all the songs
def getPlaylist(duration, g, ng):
	genre = g
	desired_length = duration
	notgenre = ng
	if not notgenre == "":
		notgenre = "%"+ng+"%"
	length = 0
	playlist = []
	desired_length = int(float(desired_length) * 3600000);
	db = pymysql.connect(host="localhost", user="flur", password="KirklandSignature", db="flur", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
	#print("connected to database")
	s = Template("SELECT * FROM song WHERE INSTR(genres, '$genre') AND genres NOT LIKE '$notgenre' AND popularity >= 50 ORDER BY RAND()")
	sql = s.substitute(genre=genre, notgenre=notgenre)

	cursor = db.cursor()

	cursor.execute(sql)

	data = cursor.fetchall()
	print("got data")
	songsadded=0
	#while (length < desired_length):
	#	if (songsadded >= len(data)):
	#		break
	#	rnd = random.randint(0, len(data)-1)
	#	if not data[rnd]['url'] in playlist:
	#		playlist.append(data[rnd]['url'])
	#		#print(data[rnd]['name'])
	#		#identification = url[31:]
	#		#ids.append(identification)
	#		length += data[rnd]['duration']
	#		songsadded += 1
	for song in data:
		if length >= desired_length:
			break
		if not song['url'] in playlist:
			playlist.append(song['url'])
			length += song['duration']
	print("Songs: ", playlist);
	print("Duration: ", float(length)/3600000)
	db.close()
	return playlist

@flur.route('/')
def index():
	return render_template('index.html')

#@flur.route('/')
#def playlist():
#	return render_template('playlist.html')

@flur.route('/generate', methods = ['POST'])
def generate():
	duration = request.form['duration']
	genre = request.form['genre']
	notgenre = request.form['notgenre']
	list_of_ids = getPlaylist(duration, genre, notgenre)
	source = "https://embed.spotify.com/?uri=spotify:trackset:Flur:"
	for song in list_of_ids:
		source = source + song[31:] + ","
	source = source.rstrip(",")
	#method call?
	ids = []
	identification=""
	return render_template('playlist.html', genre=genre, notgenre=notgenre, source=source)


if __name__== '__main__':
	flur.run(debug=True,host="162.243.5.44",port=80)
