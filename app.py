#Database System Design
#The Second Hand Watch Company
#Anthony Cruz, Ethan Hicks, Kent Ogasawara, Brandon Angell
from flask import Flask, render_template, request, redirect, url_for
from database import Database

app= Flask(__name__)
db = Database()

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

@app.route("/sign", methods=["GET", "POST"])
def sign():
    if request.method == "POST":
        employee_id = request.form["employee_id"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        role = request.form["role"]
        company_id = request.form["company_id"]

        success, message = db.add_employee(employee_id, first_name, last_name, role, company_id)
        return render_template("sign.html", message=message)

    return render_template("sign.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)