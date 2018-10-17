import os

import json

from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from classes import User, Book

import requests

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    if session["user"] is None:
        return login()
    else:
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        result = db.execute("SELECT id, name, email, username, password FROM users WHERE username=:username AND password=:password", {"username": username, "password": password}).fetchone()
        if result is None:
        	return render_template("error.html", message="Username or password incorrect")
        else:
            user = User(result.id, result.name, result.email, result.username, result.password)
            
        
            if user:
                session["user"] = user
                return render_template("index.html")
    
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        db.execute("INSERT INTO users(name, email, username, password) VALUES (:name, :email, :username, :password)", {"name": name, "email": email, "username": username, "password": password})
        db.commit()
        return render_template("login.html")


@app.route("/layout")
def layout():
    return render_template("layout.html")


@app.route("/logout")
def logout():
    """ Logout the user and clean the cache session"""
    session["user"] = None
    return render_template("login.html")


@app.route("/books", methods=["GET", "POST"])
def books():
    if session["user"] is None:
        return login()

    """ If the request is GET, render the page of search to the user with no books"""
    if request.method == "GET":
        return render_template("books.html")
    else:
        """ If the request is POST, do the search with the text provided by the user"""
        text = "%"+request.form.get("search-text")+"%"
        books = db.execute("SELECT * FROM books WHERE (isbn LIKE :isbn OR title LIKE :title OR author LIKE :author OR year LIKE :year)", {"isbn":text, "title":text, "author":text, "year":text}).fetchall()
        return render_template("books.html", books=books)


@app.route("/details/<string:isbn>", methods=["GET", "POST"])
def details(isbn):
    if session["user"] is None:
        return login()
    """ Give all the details about the book"""
    book = Book()

    book.isbn, book.title, book.author, book.year, book.reviews_count, book.average_rating = db.execute("SELECT isbn, title, author, year, reviews_count, average_rating FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()

    if book.average_rating==0 or book.reviews_count==0:
        book_aux = api_intern(isbn)
        
        book.average_rating = book_aux["books"][0]["average_rating"]
        book.reviews_count = book_aux["books"][0]["reviews_count"]
        db.execute("UPDATE books SET average_rating = :average_rating, reviews_count = :reviews_count WHERE isbn=:isbn", {"isbn": isbn, "average_rating": float(book.average_rating), "reviews_count": int(book.reviews_count)})

        db.commit()
    if request.method == "GET":
        return render_template("details.html", book=book)
    else:
        return "POST DETAILS"


@app.route("/api/<string:isbn>", methods=["GET"])
def api(isbn):
    """ Give all the details about the book"""
    if request.method == "GET":
        res = db.execute("SELECT title, author, year, isbn, reviews_count, average_rating FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
        book = Book()

        if res is None:
            return render_template("error.html", message="404 book not found"), 404
        
        book.title, book.author, book.year, book.isbn, book.reviews_count, book.average_rating = res
        if res.reviews_count==0 or res.average_rating==0:
            book_aux = api_intern(isbn)
            book.average_rating = book_aux["books"][0]["average_rating"]
            book.reviews_count = book_aux["books"][0]["reviews_count"]

        response = {"title": book.title, "author": book.author, "year": book.year, "isbn": book.isbn, "review_count": book.reviews_count, "average_score": book.average_rating}
        return jsonify(response)
    

def api_intern(isbn):
    """ Give all the details about the book"""
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "tG3fNOMnNgw8HsbsI1Rhdg", "isbns": isbn})

    return res.json()
    

""" Route to submit and see the reviews from one book"""
@app.route("/review/<string:isbn>", methods=["GET", "POST"])
def review(isbn):
    if session["user"] is None:
        return login()

    """ Render form to the user submit a review """
    book = db.execute("SELECT * FROM books WHERE isbn= :isbn"
        , {"isbn": isbn}).fetchone()
    if request.method == "POST":
        review = request.form.get("review")
        score = request.form.get("score")
        """ Calculating new average rating and number of reviews from the book """
        average_rating = (book.average_rating + float(score))/2
        reviews_count = book.reviews_count + 1
        comments = db.execute("SELECT * FROM reviews WHERE author_id= :author_id AND book_isbn= :book_isbn", {"author_id": session["user"].id, "book_isbn": isbn}).fetchone()

        """ Checks if the user already made a comment to this book """
        if comments is not None:
            return render_template("error.html", message="You already posted a comment to this book")

        db.execute("INSERT INTO reviews(review, score, author_id, book_isbn) VALUES (:review, :score, :author_id, :book_isbn)", {"review": review, "score": score, "author_id": session["user"].id, "book_isbn": isbn})
        db.execute("UPDATE books SET average_rating = :average_rating, reviews_count = :reviews_count WHERE isbn=:isbn", {"isbn": isbn, "average_rating": average_rating, "reviews_count": reviews_count})

        db.commit()

    reviews = db.execute("SELECT * FROM reviews WHERE book_isbn= :isbn"
        , {"isbn": isbn}).fetchall()
    return render_template("review.html", book=book, reviews=reviews)