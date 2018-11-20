import os

import json

from flask import Flask, session, render_template, request, session, jsonify
from flask_session import Session
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

from models import *

app = Flask(__name__)

database = SQLAlchemy()

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    if "user" not in session.keys() or session["user"] is None:
        return render_template("login.html")
    else:
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        #Selec user
        u = User.query.filter_by(email=email).first()
        if u is None or u.password != password:
        	return render_template("error.html", message="Username or password incorrect")
        else:
            session["user"] = u
            return render_template("index.html")
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    """ Logout the user and clean the cache session"""
    session["user"] = None
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        # Create new user
        u = User(name=name, email=email, password=password)

        #Add new user in the database
        u.add_user()

        return render_template("login.html")


@socketio.on("create channel")
def socket_create_channel(data):
    channel = Channel.query.filter_by(name=data['name']).first()
    if channel == None:
        c = Channel(name=data['name'], user_id=session['user'].id)
        c = c.add_channel()
        c.add_user()
        data['id'] = c.id 
        emit("channel created", data, broadcast=True)    
     

@app.route("/channel/<string:id>", methods=["GET"])
def channel(id):
    if request.method == "GET":
        # Checks if the user is in this channel
        u = User_has_channel.query.filter(and_(User_has_channel.user_id == session['user'].id, User_has_channel.channel_id == id)).first()
        c = Channel.query.get(id)
        if u == None:
            c.add_user_in_channel(session['user'].id)

        return render_template("messages.html", channel=c, messages=c.messages)
    

@socketio.on("send message")
def socket_send_message(data):
    # Checks if the user is in this channel
    channel_id = data["channel_id"]
    message = data["message"]
    channel = Channel.query.get(channel_id)
    channel.add_message(message, session['user'].id)
    data['user_id'] = session['user'].id
    emit("message received", data, broadcast=True)


@app.route("/my_channels", methods=["GET"])
def my_channels():
    channels = User_has_channel.query.filter_by(user_id=session["user"].id)
    my_channels = []
    for channel in channels:
        c = Channel.query.filter_by(id=channel.channel_id).first()
        my_channels.append(c)

    return render_template("my_channels.html", my_channels=my_channels)


@app.route("/others_channels", methods=["GET"])
def others_channels():
    channels = User_has_channel.query.filter_by(user_id=session["user"].id)
    my_channels = []
    for channel in channels:
        c = Channel.query.filter_by(id=channel.channel_id).first()
        my_channels.append(c)
    
    others_channels = Channel.query.all()

    
    for channel in my_channels:
        if channel in others_channels:
            others_channels.remove(channel)
    return render_template("others_channels.html", others_channels=others_channels)