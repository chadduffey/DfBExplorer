from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment 
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required 

app = Flask(__name__)
app.config['SECRET_KEY'] = '1testingOnly2'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(Form):
	name = StringField('Username:', validators=[Required()])
	submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
	name = None
	form = NameForm()
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
	return render_template('index.html', form=form, name=name, current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
	return render_template('index.html', name=name, current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500

if __name__ == '__main__':
	app.run(debug=True)