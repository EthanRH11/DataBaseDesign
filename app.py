#Database System Design
#The Second Hand Watch Company
#Anthony Cruz, Ethan Hicks, Kent Ogasawara, Brandon Angell
from flask import Flask, render_template

app= Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/login")
def login():
    return render_template("log.html")

@app.route("/repairs")
def repairs():
    return render_template("repair.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)