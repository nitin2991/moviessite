from flask import Flask, render_template, request, redirect, session
import json
import os
app = Flask(__name__)
app.secret_key = "nitin_secret_2026"

ADMIN_PASS = "nitin000001"

def load_movies():
    try:
        with open("movies.json","r") as f:
            return json.load(f)
    except:
        return []

def save_movies(data):
    with open("movies.json","w") as f:
        json.dump(data,f,indent=4)

# HOME + SEARCH
@app.route("/")
def home():
    q = request.args.get("q")
    movies = load_movies()

    if q:
        movies = [m for m in movies if q.lower() in m["name"].lower()]

    return render_template("index.html", movies=movies, query=q)

# MOVIE PAGE
@app.route("/movie/<int:id>")
def movie(id):
    movies = load_movies()
    return render_template("movie.html", movie=movies[id])

# ADMIN LOGIN SAME PAGE
@app.route("/admin", methods=["GET","POST"])
def admin():

    if not session.get("admin"):
        if request.method == "POST":
            if request.form["password"] == ADMIN_PASS:
                session["admin"] = True
                return redirect("/admin")

        return '''
        <html>
        <style>
        body{background:#020c1b;display:flex;justify-content:center;align-items:center;height:100vh}
        .box{background:#111827;padding:30px;border-radius:15px;color:white;text-align:center}
        input{padding:10px;border-radius:10px;border:none}
        button{padding:10px 20px;background:#7b2ff7;color:white;border:none;border-radius:10px}
        </style>
        <div class="box">
        <h2>🔐 Admin Login</h2>
        <form method="post">
        <input type="password" name="password"><br><br>
        <button>Login</button>
        </form>
        </div>
        </html>
        '''

    movies = load_movies()

    if request.method == "POST":
        movies.append({
            "name": request.form["name"],
            "poster": request.form["poster"],
            "link480": request.form["link480"],
            "link720": request.form["link720"],
            "link1080": request.form["link1080"]
        })
        save_movies(movies)
        return redirect("/admin")

    return render_template("admin.html", movies=movies)

# DELETE
@app.route("/delete/<int:id>")
def delete(id):
    movies = load_movies()
    movies.pop(id)
    save_movies(movies)
    return redirect("/admin")

# EDIT
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):
    movies = load_movies()

    if request.method == "POST":
        movies[id]["name"] = request.form["name"]
        movies[id]["poster"] = request.form["poster"]
        movies[id]["link480"] = request.form["link480"]
        movies[id]["link720"] = request.form["link720"]
        movies[id]["link1080"] = request.form["link1080"]

        save_movies(movies)
        return redirect("/admin")

    return render_template("edit.html", movie=movies[id], id=id)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
