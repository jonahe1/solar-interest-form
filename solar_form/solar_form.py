from flask_restful import Resource, Api
import os
import sqlite3
from flask import Flask, request, redirect, session, g, url_for, abort, flash, jsonify

app = Flask(__name__)
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
    # Connects to database file specified in config
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row # uses namedtuple object
    return rv

def get_db():
    # Open a new database connection if the current context doesn't have one
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    # Allows initialization of the databse through command line
    init_db()
    print('Initialized the database.')

@app.teardown_appcontext
def close_db(error):
    # Closes the database connection at the end of every request
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def query_db(query, args=(), one=False):
    # From SQLite 3 with Flask tutorial
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/', methods=['GET'])
def show_form():
    return app.send_static_file('index.html')

@app.route('/', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    zipcode = request.form['zip']
    interest = request.form['interest']
    db = get_db()
    db.execute('insert into entries (name, age, address, city, state, zip, text) values (?, ?, ?, ?, ?, ?, ?)',
                [name, age, address, city, state, zipcode, interest])
    db.commit()
    return 'SUCCESS'

class Responses_Count(Resource):
    def get(self):
        entry = query_db('select count(*) from entries')
        return entry[0][0]

class Responses_Age(Resource):
    def get(self, age):
        data = {}
        for entry in query_db("select * from entries where age='%s'"%age):
            data[entry['id']] = {'name': entry['name'], 'age': entry['age'], 'address': entry['address'],
                'city': entry['city'], 'state': entry['state'], 'zip': entry['zip'],
                'interest': entry['text']}
        return data

class Responses_City(Resource):
    def get(self, city):
        data = {}
        for entry in query_db("select * from entries where city='%s'"%city):
            data[entry['id']] = {'name': entry['name'], 'age': entry['age'], 'address': entry['address'],
                'city': entry['city'], 'state': entry['state'], 'zip': entry['zip'],
                'interest': entry['text']}
        return data

class Responses_State(Resource):
    def get(self, state):
        data = {}
        for entry in query_db("select * from entries where state='%s'"%state):
            data[entry['id']] = {'name': entry['name'], 'age': entry['age'], 'address': entry['address'],
                'city': entry['city'], 'state': entry['state'], 'zip': entry['zip'],
                'interest': entry['text']}
        return data

class Responses_ZIP(Resource):
    def get(self, zipcode):
        data = {}
        for entry in query_db("select * from entries where zip='%s'"%zipcode):
            data[entry['id']] = {'name': entry['name'], 'age': entry['age'], 'address': entry['address'],
                'city': entry['city'], 'state': entry['state'], 'zip': entry['zip'],
                'interest': entry['text']}
        return data

class Responses_All(Resource):
    def get(self):
        data = {}
        for entry in query_db('select * from entries'):
            data[entry['id']] = {'name': entry['name'], 'age': entry['age'], 'address': entry['address'],
                'city': entry['city'], 'state': entry['state'], 'zip': entry['zip'],
                'interest': entry['text']}
        return data

api.add_resource(Responses_Age, '/age/<string:age>')
api.add_resource(Responses_City, '/city/<string:city>')
api.add_resource(Responses_State, '/state/<string:state>')
api.add_resource(Responses_ZIP, '/zip/<string:zipcode>')
api.add_resource(Responses_All, '/all')
api.add_resource(Responses_Count, '/count')

if __name__ == '__main__':
     app.run()
