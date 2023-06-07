import mariadb
import sys
import signupLoginMenu

con = mariadb.connect(
    user="root",
    password="ilove127",
    host="localhost",)

cur  = con.cursor()
with open('Project_Dependencies.sql', 'r') as sql_file:
    result_iterator = cur.execute(sql_file.read(), multi=True)
    for res in result_iterator:
        print("Running query: ", res)  # Will print out a short representation of the query
        print(f"Affected {res.rowcount} rows" )

cur.commit()

#separate function call module to stop iterating mainMenuLoop if imported from other modules
# signupLoginMenu.mainMenuLoop()