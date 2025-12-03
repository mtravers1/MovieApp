# from flask import Flask, request, render_template, session
# from flask import redirect, make_response, jsonify
# from functools import wraps
# import os
# import mysql.connector
# from flask_restful import Resource, Api
# from flask_jwt_extended import create_access_token
# from flask_jwt_extended import jwt_required, verify_jwt_in_request
# from flask_jwt_extended import JWTManager, get_jwt_identity, get_jwt
# from flask_jwt_extended import set_access_cookies


# app = Flask(__name__)
# app.config["JWT_SECRET_KEY"] = "secretkey"
# app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
# app.config["JWT_COOKIE_SECURE"] = False
# jwt = JWTManager(app)
# jwt.init_app(app)
# app = Flask(__name__)
# app.secret_key = "secretkey"
# app.config["UPLOADED_PHOTOS_DEST"] = "static"
# app.config["JWT_SECRET_KEY"] = "secretkey"
# app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
# app.config["JWT_COOKIE_SECURE"] = False
# app.config["JWT_COOKIE_CSRF_PROTECT"] = False

# jwt = JWTManager(app)
# jwt.init_app(app)

# movies = [
#     {
#         "id": 0,
#         "title": "Doctor Strange in the Multiverse of Madness",
#         "year": 2022,
#         "director": "Sam Raimi",
#         "writters": "Jade Halley Bartlett, Steve Ditko, Stan Lee",
#         "stars": "Benedict Cumberbatch, Elizabeth Olsen, Rachel McAdams",
#     },
#     {
#         "id": 1,
#         "title": "Moonfall",
#         "year": 2022,
#         "director": "Roland Emmerich",
#         "writters": "Spenser Cohen, Roland Emmerich, Harald Kloser",
#         "stars": "Halle Berry, Patrick Wilson, John Bradley",
#     },
#     {
#         "id": 2,
#         "title": "Death on the Nile",
#         "year": 2022,
#         "director": "Kenneth Branagh",
#         "writters": "Agatha Christie, Michael Green",
#         "stars": "Kenneth Branagh, Gal Gadot, Tom Bateman",
#     },
# ]

# users = [
#     {"username": "testuser", "password": "testuser", "role": "admin"},
#     {"username": "John", "password": "John", "role": "reader"},
#     {"username": "Anne", "password": "Anne", "role": "admin"},
#     {"username": "reader", "password": "reader", "role": "reader"},
#     {"username": "admin", "password": "admin", "role": "admin"}
# ]

# cnx = mysql.connector.connect(
#     user='root',
#     password='MyPassword',
#     host='127.0.0.1',
#     database='Movies',
#     auth_plugin='mysql_native_password'
# )

# cursor = cnx.cursor()

# # ================================
# # CREATE MOVIES TABLE
# # ================================
# cursor.execute("DROP TABLE IF EXISTS movies;")
# cursor.execute("""
# CREATE TABLE movies (
#     id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(255),
#     year INT,
#     director VARCHAR(255),
#     writters TEXT,
#     stars TEXT
#     );
# """)

# # Insert movies
# movie_insert_query = """
#     INSERT INTO movies (id, title, year, director, writters, stars)
#     VALUES (%s, %s, %s, %s, %s, %s);
# """










# # for m in movies:
# #     cursor.execute(movie_insert_query, (
# #         m["id"], m["title"], m["year"], m["director"], m["writters"], m["stars"]
# #     ))


# # ================================
# # CREATE USERS TABLE
# # ================================
# cursor.execute("DROP TABLE IF EXISTS users;")
# cursor.execute("""
#     CREATE TABLE users (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         username VARCHAR(100),
#         password VARCHAR(100),
#         role VARCHAR(20)
#     );
# """)

# user_insert_query = """
#     INSERT INTO users (username, password, role)
#     VALUES (%s, %s, %s);
# """

# for u in users:
#     cursor.execute(user_insert_query, (
#         u["username"], u["password"], u["role"]
#     ))


# # Commit changes
# cnx.commit()

# # ================================
# # PRINT RESULTS
# # ================================
# print("\nMovies in database:")
# cursor.execute("SELECT * FROM movies;")
# for row in cursor.fetchall():
#     print(row)

# print("\nUsers in database:")
# cursor.execute("SELECT * FROM users;")
# for row in cursor.fetchall():
#     print(row)

# # cursor.close()
# # cnx.close()
# print("\nData inserted successfully!")



# def admin_required(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         verify_jwt_in_request()
#         #claims = get_jwt_claims()
#         claims = get_jwt()
#         print(claims)
#         #if claims['role'] != 'admin':
#         if claims['fresh']['role'] != 'admin':
#             return jsonify(msg='Admins only'), 403
#         else:
#             return fn(*args, **kwargs)
#     return wrapper


# def checkUser(username, password):
#     for user in users:
#         if username in user["username"] and password in user["password"]:
#             return {"username": user["username"], "role": user["role"]}
#     return None


# @app.route("/", methods=["GET"])
# def firstRoute():
#     return render_template("register.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         validUser = checkUser(username, password)
#         if validUser != None:
#             # set JWT token

#             user_claims = {"role": validUser["role"]}
#             #access_token = create_access_token(username, user_claims=user_claims)
#             access_token = create_access_token(username, user_claims)

#             response = make_response(
#                 render_template(
#                     "index.html", title="movies", username=username, movies=movies
#                 )
#             )
#             response.status_code = 200
#             # add jwt-token to response headers
#             # response.headers.extend({"jwt-token": access_token})
#             set_access_cookies(response, access_token)
#             return response

#     return render_template("register.html")


# @app.route("/logout")
# def logout():
#     # invalidate the JWT token

#     return "Logged Out of My Movies"


# @app.route("/movies", methods=["GET"])
# @jwt_required()
# def getMovies():
#     try:
#         username = get_jwt_identity()
#         cursor = cnx.cursor(dictionary=True)  # return rows as dicts

#         # Fetch all movies
#         cursor.execute("SELECT * FROM movies;")
#         movies = cursor.fetchall()

#         # cursor.close()
#         # cnx.close()
#         return render_template('movies.html', username=username, movies=movies)
#     except:
#         return render_template("register.html")
    

# # @app.route("/addmovie", methods=["GET", "POST"])
# # @jwt_required()
# # @admin_required
# # def addMovie():
# #     username = get_jwt_identity()
# #     if request.method == "GET":
# #         return render_template("addMovie.html", username=username)
# #     if request.method == "POST":
# #         # expects pure json with quotes everywheree
# #         # id = len(movies)
# #         title = request.form.get("title")
# #         year = request.form.get("year")
# #         newmovie = {"id": id, "title": title, "year": year}
# #         movies.append(newmovie)
# #         insert_query = """
# #             INSERT INTO movies (title, year)
# #             VALUES (%s, %s, %s, %s, %s);
# #         """
# #         cursor.execute(insert_query, (title, year))
# #         cnx.commit()

# #         # Load updated movies list
# #         cursor.execute("SELECT * FROM movies;")
# #         movies = cursor.fetchall()

# #         # cursor.close()
# #         # cnx.close()

#     #     return render_template(
#     #         "movies.html", 
#     #         movies=movies, 
#     #         username=username, 
#     #         title="movies"
#     #     )
#     #     return render_template(
#     #         "movies.html", movies=movies, username=username, title="movies"
#     #     )
#     # else:
#     #     return 400
# @app.route("/addmovie", methods=["GET", "POST"])
# @jwt_required()
# @admin_required
# def addMovie():
#     username = get_jwt_identity()

#     if request.method == "GET":
#         return render_template("addMovie.html", username=username)

#     if request.method == "POST":
#         # Get form data
#         title = request.form.get("title")
#         year = request.form.get("year")
#         director = request.form.get("director")
#         writters = request.form.get("writters")
#         stars = request.form.get("stars")

#         # # Connect to MySQL
#         # cnx = mysql.connector.connect(
#         #     user='root',
#         #     password='MyPassword',
#         #     host='127.0.0.1',
#         #     database='education',
#         #     auth_plugin='mysql_native_password'
#         # )
#         cursor = cnx.cursor(dictionary=True)

#         # Correct INSERT query
#         insert_query = """
#             INSERT INTO movies (title, year, director, writters, stars)
#             VALUES (%s, %s, %s, %s, %s);
#         """

#         cursor.execute(insert_query, (title, year, director, writters, stars))
#         cnx.commit()

#         # Load updated movies list
#         cursor.execute("SELECT * FROM movies;")
#         movies = cursor.fetchall()

#         # cursor.close()
#         # cnx.close()

#         return render_template(
#             "movies.html",
#             movies=movies,
#             username=username,
#             title="movies"
#         )

#     return "Bad Request", 400


# @app.route("/addimage", methods=["GET", "POST"])
# @jwt_required()
# @admin_required
# def addimage():
#     if request.method == "GET":
#         return render_template("addimage.html")
#     elif request.method == "POST":
#         image = request.files["image"]
#         id = request.form.get("number")  # use id to number the image
#         imagename = "image_" + id + ".png"
#         image.save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], imagename))
#         print(image.filename)
#         return "image loaded"

#     return "all done"


# if __name__ == "__main__":
#     #app.run(debug=True, host="0.0.0.0", port=5000)
#     app.run(debug=True, host="127.0.0.1", port=5000)
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

# JWT SETTINGS
app.config["JWT_SECRET_KEY"] = "secretkey"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
jwt = JWTManager(app)

app.config["UPLOADED_PHOTOS_DEST"] = "static"

# Database connection
cnx = mysql.connector.connect(
    user='root',
    password='MyPassword',
    host='127.0.0.1',
    database='Movies',
    auth_plugin='mysql_native_password'
)

# ================================
# CREATE MOVIES TABLE
# ================================
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS movies (
#     id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(255),
#     year INT,
#     director VARCHAR(255),
#     writters TEXT,
#     stars TEXT
# );
# """)
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

# ================================
# CREATE MOVIES TABLE
# ================================
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

# Insert movies (NO ID — auto-increment handles it)
movie_insert_query = """
    INSERT INTO movies (title, year, director, writters, stars)
    VALUES (%s, %s, %s, %s, %s);
"""

for m in movies:
    cursor.execute(movie_insert_query, (
        m["title"], 
        m["year"], 
        m["director"], 
        m["writters"], 
        m["stars"]
    ))

cnx.commit()

# ================================
# CREATE USERS TABLE
# ================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(100),
    role VARCHAR(20)
);
""")

# Hardcoded users (skip re-inserting if table already populated)
cursor.execute("SELECT COUNT(*) FROM users;")
count = cursor.fetchone()[0]

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
