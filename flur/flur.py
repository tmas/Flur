from flask import Flask, render_template

flur = Flask(__name__)

@flur.route('/')
def index():
	return render_template('index.html')
	
#@flur.route('/')
#def playlist():
#	return render_template('playlist.html')
	
@flur.route('/generate')
def generate():	
	duration = request.form['duration']
	genre = request.form['genre']
	return render_template('playlist.html', duration, genre)
	
	
	
if __name__== '__main__':
	flur.run(debug=True)