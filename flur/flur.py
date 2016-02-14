from flask import Flask, render_template, request, redirect
import pymysql.cursors
from peewee import *
import sys
import random


flur = Flask(__name__)
flur.jinja_env.add_extension('jinja2.ext.do')




def safePlaytime(artstplytm, artist):
	if artist in artstplytm.keys():
		return artstplytm[artist]
	else:
		return 0

	#returns ids of all the songs
def getPlaylist(duration, g, solubility=0.4):
	genre = g
	desired_length = duration
	length = 0
	playlist = []
	artistplaytime = {}
	desired_length = int(float(desired_length) * 3600000);
	db = pymysql.connect(host="localhost", user="flur", password="KirklandSignature", db="flur", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)

	sql = "SELECT * FROM song WHERE INSTR(genres, %s) AND popularity >= 50"

	cursor = db.cursor()

	cursor.execute(sql, genre)

	data = cursor.fetchall()

	while (length < desired_length):
		rnd = random.randint(0, len(data)-1)
		if (not data[rnd]['url'] in playlist) and ((float(safePlaytime(artistplaytime, data[rnd]['artists']) + data[rnd]['duration']) / float(duration)) < solubility):
			playlist.append(data[rnd]['url'])
			#print(data[rnd]['name'])
			#identification = url[31:]
			#ids.append(identification)
			length += data[rnd]['duration']
			artistplaytime[data[rnd]['artists']] += data[rnd]['duration']
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
	list_of_ids = getPlaylist(duration, genre)
	source = "https://embed.spotify.com/?uri=spotify:trackset:Flur:"
	for song in list_of_ids:
		source = source + song[31:] + ","
	source = source.rstrip(",")
	#method call?
	ids = []
	identification=""
	return render_template('playlist.html', genre=genre, source=source)


if __name__== '__main__':
	flur.run(debug=True,host="162.243.5.44",port=80)
