SolarCity Coding Challenge:
============================

Problem
-------
The task was to create a web service allowing users to indicate interest in
solar panels. It accepts a customer's name age, address, and why they're
interested in solar panels. It should save this data in a database.

Solution
--------
The solution is a web app built using a React.JS front-end and a Flask (Python)
back-end. The database is queried using SQL, and serviced through Flask using
sqlite3.

Facebook Incubator's create-react-app package (available on GitHub) was used to
develop the front-end and to build the final optimized .css and .js files
hosted on the server. The original, non-optimized App.js and other files are
located in /static/originals.

The sqlite3 database is stored locally, which provides faster queries than
remote or distributed for small scale web apps like this one-- even with
thousands of submissions, the database would not put too much memory load on a
single modern computer. The trade-off for this choice comes down to ease of
transferring the hosting of the app between computers-- because the database
isn't hosted remotely, the file would need to be physically copied to a new
computer. The database data, however, can still be accessed remotely through the
external API I've written.

Boilerplate code was not used, but the database connection functions in
solar_form.py are very standard and do not contain original code: init_db,
get_db, query_db, close_db.

My Level of Experience
----------------------
Before this challenge, I'd never done any front-end or back-end web development.
I had a good deal of experience in Python, but none in Flask or React/JavaScript
(so I learned them both in the process, as well as general networking
knowledge).

Type/Track
----------
**FULL-STACK**:
This app is relatively evenly divided between front-end and back end-- I spent
a good deal of time polishing the React scripts/formatting. The ReactJS
app handles incomplete submissions in advance of the server and highlights
incomplete fields.

The back-end initializes connections with the SQL database, commits POST request
data to the database, and provides a RESTful API in JSON using the flask_restful
library to fetch data from the database.

REST API Commands:
-------------
* /api/forms: Returns all submissions as JSON data
* /api/forms/count: Returns the count of all submissions
* /api/forms?column=x: Returns all entries where column (a SQL column)=x
* /api/delete/\<int:entry_id\>: Deletes an entry from the database with id matching entry_id

Local Installation Instructions
-------------------------------

**This app can be launched from any Mac or Linux computer**

1. Clone the repository

2. **In terminal at home folder:**

  * pip install flask

  * pip install flask_restful

3. **cd into the repository root directory**

  * pip install --editable .

  * export FLASK_APP=solar_form
  * export FLASK_DEBUG=True (if not planning to host publicly)

  * to initialize the database (clears existing one):
    * flask initdb

  * to run the server on a local port:
    * flask run
  * to run an externally visible server:
    * flask run --host=0.0.0.0
