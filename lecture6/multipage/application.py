from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def first():
    return render_template("first.html")

@app.route("/second")
def second():
    return render_template("second.html")

@app.route("/third")
def third():
    return render_template("third.html")
