from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment 
import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def index():
	return render_template('index.html', current_time=datetime.datetime.utcnow())

@app.route('/user/<name>')
def user(name):
	return render_template('index.html', name=name, current_time=datetime.datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500

if __name__ == '__main__':
	app.run(debug=True)