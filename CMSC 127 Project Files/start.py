import sys
import mysql.connector
from mysql.connector import Error
import signupLoginMenu

def execute_sql_from_file(filename):
    try:
        # Connect to the MySQL server
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ilove127",
        )

        # Create a cursor object to execute SQL statements
        cursor = connection.cursor()

        # create the database
        cursor.execute("CREATE DATABASE IF NOT EXISTS cmsc127group3")
        cursor.execute("USE cmsc127group3")

        # commit changes
        connection.commit()

        # close the cursor and connection and start a new one
        cursor.close()
        connection.close()

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ilove127",
            database="cmsc127group3"    
        )
        cursor = connection.cursor()

        # read the SQL file
        with open(filename, "r") as sql_file:
            sql_statements = sql_file.read()

        # split the statements and execute them individually
        statements = sql_statements.split(';')
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)

        connection.commit()

        print("SQL statements executed successfully!")

    except Error as e:
        print(f"Error executing SQL statements: {e}")

# Call the function and provide the path to your SQL file
execute_sql_from_file("Project_Dependencies.sql")

#separate function call module to stop iterating mainMenuLoop if imported from other modules
signupLoginMenu.mainMenuLoop()