from flask import Flask, render_template, request, redirect, session
import psycopg2, os

app = Flask(__name__)
app.secret_key = "nitin_movie_site_secret_2026_super_secure_key_123"

ADMIN_PASS = "nitin000001"

DATABASE_URL = os.environ.get("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS movies (
id SERIAL PRIMARY KEY,
name TEXT,
poster TEXT,
link_480 TEXT,
size_480 TEXT,
link_720 TEXT,
size_720 TEXT,
link_1080 TEXT,
size_1080 TEXT
)
""")
conn.commit()

def get_movies():
    cur.execute("SELECT * FROM movies ORDER BY id DESC")
    rows = cur.fetchall()
    movies = []
    for r in rows:
        movies.append({
            "id": r[0],
            "name": r[1],
            "poster": r[2],
            "link_480": r[3],
            "size_480": r[4],
            "link_720": r[5],
            "size_720": r[6],
            "link_1080": r[7],
            "size_1080": r[8]
        })
    return movies

@app.route("/")
def home():
    q = request.args.get("q","").lower()
    movies = get_movies()

    if q:
        movies = [m for m in movies if q in m["name"].lower()]

    return render_template("index.html", movies=movies, total=len(movies))

@app.route("/movie/<int:id>")
def movie(id):
    cur.execute("SELECT * FROM movies WHERE id=%s",(id,))
    r = cur.fetchone()

    m = {
        "id": r[0],
        "name": r[1],
        "poster": r[2],
        "link_480": r[3],
        "size_480": r[4],
        "link_720": r[5],
        "size_720": r[6],
        "link_1080": r[7],
        "size_1080": r[8]
    }

    return render_template("movie.html", m=m)

@app.route("/admin", methods=["GET","POST"])
def admin():
    if not session.get("admin"):
        if request.method == "POST" and request.form["password"] == ADMIN_PASS:
            session["admin"] = True
            return redirect("/admin")
        return "<form method='post'><input type='password' name='password'><button>Login</button></form>"

    movies = get_movies()
    return render_template("admin.html", movies=movies, total=len(movies))

@app.route("/add", methods=["POST"])
def add():
    cur.execute("""
    INSERT INTO movies (name,poster,link_480,size_480,link_720,size_720,link_1080,size_1080)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """,(
        request.form["name"],
        request.form["poster"],
        request.form["link_480"],
        request.form["size_480"],
        request.form["link_720"],
        request.form["size_720"],
        request.form["link_1080"],
        request.form["size_1080"]
    ))
    conn.commit()
    return redirect("/admin")

@app.route("/delete/<int:id>")
def delete(id):
    cur.execute("DELETE FROM movies WHERE id=%s",(id,))
    conn.commit()
    return redirect("/admin")

@app.route("/edit/<int:id>")
def edit(id):
    cur.execute("SELECT * FROM movies WHERE id=%s",(id,))
    r = cur.fetchone()

    movie = {
        "id": r[0],
        "name": r[1],
        "poster": r[2],
        "link_480": r[3],
        "size_480": r[4],
        "link_720": r[5],
        "size_720": r[6],
        "link_1080": r[7],
        "size_1080": r[8]
    }

    return render_template("edit.html", movie=movie)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    cur.execute("""
    UPDATE movies SET
    name=%s,
    poster=%s,
    link_480=%s,
    size_480=%s,
    link_720=%s,
    size_720=%s,
    link_1080=%s,
    size_1080=%s
    WHERE id=%s
    """,(
        request.form["name"],
        request.form["poster"],
        request.form["link_480"],
        request.form["size_480"],
        request.form["link_720"],
        request.form["size_720"],
        request.form["link_1080"],
        request.form["size_1080"],
        id
    ))
    conn.commit()
    return redirect("/admin")
