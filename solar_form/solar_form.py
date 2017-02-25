from flask_restful import Resource, Api
import os
import sqlite3
from flask import Flask, request, session, g, abort, jsonify, make_response

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

# Connects to database file specified in config
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row # uses namedtuple object
    return rv

# Open a new database connection if the current context doesn't have one
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# Initializes database using SQL schema provided in root directory
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

# Allows initialization of the databse through command line
@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

# Closes the database connection at the end of every request
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# Makes 404 error response return JSON
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# Conducts SQL query on current database
def query_db(query, args=(), one=False):
    # From SQLite 3 with Flask tutorial
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Serves index.html file to homepage get request
@app.route('/', methods=['GET'])
def show_form():
    return app.send_static_file('index.html')

# Commits post request form data to database
@app.route('/api/forms', methods=['POST'])
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

# Returns JSON data for each entry with 'age' matching age
def get_age(age):
    data = {}
    for entry in query_db("select * from entries where age='%s'"%age):
        data[entry['id']] = {'name': entry['name'], 'age': entry['age'], 'address': entry['address'],
            'city': entry['city'], 'state': entry['state'], 'zip': entry['zip'],
            'interest': entry['text']}
    return jsonify(data)

# Returns JSON data for each entry with 'city' matching city
def get_city(city):
    data = {}
    for entry in query_db("select * from entries where city='%s'"%city):
        data[entry['id']] = {'name': entry['name'], 'age': entry['age'], 'address': entry['address'],
            'city': entry['city'], 'state': entry['state'], 'zip': entry['zip'],
            'interest': entry['text']}
    return jsonify(data)

# Returns JSON data for each entry with 'state' matching state
def get_state(state):
    data = {}
    for entry in query_db("select * from entries where state='%s'"%state):
        data[entry['id']] = {'name': entry['name'], 'age': entry['age'], 'address': entry['address'],
            'city': entry['city'], 'state': entry['state'], 'zip': entry['zip'],
            'interest': entry['text']}
    return jsonify(data)

# Returns JSON data for each entry with 'zip' matching zipcode
def get_zip(zipcode):
    data = {}
    for entry in query_db("select * from entries where zip='%s'"%zipcode):
        data[entry['id']] = {'name': entry['name'], 'age': entry['age'], 'address': entry['address'],
            'city': entry['city'], 'state': entry['state'], 'zip': entry['zip'],
            'interest': entry['text']}
    return jsonify(data)

# Returns JSON data for count of entries
class Responses_Count(Resource):
    def get(self):
        entry = query_db('select count(*) from entries')
        return jsonify(entry[0][0])

# Returns JSON data, route to sorting request based on args
class Responses(Resource):
    def get(self):
        age = request.args.get('age') # if age sort requested
        if age is not None:
            return get_age(age)
        city = request.args.get('city') # if city sort requested
        if city is not None:
            return get_city(city)
        state = request.args.get('state') # etc
        if state is not None:
            return get_state(state)
        zipcode = request.args.get('zip')
        if zipcode is not None:
            return get_zip(zipcode)
        data = {}
        for entry in query_db('select * from entries'):
            data[entry['id']] = {'name': entry['name'], 'age': entry['age'], 'address': entry['address'],
                'city': entry['city'], 'state': entry['state'], 'zip': entry['zip'],
                'interest': entry['text']}
        return jsonify(data)

# Deletes entry from database with 'id' matching entry_id
class Response(Resource):
    def delete(self, entry_id):
        db = get_db()
        db.execute("delete from entries where id=%d"%entry_id)
        db.commit()
        return jsonify({'result': True})

api.add_resource(Responses, '/api/forms')
api.add_resource(Responses_Count, '/api/forms/count')
api.add_resource(Response, '/api/forms/<int:entry_id>')

if __name__ == '__main__':
     app.run()
