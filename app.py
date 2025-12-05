
from flask import Flask, request, render_template, session, redirect, make_response, jsonify
from functools import wraps
import os
import mysql.connector
from flask_restful import Resource, Api
from flask_jwt_extended import (
    create_access_token, jwt_required, verify_jwt_in_request,
    JWTManager, get_jwt_identity, get_jwt, set_access_cookies
)

app = Flask(__name__)
app.secret_key = "secretkey"

app.config["JWT_SECRET_KEY"] = "secretkey"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
jwt = JWTManager(app)

app.config["UPLOADED_PHOTOS_DEST"] = "static"
#Connect to MySQL
cnx = mysql.connector.connect(
    user='root',
    password='MyPassword',
    host='127.0.0.1',
    database='Movies',
    auth_plugin='mysql_native_password'
)

movies = [
    {
        "id": 0,
        "title": "Doctor Strange in the Multiverse of Madness",
        "year": 2022,
        "director": "Sam Raimi",
        "writters": "Jade Halley Bartlett, Steve Ditko, Stan Lee",
        "stars": "Benedict Cumberbatch, Elizabeth Olsen, Rachel McAdams",
    },
    {
        "id": 1,
        "title": "Moonfall",
        "year": 2022,
        "director": "Roland Emmerich",
        "writters": "Spenser Cohen, Roland Emmerich, Harald Kloser",
        "stars": "Halle Berry, Patrick Wilson, John Bradley",
    },
    {
        "id": 2,
        "title": "Death on the Nile",
        "year": 2022,
        "director": "Kenneth Branagh",
        "writters": "Agatha Christie, Michael Green",
        "stars": "Kenneth Branagh, Gal Gadot, Tom Bateman",
    },
]
cursor = cnx.cursor()

# CREATE MOVIES TABLE
cursor.execute("DROP TABLE IF EXISTS movies;")
cursor.execute("""
CREATE TABLE movies (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    year INT,
    director VARCHAR(255),
    writters TEXT,
    stars TEXT
);
""")
#Query to insert values
movie_insert_query = """
    INSERT INTO movies (title, year, director, writters, stars)
    VALUES (%s, %s, %s, %s, %s);
"""
#loop through movies to add into table
for m in movies:
    cursor.execute(movie_insert_query, (
        m["title"], 
        m["year"], 
        m["director"], 
        m["writters"], 
        m["stars"]
    ))

cnx.commit()

# CREATE USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(100),
    role VARCHAR(20)
);
""")

cursor.execute("SELECT COUNT(*) FROM users;")
count = cursor.fetchone()[0]
#Insert Users into User table
if count == 0:
    users = [
        {"username": "testuser", "password": "testuser", "role": "admin"},
        {"username": "John", "password": "John", "role": "reader"},
        {"username": "Anne", "password": "Anne", "role": "admin"},
        {"username": "reader", "password": "reader", "role": "reader"},
        {"username": "admin", "password": "admin", "role": "admin"}
    ]
    for u in users:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (u["username"], u["password"], u["role"])
        )
    cnx.commit()


# ================================
# HELPERS
# ================================
def checkUser(username, password):
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    return cursor.fetchone()


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify(msg="Admins only"), 403
        return fn(*args, **kwargs)
    return wrapper


# ================================
# ROUTES
# ================================
@app.route("/", methods=["GET"])
def firstRoute():
    return render_template("register.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         user = checkUser(username, password)
#         if user:
#             access_token = create_access_token(
#                 identity=user["username"],
#                 additional_claims={"role": user["role"]}
#             )

#             response = make_response(render_template(
#                 "index.html", title="movies", username=username
#             ))
#             set_access_cookies(response, access_token)
#             return response

#     return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = checkUser(username, password)
        if user:
            access_token = create_access_token(
                identity=user["username"],
                additional_claims={"role": user["role"]}
            )

            # Fetch movies from DB instead of Python list
            cursor = cnx.cursor(dictionary=True)
            cursor.execute("SELECT * FROM movies;")
            db_movies = cursor.fetchall()

            response = make_response(
                render_template(
                    "index.html",
                    title="movies",
                    username=username,
                    movies=db_movies
                )
            )
            set_access_cookies(response, access_token)
            return response

    return render_template("register.html")


@app.route("/movies", methods=["GET"])
@jwt_required()
def getMovies():
    username = get_jwt_identity()
    #get movies from MySQL
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movies;")
    movies = cursor.fetchall()
    return render_template("movies.html", username=username, movies=movies)


@app.route("/addmovie", methods=["GET", "POST"])
@jwt_required()
@admin_required
def addMovie():
    username = get_jwt_identity()

    if request.method == "GET":
        return render_template("addMovie.html", username=username)

    if request.method == "POST":
        title = request.form.get("title")
        year = request.form.get("year")
        director = request.form.get("director")
        writters = request.form.get("writters")
        stars = request.form.get("stars")
        #Put Movies into movies table
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(
            """
            INSERT INTO movies (title, year, director, writters, stars)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (title, year, director, writters, stars)
        )
        cnx.commit()

        cursor.execute("SELECT * FROM movies;")
        movies = cursor.fetchall()

        return render_template(
            "movies.html",
            movies=movies,
            username=username,
            title="movies"
        )


@app.route("/addimage", methods=["GET", "POST"])
@jwt_required()
@admin_required
def addimage():
    if request.method == "GET":
        return render_template("addimage.html")

    if request.method == "POST":
        image = request.files["image"]
        id = request.form.get("number")
        imagename = f"image_{id}.png"
        image.save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], imagename))
        return "image loaded"

    return "all done"


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
