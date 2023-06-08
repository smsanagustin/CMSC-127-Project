import sys
import mysql.connector
# import signupLoginMenu

# connects to a mariadb database
try: 
    con = mysql.connector.connect(
        user="root",
        password="ilove127",
        host="localhost",
        port= 3306,
        )
    print("Connection successful!")

    # perform database operations here:
    # used to execute sql queries on the databases
    cur  = con.cursor()

    # opens a file in read mode
    with open('Project_Dependencies.sql', 'r') as sql_file:
        result_iterator = cur.execute(sql_file.read(), multi=True) # reads content of the sql file
        for res in result_iterator:
            print("Running query: ", res)  # Will print out a short representation of the query
            print(f"Affected {res.rowcount} rows" )

    cur.commit()

    # close the connection
    con.close()

except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")
    sys.exit(1)

#separate function call module to stop iterating mainMenuLoop if imported from other modules
# signupLoginMenu.mainMenuLoop()