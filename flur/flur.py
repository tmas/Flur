from flask import Flask, render_template

flur = Flask(__name__)

@flur.route('/')
def index():
	return render_template('index.html')
	
def playlist():
	return render_template('playlist.html')
	
if __name__== '__main__':
	flur.run(debug=True)