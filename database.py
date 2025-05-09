import pymysql

class Database:

    def __init__(self, host='dbdev.cs.kent.edu', user='ehicks12',
                 password='7Yg2Zisd', db='ehicks12'):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.connection = None
        
    def connect(self):
        """Connect to the database and return a connection object."""
        try:
            if self.connection is None:
                print(f"Attempting to connect to {self.host} as user {self.user}...")
                self.connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    db=self.db,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
                print("Connection Successful!")
            return self.connection
        except pymysql.MySQLError as e:
            print(f"Error connecting to the database: {e}")
            return None

    def listAllCompleteWatches(self):
        """List all complete watches"""
        conn = self.connect()
        if conn is None:
            return []
        
        try:
            with conn.cursor() as cursor:
                query = """
                SELECT WatchID, Model, Description, Price, Type
                FROM ehicks12.CompleteWatch
                ORDER BY Price
                """
                cursor.execute(query)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error getting watches: {e}")
            return []
        
    def listAllCustomers(self):
        conn = self.connect()
        if conn is None:
            return []
        
        try:
            with conn.cursor() as cursor:
                query = """
                SELECT CustomerID, FirstName, LastName, email, number
                From ehicks12.Customer
                ORDER BY LastName
                """
                cursor.execute(query)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error getting customers: {e}")
            return []
        
    def fetchSpecificCustomer(self, name_part):
        conn = self.connect()
        if conn is None:
            return []
        
        try:
            with conn.cursor() as cursor:
                check_query = "SELECT COUNT(*) as count FROM ehicks12.Customer"
                cursor.execute(check_query)
                result = cursor.fetchone()
                print(f"Total customers in database: {result['count'] if result else 'unknown'}")

            with conn.cursor() as cursor:
                query = """
                SELECT * FROM ehicks12.Customer
                WHERE FirstName LIKE %s OR LastName LIKE %s
                    OR email LIKE %s
                    OR number LIKE %s
                    OR CustomerID LIKE %s
                """

                wildcard = f"%{name_part}%"
                print(f"Executing query with parameters: '%{wildcard}%' across multiple fields")
                cursor.execute(query, (wildcard, wildcard, wildcard, wildcard, wildcard))
                results = cursor.fetchall()
                print(f"Search results for name '{name_part}': {results}")

                if not results:
                    print("No results found, trying more basic query...")
                    basic_query = "SELECT * FROM ehicks12.Customer LIMIT 5"
                    cursor.execute(basic_query)
                    sample_results = cursor.fetchall()
                    print(f"Sample customer records: {sample_results}")

                return results
        except pymysql.MySQLError as e:
            error_msg = str(e)
            print(f"Error searching customers by name: {error_msg}")
            return []
        
    def fetchSpecificEmployee(self, name_part):
        conn = self.connect()
        if conn is None:
            return []
        
        try:
            with conn.cursor() as cursor:
                check_query = "SELECT COUNT(*) as count FROM ehicks12.Employee"
                cursor.execute(check_query)
                result = cursor.fetchone()
                print(f"Total employees in database: {result['count'] if result else 'unknown'}")

            with conn.cursor() as cursor:
                query = """
                SELECT * FROM ehicks12.Employee
                WHERE FirstName LIKE %s OR LastName LIKE %s
                    OR Role LIKE %s
                    OR EmployeeID LIKE %s
                    OR CompanyID LIKE %s
                """

                wildcard = f"%{name_part}%"
                print(f"Executing query with parameters: '%{wildcard}%' across multiple fields")
                cursor.execute(query, (wildcard, wildcard, wildcard, wildcard, wildcard))
                results = cursor.fetchall()
                print(f"Search results for name '{name_part}': {results}")

                if not results:
                    print("No results found, trying more basic query...")
                    basic_query = "SELECT * FROM customer LIMIT 5"
                    cursor.execute(basic_query)
                    sample_results = cursor.fetchall()
                    print(f"Sample customer records: {sample_results}")

                return results
        except pymysql.MySQLError as e:
            error_msg = str(e)
            print(f"Error searching customers by name: {error_msg}")
            return []
        
    def addCustomer(self, CustomerID, FirstName, LastName, email, number):
        conn = self.connect()
        if conn is None:
            return False
        
        try:
            with conn.cursor() as cursor:
                query = """
                INSERT INTO ehicks12.Customer (CustomerID, FirstName, LastName, email, number)
                VALUE (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (CustomerID, FirstName, LastName, email, number))
                conn.commit()
                return True, "Customer added successfully"
        except pymysql.MySQLError as e:
            error_msg = str(e)
            print(f"Error adding stduent: {error_msg}")

            if "Duplicate entry" in error_msg and "PRIMARY" in error_msg:
                error_msg = f"CustomerID '{CustomerID}' already exists"

            try:
                conn.rollback()
            except:
                pass
            return False, error_msg
        
    def add_employee(self, employee_id, first_name, last_name, role, company_id):
        conn = self.connect()
        if conn is None:
            return False, "Database connection failed"

        try:
            with conn.cursor() as cursor:
                query = """
                INSERT INTO ehicks12.Employee (EmployeeID, FirstName, LastName, Role, CompanyID)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (employee_id, first_name, last_name, role, company_id))
                conn.commit()
                return True, "Employee account created successfully"
        except pymysql.MySQLError as e:
            error_msg = str(e)
            print(f"Error adding employee: {error_msg}")

            try:
                conn.rollback()
            except:
                pass

            if "Duplicate entry" in error_msg and "PRIMARY" in error_msg:
                error_msg = f"Employee ID '{employee_id}' already exists"
            return False, error_msg
        
    def list_all_employees(self):
        conn = self.connect()
        if conn is None:
            return []
        
        try:
            with conn.cursor() as cursor:
                query = """
                Select EmployeeID, FirstName, LastName, Role, CompanyID
                From ehicks12.Employee
                ORDER BY LastName
                """
                cursor.execute(query)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error getting employees: {e}")
            return []
    
    def fetch_employee_by_ID(self, id_part):
        conn = self.connect()
        if conn is None:
            return []
        
        try:
            with conn.cursor() as cursor:
                query = """
                SELECT * FROM ehicks12.Employee
                WHERE EmployeeID LIKE %s
                """
                cursor.execute(query, (f'%{id_part}%'))
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            error_msg = str(e)
            print(f"Error searching Employees by ID: {error_msg}")
            return []
        return results
        
    def employee_search_by_role(self, role_part):
        conn = self.connect()
        if conn is None:
            return False
        
        try:
            with conn.cursor() as cursor:
                query = """
                SELECT EmployeeID, FirstName, LastName, Role, CompanyID
                FROM ehicks12.Employee
                WHERE Role = %s
                """
                cursor.execute(query, (role_part,))
                results = cursor.fetchall()
                return results
        except pymysql.MySQLError as e:
            error_msg = str(e)
            print(f"Error searching employee by role: {error_msg}")
            return []
        
    def get_watch_repairs_by_status(self, status):
        conn = self.connect()
        if conn is None:
            return []
    
        try:
            with conn.cursor() as cursor:
                query = """
                SELECT c.CustomerID, c.FirstName, c.LastName, c.number, wr.RepairID, wr.status 
                FROM ehicks12.Customer AS c 
                INNER JOIN ehicks12.WatchRepair AS wr 
                ON c.CustomerID = wr.CustomerID 
                WHERE wr.status = %s
                """
                cursor.execute(query, (status,))
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            error_msg = str(e)
            print(f"Error getting repairs by status: {error_msg}")
            return []
        
    def get_completed_watch_repairs(self):
        conn = self.connect()
        if conn is None:
            return []
    
        try:
            with conn.cursor() as cursor:
                query = """
                SELECT c.CustomerID, c.FirstName, c.LastName, c.number, wr.RepairID, wr.status 
                FROM ehicks12.Customer AS c 
                INNER JOIN ehicks12.WatchRepair AS wr 
                ON c.CustomerID = wr.CustomerID 
                WHERE wr.status = 'complete'
                """
            cursor.execute(query)
            return cursor.fetchall()
        except pymysql.MySQLError as e:
            error_msg = str(e)
            print(f"Error getting customers with completed repairs: {error_msg}")
            return []
        
    def get_Watch_by_ID(self, watchID):
        conn = self.connect()
        if conn is None:
            return []
        
        try:
            with conn.cursor as cursor:
                query="""
                SELECT WatchID, Model, Description, Price, Type
                FROM ehicks12.CompleteWatch
                WHERE WatchID = %s
                """
                cursor.execute(query, (watchID,))
                result = cursor.fetchone()
                return result
        except pymysql.MySQLError as e:
            error_msg = str(e)
            print(f"Error getting watch by ID: {error_msg}")
            return None
        
    def get_Watch_By_Price(self, price=None):
        conn = self.connect()
        if conn is None:
            return []
        
        try:
            with conn.cursor() as cursor:
                if price is not None:
                    query="""
                    SELECT WatchID, Model, Description, Price, Type
                    FROM ehicks12.CompleteWatch
                    WHERE Price <= %s
                    ORDER BY Price ASC
                    """
                    cursor.execute(query, (price,))
                else:
                    query = """
                    SELECT WatchID, Model, Description, Price, Type
                    FROM ehicks12.CompleteWatch
                    ORDER BY Price ASC
                    """
                    cursor.execute(query)
                
                result = cursor.fetchall()
                return result
        except pymysql.MySQLError as e:
            error_msg = str(e)
            print(f"Error getting watches by price: {error_msg}")
            return []

    def add_event(self, event_id, name, start_date, end_date, discount_percent):
        conn = self.connect()
        if conn is None:
            return False, "Database connection failed"

        try:
            with conn.cursor() as cursor:
                query = """
                INSERT INTO ehicks12.SaleEvent (EventID, Name, startDate, endDate, discountPercent)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (event_id, name, start_date, end_date, discount_percent))
                conn.commit()
                return True, "Sale event added successfully"
        except pymysql.MySQLError as e:
            error_msg = str(e)
            print(f"Error adding sale event: {error_msg}")

        try:
            conn.rollback()
        except:
            pass

        if "Duplicate entry" in error_msg and "PRIMARY" in error_msg:
            error_msg = f"Event ID '{event_id}' already exists"
            return False, error_msg

    def list_all_events(self):
        conn = self.connect()
        if conn is None:
            return []
    
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:  
                query = """
                SELECT EventID, Name, startDate, endDate, discountPercent
                FROM ehicks12.SaleEvent
                ORDER BY startDate
                """
                cursor.execute(query)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error getting sale events: {e}")
            return []
        
    def get_active_events(self):
        conn = self.connect()
        if conn is None:
            return []
    
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:  
                query = """
                SELECT EventID, Name, startDate, endDate, discountPercent
                FROM ehicks12.SaleEvent
                WHERE CURDATE() BETWEEN startDate AND endDate
                ORDER BY discountPercent DESC
                """
                cursor.execute(query)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error getting active sale events: {e}")
            return []
            
    def get_part_by_name(self, part_name):
        conn = self.connect()
        if conn is None:
            return []

        try:
            with conn.cursor() as cursor:
                query="""
                SELECT partID, Name, Description, QuantityInStock
                FROM ehicks12.WatchPart
                WHERE Name = %s
                """
                cursor.execute(query, (part_name,))
                result = cursor.fetchone()
                return result
        except pymysql.MySQLError as e:
            print("Error getting watch part by name: {e}")
            return None
        
    def get_all_parts(self):
        conn = self.connect()
        if conn is None:
            return []
        
        try:
            with conn.cursor() as cursor:
                query="""
                Select partID, Name, Description, QuantityInStock
                From ehicks12.WatchPart
                ORDER BY Name
                """
                cursor.execute(query)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error getting employees: {e}")
            return []


        

    def removeCustomer(self, CustomerID):
        conn = self.connect()
        if conn is None:
            return False, "Database connection failed"

        try:
            with conn.cursor() as cursor:
                query = """
                DELETE FROM ehicks12.Customer WHERE CustomerID = %s
                """
                cursor.execute(query, (CustomerID,))
                conn.commit()
                if cursor.rowcount == 0:
                    return False, f"No customer found with CustomerID '{CustomerID}'"
                return True, "Customer removed successfully"
        except pymysql.MySQLError as e:
            error_msg = str(e)
            print(f"Error removing customer: {error_msg}")
            try:
                conn.rollback()
            except:
                pass
            return False, error_msg
        
    def removeEmployee(self, EmployeeID):
        conn = self.connect()
        if conn is None:
            return False, "Database connection failed"

        try:
            with conn.cursor() as cursor:
                query = """
                DELETE FROM ehicks12.Employee WHERE EmployeeID = %s
                """
                cursor.execute(query, (EmployeeID,))
                conn.commit()
                if cursor.rowcount == 0:
                    return False, f"No employee found with EmployeeID '{EmployeeID}'"
                return True, "Employee removed successfully"
        except pymysql.MySQLError as e:
            error_msg = str(e)
            print(f"Error removing customer: {error_msg}")
            try:
                conn.rollback()
            except:
                pass
            return False, error_msg
        
    def getCustomerByID(self, customerID):
        conn = self.connect()
        if conn is None:
            return None
        
        try:
            with conn.cursor() as cursor:
                query = """
                SELECT CustomerID, FirstName, LastName, email, number
                FROM ehicks12.Customer
                WHERE CustomerID = %s
                """
                cursor.execute(query, (customerID,))
                result = cursor.fetchone()
                return result
        except pymysql.MySQLError as e:
            print(f"Error getting customer by ID: {e}")
            return None
        
        
    def getEmployeeByID(self, employeerID):
        conn = self.connect()
        if conn is None:
            return None
        
        try:
            with conn.cursor() as cursor:
                query = """
                SELECT EmployeeID, FirstName, LastName, Role, CompanyID
                FROM ehicks12.Employee
                WHERE employeeID = %s
                """
                cursor.execute(query, (employeerID,))
                result = cursor.fetchone()
                return result
        except pymysql.MySQLError as e:
            print(f"Error getting customer by ID: {e}")
            return None
    
    def updateCustomer(self, customer_data):
        conn = self.connect()
        if conn is None:
            return False
        
        try:
            with conn.cursor() as cursor:
                query = """
                UPDATE ehicks12.Customer
                SET FirstName = %s, LastName = %s, email = %s, number = %s
                WHERE CustomerID = %s
                """
                cursor.execute(
                    query,
                    (
                        customer_data["FirstName"],
                        customer_data["LastName"],
                        customer_data["email"],
                        customer_data["number"],
                        customer_data["CustomerID"]
                    )
                )
            conn.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"Error updating customer: {e}")
            return False
        
    def updateEmployee(self, employee_data):
        conn = self.connect()
        if conn is None:
            return False
        
        try:
            with conn.cursor() as cursor:
                query = """
                UPDATE ehicks12.Employee
                SET FirstName = %s, LastName = %s, Role = %s, CompanyID = %s
                WHERE EmployeeID = %s
                """
                cursor.execute(
                    query,
                    (
                        employee_data["FirstName"],
                        employee_data["LastName"],
                        employee_data["Role"],
                        employee_data["CompanyID"],
                        employee_data["EmployeeID"]
                    )
                )
            conn.commit()
            return True
        except pymysql.MySQLError as e:
            print(f"Error updating employee: {e}")
            return False
