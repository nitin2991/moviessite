from flask import Flask, render_template, request, redirect, session
import psycopg2, os

app = Flask(__name__)
app.secret_key = "nitin_movie_site_secret_2026_super_secure_key_123"

ADMIN_PASS = "nitin000001"

DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS movies (
id SERIAL PRIMARY KEY,
name TEXT,
poster TEXT,
link480 TEXT,
size480 TEXT,
link720 TEXT,
size720 TEXT,
link1080 TEXT,
size1080 TEXT
)
""")
conn.commit()

def get_movies():
    cur.execute("SELECT * FROM movies ORDER BY id DESC")
    rows = cur.fetchall()
    return rows

# HOME
@app.route("/")
def home():
    return render_template("index.html", movies=get_movies())

# MOVIE PAGE
@app.route("/movie/<int:id>")
def movie(id):
    cur.execute("SELECT * FROM movies WHERE id=%s",(id,))
    m = cur.fetchone()
    return render_template("movie.html", m=m)

# ADMIN
@app.route("/admin", methods=["GET","POST"])
def admin():
    if not session.get("admin"):
        if request.method == "POST":
            if request.form["password"] == ADMIN_PASS:
                session["admin"] = True
                return redirect("/admin")

        return '''
        <style>
        body{background:#0b1220;color:white;display:flex;justify-content:center;align-items:center;height:100vh}
        .box{background:#111;padding:30px;border-radius:15px;text-align:center}
        input{padding:10px;border-radius:10px;border:none}
        button{padding:10px;background:#6a11cb;color:white;border:none;border-radius:10px}
        </style>
        <div class="box">
        <h2>Admin Login</h2>
        <form method="post">
        <input name="password" placeholder="Password"><br><br>
        <button>Enter</button>
        </form>
        </div>
        '''

    if request.method == "POST":
        cur.execute("""INSERT INTO movies 
        (name,poster,link480,size480,link720,size720,link1080,size1080)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
        (request.form["name"],request.form["poster"],
         request.form["link480"],request.form["size480"],
         request.form["link720"],request.form["size720"],
         request.form["link1080"],request.form["size1080"]))
        conn.commit()

    return render_template("admin.html", movies=get_movies())

# DELETE
@app.route("/delete/<int:id>")
def delete(id):
    cur.execute("DELETE FROM movies WHERE id=%s",(id,))
    conn.commit()
    return redirect("/admin")

# EDIT
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):
    if request.method == "POST":
        cur.execute("""UPDATE movies SET 
        name=%s,poster=%s,link480=%s,size480=%s,
        link720=%s,size720=%s,link1080=%s,size1080=%s
        WHERE id=%s""",
        (request.form["name"],request.form["poster"],
         request.form["link480"],request.form["size480"],
         request.form["link720"],request.form["size720"],
         request.form["link1080"],request.form["size1080"],id))
        conn.commit()
        return redirect("/admin")

    cur.execute("SELECT * FROM movies WHERE id=%s",(id,))
    m = cur.fetchone()
    return render_template("edit.html", m=m)

app.run(host="0.0.0.0", port=10000)
