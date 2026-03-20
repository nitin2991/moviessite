from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "nitin_movie_site_secret_2026_super_secure_key_123"

ADMIN_PASS = "nitin000001"  # change

movies = []

# HOME + SEARCH
@app.route("/")
def home():
    q = request.args.get("q", "").lower()
    filtered = [m for m in movies if q in m["name"].lower()] if q else movies
    return render_template("index.html", movies=filtered, total=len(filtered), query=q)

# DETAIL PAGE
@app.route("/movie/<int:id>")
def movie(id):
    if id < 0 or id >= len(movies):
        return redirect("/")
    return render_template("movie.html", m=movies[id])

# ADMIN (PASSWORD)
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin"):
        if request.method == "POST" and request.form.get("password") == ADMIN_PASS:
            session["admin"] = True
            return redirect("/admin")
        return '''
        <div style="text-align:center;margin-top:100px;color:white;background:#0b1220;height:100vh">
            <h2>🔐 Admin Login</h2>
            <form method="post">
                <input type="password" name="password" placeholder="Password" style="padding:10px;border-radius:10px"><br><br>
                <button style="padding:10px 20px;border-radius:10px;background:#6a5cff;color:white;border:none">Login</button>
            </form>
        </div>
        '''

    return render_template("admin.html", movies=movies, total=len(movies))

# ADD
@app.route("/add", methods=["POST"])
def add():
    movies.append({
        "id": len(movies),
        "name": request.form["name"],
        "poster": request.form["poster"],
        "link_480": request.form["link_480"],
        "size_480": request.form["size_480"],
        "link_720": request.form["link_720"],
        "size_720": request.form["size_720"],
        "link_1080": request.form["link_1080"],
        "size_1080": request.form["size_1080"]
    })
    return redirect("/admin")

# DELETE
@app.route("/delete/<int:id>")
def delete(id):
    global movies
    movies = [m for m in movies if m["id"] != id]
    # reindex
    for i, m in enumerate(movies):
        m["id"] = i
    return redirect("/admin")

# EDIT PAGE (inline simple)
@app.route("/edit/<int:id>")
def edit(id):
    m = next((x for x in movies if x["id"] == id), None)
    if not m:
        return redirect("/admin")
    return f'''
    <body style="background:#0b1220;color:white;font-family:sans-serif;text-align:center">
    <h2>Edit Movie</h2>
    <form method="post" action="/update/{id}">
    <input name="name" value="{m['name']}"><br>
    <input name="poster" value="{m['poster']}"><br>
    <input name="link_480" value="{m['link_480']}">
    <input name="size_480" value="{m['size_480']}"><br>
    <input name="link_720" value="{m['link_720']}">
    <input name="size_720" value="{m['size_720']}"><br>
    <input name="link_1080" value="{m['link_1080']}">
    <input name="size_1080" value="{m['size_1080']}"><br><br>
    <button>Update</button>
    </form>
    </body>
    '''

# UPDATE
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    for m in movies:
        if m["id"] == id:
            m["name"] = request.form["name"]
            m["poster"] = request.form["poster"]
            m["link_480"] = request.form["link_480"]
            m["size_480"] = request.form["size_480"]
            m["link_720"] = request.form["link_720"]
            m["size_720"] = request.form["size_720"]
            m["link_1080"] = request.form["link_1080"]
            m["size_1080"] = request.form["size_1080"]
    return redirect("/admin")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
