import mysql.connector

mariadb_connection = mysql.connector.connect(
    user="root",
    password="elvinbautista",
    host="localhost",
    database="cmsc127group3")

cur = mariadb_connection.cursor()


def addGroup():
    # print("Add group still WIP!")
    group_name = input("Enter groupname: ")
    try: 
        #TODO: insert new user tuple sql query here
        query = f"INSERT INTO grp (group_name) VALUES ('{group_name}')"
        cur.execute(query)
        mariadb_connection.commit()
        print(group_name,"has been created")
    except mysql.connector.Error as e: 
        print(f"Error: {e}")

def deleteGroup():
    print("Delete group still WIP!")

    #TODO: Request for the groupID to be deleted

def searchGroup():
    print("Search group still WIP!")

    #TODO: Request for the groupID to be searched
    #then display the details of the group

def updateGroup():
    print("Update group still WIP!")

    #TODO: Request for the groupID to be updated
    #then display input fields for the new values

def addFriendtoGroup():
    print("Update group still WIP!")

    #TODO: Request for the groupID to be updated
    #TODO: Request for the userID to be added
    #then display prompt if successful


def groupsManager(userChoice, userName):
    while True:
        print("\n What would you like to do?\n"
            "[1] Add Group\n"
            "[2] Delete Group\n"
            "[3] Search Group\n"
            "[4] Update Group\n"
            "[5] Add Friend to a Group\n"
            "[0] Back"
            )
        groupManagerOption = input("\nEnter choice: ")
        
        if groupManagerOption == '0':

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice,userName)
            break
        elif groupManagerOption == '1':
            addGroup()
        elif groupManagerOption == '2':
            deleteGroup()
        elif groupManagerOption == '3':
            searchGroup()
        elif groupManagerOption == '4':
            updateGroup()
        elif groupManagerOption == '5':
            addFriendtoGroup()
        else:
            print("Invalid Input!")