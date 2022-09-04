from flask import Flask, render_template, request, redirect
from cs50 import SQL

app = Flask(__name__)

SPORTS = ["ski", "football", "surf"]

REGISTRANTS = {}

db = SQL("sqlite:///app.db")


@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)


@app.route("/register", methods=["POST"])
def register():

    # Validate name
    name = request.form.get("name")
    if not name:
        return render_template("status.html", message="Missing name")

    #Validate sport
    sport = request.form.get("sport")
    if not sport:
        return render_template("status.html", message="Missing sport")

    REGISTRANTS[name] = sport

    db.execute("INSERT INTO registrants (name, sport) VALUES(?, ?)", name, sport)

    return redirect("/registrants")


@app.route("/registrants")
def registrants():
    registrants = db.execute("SELECT * FROM registrants")
    return render_template("registrants.html", registrants=registrants)


@app.route("/deregister", methods=["POST"])
def deregister():

    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM registrants WHERE id = ?", id)
    return redirect("/registrants")