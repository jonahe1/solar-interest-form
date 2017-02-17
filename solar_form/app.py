from flask_restful import Resource, Api
import os
import sqlite3
from flask import Flask, request, redirect, session, g, url_for, abort, flash

app = Flask(__name__, static_url_path='/static/')
app.config.from_object(__name__) # load config from this file , app.py
api = Api(app)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'app.db'),
    SECRET_KEY='development key',
    USERNAME='jonahe',
    PASSWORD='Sneakers123'
))
app.config.from_envvar('APP_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/', methods=['GET'])
def show_form():
    return app.send_static_file('index.html')

def valid_submit(form):
    if '' in form.values(): return False
    return True

@app.route('/', methods=['POST'])
def submit():
    name = request.form['yourname']
    age = request.form['yourage']
    address = request.form['youraddress']
    city = request.form['yourcity']
    state = request.form['yourstate']
    zipcode = request.form['yourzip']
    interest = request.form['yourinterest']
    if valid_submit(request.form):
        db = get_db()
        db.execute('insert into entries (name, age, address, city, state, zip, text) values (?, ?, ?, ?, ?, ?, ?)',
                 [name, age, address, city, state, zipcode, interest])
        db.commit()
        flash('New entry was successfully posted')
        return 'Submit successful'
    else:
        return 'Form incomplete'

class Responses_Count(Resource):
    def get(self):
        query = query_db('select count(*) from entries')
        return query

class Responses_Age(Resource):
    def get_age(self, age):
        query = query_db("select * from entries where age='%s'"%age)
        result = {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}
        return result

class Responses_City(Resource):
    def get_city(self, city):
        query = query_db("select * from entries where city='%s'"%city)
        result = {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}
        return result

class Responses_State(Resource):
    def get_state(self, state):
        query = query_db("select * from entries where state='%s'"%state)
        result = {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}
        return result

class Responses_ZIP(Resource):
    def get_zip(self, zipcode):
        query = query_db("select * from entries where zip='%s'"%zipcode)
        result = {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}
        return result

class Responses_All(Resource):
    def get_all(self):
        query = query_db('select * from entries')
        result = {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}
        return result

api.add_resource(Responses_Age, '/age/<string:age>')
api.add_resource(Responses_City, '/city/<string:city>')
api.add_resource(Responses_State, '/state/<string:state>')
api.add_resource(Responses_ZIP, '/zip/<string:zipcode>')
api.add_resource(Responses_All, '/all')
api.add_resource(Responses_Count, '/count')

if __name__ == '__main__':
     app.run()
