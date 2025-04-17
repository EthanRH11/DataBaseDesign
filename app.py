#Database System Design
#The Second Hand Watch Company
#Anthony Cruz, Ethan Hicks, Kent Ogasawara, Brandon Angell
from flask import Flask, render_template, request, redirect, url_for, session
from database import Database

app= Flask(__name__)
app.secret_key = "dev_key"
db = Database()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        employee_id = request.form["employee_id"]
        employee = db.fetch_employee_by_ID(employee_id)

        if employee: 
            employee_data = employee[0]
            session["employee_id"] = employee_id
            session["first_name"] = employee_data["FirstName"]
            
            # Debugging output to verify session data
            print(f"Session data after login: {session}")
            
            return redirect(url_for("home"))
        else:
            return render_template("log.html", message="Invalid Employee ID")

    return render_template("log.html")

@app.route("/repairs")
def repairs():
    status = request.args.get('status', 'in progress')

    repairs_data = db.get_watch_repairs_by_status(status)

    return render_template("repair.html", repairs=repairs_data, selected_status=status)

@app.route("/employee")
def employee():
    employees = db.list_all_employees()
    return render_template("employee.html", employees=employees)

@app.route("/customer")
def customer():
    customers = db.listAllCustomers()
    return render_template("customer.html", customers=customers)


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
