import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "atharva2105"  # Replace with your MySQL password
        self.database = "InventoryDB"
        self.connection = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Successfully connected to MySQL database")
                return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")
    
    def get_cursor(self):
        if self.connection:
            return self.connection.cursor(dictionary=True)
        return None
