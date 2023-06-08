import sys
import mysql.connector
# import signupLoginMenu

# connects to a mariadb database
con = mysql.connector.connect(
    user="root",
    password="ilove127",
    host="localhost",
    port= 3306,
    )

# perform database operations here:
# used to execute sql queries on the databases
cur  = con.cursor()

# opens a file in read mode
with open('Project_Dependencies.sql', 'r') as sql_file:
    result_iterator = cur.execute(sql_file.read(), multi=True) # reads content of the sql file

con.commit()
#separate function call module to stop iterating mainMenuLoop if imported from other modules
# signupLoginMenu.mainMenuLoop()