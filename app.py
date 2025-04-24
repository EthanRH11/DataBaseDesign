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

@app.route("/shop", methods=["GET", "POST"])
def shop():
    part_data = None
    message = None

    all_parts = db.get_all_parts()
    
    if request.method == "POST":
        # Debug print to see if we're hitting this code path
        print("POST request received")
        
        part_name = request.form.get("part_name")
        print(f"Searching for part: {part_name}")
        
        if part_name:
            part_data = db.get_part_by_name(part_name)
            print(f"Part data returned: {part_data}")
            
            if not part_data:
                message = f"No part found with name: {part_name}"
    
    return render_template("shop.html", part=part_data, message=message, all_parts=all_parts)

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
    status = request.args.get('status', 'In Progress')

    repairs_data = db.get_watch_repairs_by_status(status)

    all_statuses = ["Completed", "In Progress", "Diagnostics", "Awaiting Parts", "Scheduled"]

    return render_template("repair.html", repairs=repairs_data, selected_status=status, all_statuses=all_statuses)

@app.route("/employee", methods =["GET","POST"])
def employee():
    if request.method == "POST":
        name_part = request.form.get("search", "")
        employees = db.fetchSpecificEmployee(name_part)
    else:
        employees = db.list_all_employees()
    return render_template("employee.html", employees=employees)

@app.route("/customer", methods=["GET","POST"])
def customer():
    if request.method == "POST":
        name_part = request.form.get("search", "")
        customers = db.fetchSpecificCustomer(name_part)
    else:
        customers = db.listAllCustomers()

    return render_template("customer.html", customers=customers)

@app.route('/newCustomer', methods=["GET", "POST"])
def newCustomer():
    if request.method == "POST":
        customer_id = request.form['customer_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']

        success, message = db.addCustomer(customer_id, first_name, last_name, email, phone_number)
        return render_template("newCustomer.html", message=message)

    return render_template("newCustomer.html")


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

#date adding works, show all events, and active events no
@app.route("/events", methods=["GET", "POST"])
def events():
    if request.method == "POST":
        event_id = request.form["event_id"]
        name = request.form["name"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        discount_percent = request.form["discount_percent"]
        
        success, message = db.add_event(event_id, name, start_date, end_date, discount_percent)
        
        events_data = db.list_all_events()
        active_events = db.get_active_events()
        return render_template("events.html", events=events_data, active_events=active_events, message=message)
    
    else: 
        events_data = db.list_all_events()
        active_events = db.get_active_events()
        return render_template("events.html", events=events_data, active_events=active_events)
    
@app.route("/watches", methods=["GET", "POST"])
def watches():
    watch_data = None
    message = None

    all_watches = []

    if request.method == "POST":
        max_price = request.form.get("max_price")

        if max_price and max_price.strip() and max_price.replace('.', '', 1).isdigit():
            max_price = float(max_price)
            all_watches = db.get_Watch_By_Price(max_price)

            if not all_watches:
                message = f"No watches found under ${max_price:.2f}"
        else:
            all_watches = db.get_Watch_By_Price()
    else:
        all_watches = db.get_Watch_By_Price()

    return render_template("watches.html", watch=watch_data, message=message, all_watches=all_watches)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
