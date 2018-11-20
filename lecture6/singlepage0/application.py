from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

texts = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam tortor mauris, maximus semper volutpat vitae, varius placerat dui. Nunc consequat dictum est, at vestibulum est hendrerit at. Mauris suscipit neque ultrices nisl interdum accumsan. Sed euismod, ligula eget tristique semper, lectus est pellentesque dui, sit amet rhoncus leo mi nec orci. Curabitur hendrerit, est in ultricies interdum, lacus lacus aliquam mauris, vel vestibulum magna nisl id arcu. Cras luctus tellus ac convallis venenatis. Cras consequat tempor tincidunt. Proin ultricies purus mauris, non tempor turpis mollis id. Nam iaculis risus mauris, quis ornare neque semper vel.",
        "Praesent euismod auctor quam, id congue tellus malesuada vitae. Ut sed lacinia quam. Sed vitae mattis metus, vel gravida ante. Praesent tincidunt nulla non sapien tincidunt, vitae semper diam faucibus. Nulla venenatis tincidunt efficitur. Integer justo nunc, egestas eget dignissim dignissim, fermentum ac sapien. Suspendisse non libero facilisis, dictum nunc ut, tincidunt diam.",
        "Morbi imperdiet nunc ac quam hendrerit faucibus. Morbi viverra justo est, ut bibendum lacus vehicula at. Fusce eget risus arcu. Quisque dictum porttitor nisl, eget condimentum leo mollis sed. Proin justo nisl, lacinia id erat in, suscipit ultrices nisi. Suspendisse placerat nulla at volutpat interdum. In porttitor condimentum est nec ultricies. Donec nec mollis neque, id dapibus sem."]

@app.route("/first")
def first():
    return texts[0]

@app.route("/second")
def second():
    return texts[1]

@app.route("/third")
def third():
    return texts[2]
