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
