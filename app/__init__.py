from flask          import Flask
from flask          import render_template
from flask          import redirect
from flask          import request
from libsql_client  import create_client_sync
from dotenv         import load_dotenv

import os


# Load Turso environment variables from the .env file
load_dotenv()
TURSO_URL = os.getenv("TURSO_URL")
TURSO_KEY = os.getenv("TURSO_KEY")


# Create the Flask app
app = Flask(__name__)


# Track the DB connection
client = None

#-----------------------------------------------------------
# Connect to the Turso DB and return the connection
#-----------------------------------------------------------
def connect_db():
    global client
    if client == None:
        client = create_client_sync(url=TURSO_URL, auth_token=TURSO_KEY)
    return client


#-----------------------------------------------------------
# Home Page with list of songs
#-----------------------------------------------------------
@app.get("/")
def home():
    client = connect_db()
    result = client.execute("SELECT id, title FROM list_of_songs")
    # print(result.rows)
    songs = result.rows
    return render_template("pages/home.jinja" , songs=songs)


#-----------------------------------------------------------
# Thing details page
#-----------------------------------------------------------
@app.get("/song/<int:id>")
def show_thing(id):
    client = connect_db()
    sql = "SELECT id, title, minutes FROM list_of_songs WHERE id=?"
    
    values =  [id]

    result = client.execute(sql , values)
    
    song = result.rows[0]

    return render_template("pages/thing.jinja" , song=song)


#-----------------------------------------------------------
# New thing form page
#-----------------------------------------------------------
@app.get("/new")
def new_thing():
    return render_template("pages/thing-form.jinja")

#=====================================
# Process A new song
#=====================================

@app.post("/add-thing")
def add_thing():
    title = request.form.get("title")
    minutes = request.form.get("minutes")
    artist = "me"

    print(title)
    print(minutes)
    print(artist)


    #connect to the datatbase
    client = connect_db()
    sql = "INSERT INTO list_of_songs (title, Artist, minutes) VALUES (?, ?, ?)"
    
    values =  [title, artist, minutes]

    client.execute(sql, values)

    return redirect("/")
#-----------------------------------------------------------
# Thing deletion
#-----------------------------------------------------------
@app.get("/delete/<int:id>")
def delete_thing(id):

    client = connect_db()

    sql = "DELETE FROM list_of_songs WHERE id=?"

    values=[id]

    client.execute(sql, values)


    return redirect("/")


#-----------------------------------------------------------
# 404 error handler
#-----------------------------------------------------------
@app.errorhandler(404)
def not_found(error):
    return render_template("pages/404.jinja")
