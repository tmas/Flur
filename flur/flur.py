from flask import Flask, render_template, request, redirect
import pymysql.cursors
from peewee import *
import sys
import random
from string import Template

flur = Flask(__name__)
flur.jinja_env.add_extension('jinja2.ext.do')




def safePlaytime(artstplytm, artist):
	if artist in artstplytm.keys():
		return artstplytm[artist]
	else:
		return 0

	#returns ids of all the songs
def getPlaylist(duration, g, pop_low, pop_up, ng, solubility=0.4, linkin):
	genre = g
	desired_length = duration
	notgenre = ng
	if not notgenre == "":
		notgenre = "%"+ng+"%"
	length = 0
	playlist = []
	artistplaytime = {}
	desired_length = int(float(desired_length) * 3600000);
	db = pymysql.connect(host="localhost", user="flur", password="KirklandSignature", db="flur", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
	s = Template("SELECT * FROM song WHERE INSTR(genres, '$genre') AND popularity >= '$pop_low' AND popularity <= '$pop_up' AND genres NOT LIKE '$notgenre' ORDER BY RAND()")
	sql = s.substitute(genre=genre, pop_low=pop_low, pop_up=pop_up, notgenre=notgenre)
	print(sql)

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
		if (not song['url'] in playlist) and ((float(safePlaytime(artistplaytime, song['artists']) + song['duration']) / float(desired_length)) < solubility):
			playlist.append(song['url'])
			length += song['duration']
			artistplaytime[song['artists']] = safePlaytime(artistplaytime, song['artists']) + song['duration']
	print("Songs: ", playlist);
	print("Duration: ", float(length)/3600000)
	db.close()
	return playlist

@flur.route('/')
def index():
	return render_template('index.html', genre="", source="", form=True)

#@flur.route('/')
#def playlist():
#	return render_template('playlist.html')

@flur.route('/generate', methods = ['POST'])
def generate():
	linkin = False
	pageType = request.form['page']
	if(pageType=="linkin"):
		duration = request.form['duration]
		linkin = True
		render_template('index.html', genre=genre, source=source, form=False, notgenre=notgenre)
		genre=""
		popularity_lower=0
		popularity_upper=0
		notgenre=""
		list_of_ids = getPlayList(duration, genre, popularity_lower, popularity_upper, notgenre, linkin)
	else:
		duration = request.form['duration']
		genre = request.form['genre']
		popularity_lower = request.form['popularity-lower']
		popularity_upper = request.form['popularity-upper']
		notgenre = request.form['notgenre']
		#exclusions = request.form['h8ers'].spl	itlines()
		list_of_ids = getPlaylist(duration, genre, popularity_lower, popularity_upper, notgenre linkin)
		source = "https://embed.spotify.com/?uri=spotify:trackset:Flur:"
		for song in list_of_ids:
			source = source + song[31:] + ","
		source = source.rstrip(",")
		#method call?
		ids = []
		identification=""
		return render_template('index.html', genre=genre, source=source, form=False, notgenre=notgenre)


if __name__== '__main__':
	flur.run(debug=True,host="162.243.5.44",port=80)
