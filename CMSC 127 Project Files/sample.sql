import mysql.connector as mariadb

mariadb_connection = mariadb.connect(user='test', password = 'password', host = 'localhost', port = '3306')

create_cursor = mariadb_connection.cursor()

#################### CREATE DATABASE & TABLES ################################
##################### Show databases
create_cursor.execute("CREATE DATABASE test_database")

### create database
create_cursor.execute("SHOW DATABASES")

for x in create_cursor:
    print(x)

    