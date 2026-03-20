from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

def load_movies():
    try:
        with open("movies.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_movies(data):
    with open("movies.json", "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    movies = load_movies()
    return render_template("index.html", movies=movies[::-1])

@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        movies = load_movies()
        new_movie = {
            "title": request.form["title"],
            "image": request.form["image"],
            "link1080": request.form["link1080"],
            "link720": request.form["link720"]
        }
        movies.append(new_movie)
        save_movies(movies)

    return render_template("admin.html")