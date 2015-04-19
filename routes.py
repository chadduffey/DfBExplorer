from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager, Shell
from flask.ext.moment import Moment
from flask.ext.mail import Mail  
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
import os

#--------------------------------------------------------------
# SETUP
#--------------------------------------------------------------
#general
app = Flask(__name__)
app.config['SECRET_KEY'] = '1testingOnly2'

#database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

#css
bootstrap = Bootstrap(app)

#time
moment = Moment(app)

#manager
manager = Manager(app)

#sql migrate
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

#mail
mail = Mail(app)
app.config['MAIL_SERVER'] = 'email-smtp.us-west-2.amazonaws.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
#app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
#--------------------------------------------------------------

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))

class NameForm(Form):
	name = StringField('Username:', validators=[Required()])
	submit = SubmitField('Submit')

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), unique=True)

	def __repr__(self):
		return '<Role %r>' % self.name

	users = db.relationship('User', backref='role', lazy='dynamic')

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)

	def __repr__(self):
		return '<User %r>' % self.username

	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

@app.route('/', methods=['GET', 'POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username = form.name.data)
			db.session.add(user)
			session['known'] = False
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html', form=form, name=session.get('name'), 
		current_time=datetime.utcnow(), known = session.get('known', False))

#@app.route('/user/<name>')
#def user(name):
#	return render_template('index.html', name=session.get('name'), current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500

if __name__ == '__main__':
	manager.run()
	app.run(debug=True)