from flask import Flask, render_template, request, redirect, session
import json, os

app = Flask(__name__)
app.secret_key = "secret123"

ADMIN_PASSWORD = "nitin"

def load_movies():
    try:
        with open("movies.json") as f:
            return json.load(f)
    except:
        return []

def save_movies(data):
    with open("movies.json", "w") as f:
        json.dump(data, f, indent=4)

# HOME + SEARCH
@app.route("/")
def home():
    query = request.args.get("q", "")
    movies = load_movies()

    if query:
        movies = [m for m in movies if query.lower() in m["name"].lower()]

    return render_template("index.html", movies=movies, total=len(movies), query=query)

# ADMIN LOGIN
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin"):
        if request.method == "POST":
            if request.form["password"] == ADMIN_PASSWORD:
                session["admin"] = True
                return redirect("/admin")
        return '''
        <div style="text-align:center;margin-top:100px;">
        <h2>🔐 Admin Login</h2>
        <form method="post">
        <input type="password" name="password" placeholder="Password"><br><br>
        <button>Login</button>
        </form></div>
        '''

    movies = load_movies()
    return render_template("admin.html", movies=movies, total=len(movies))

# ADD
@app.route("/add", methods=["POST"])
def add():
    movies = load_movies()

    movies.append({
        "id": len(movies),
        "name": request.form["name"],
        "poster": request.form["poster"],
        "link_720": request.form["link_720"],
        "link_1080": request.form["link_1080"]
    })

    save_movies(movies)
    return redirect("/admin")

# DELETE
@app.route("/delete/<int:id>")
def delete(id):
    movies = load_movies()
    movies = [m for m in movies if m["id"] != id]
    save_movies(movies)
    return redirect("/admin")

# EDIT PAGE
@app.route("/edit/<int:id>")
def edit(id):
    movies = load_movies()
    movie = next((m for m in movies if m["id"] == id), None)
    return render_template("edit.html", movie=movie)

# UPDATE
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    movies = load_movies()

    for m in movies:
        if m["id"] == id:
            m["name"] = request.form["name"]
            m["poster"] = request.form["poster"]
            m["link_720"] = request.form["link_720"]
            m["link_1080"] = request.form["link_1080"]

    save_movies(movies)
    return redirect("/admin")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
