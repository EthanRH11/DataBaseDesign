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
                self.connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    db=self.db,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
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
                SELECT CustomerID, FirstName, LastName, number
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
                WHERE FirstName LIKE %s
                """
                print(f"Executing query with parameters: '%{name_part}%'")
                cursor.execute(query, (f'%{name_part}%',))
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
        
    def addCustomer(self, CustomerID, FirstName, LastName, email, number):
        conn = self.connect()
        if conn is None:
            return False
        
        try:
            with conn.cursor() as cursor:
                query = """
                INSERT INTO ehicks12.customer (CustomerID, FirstName, LastName, email, number)
                VALUE (%s, %s, %s, %s, %s)
                """
                return True, "Student added successfully"
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