import mysql.connector

mariadb_connection = mysql.connector.connect(
    user="root",
    password="elvinbautista",
    host="localhost",
    database="cmsc127group3")

cur = mariadb_connection.cursor()

def getGroups():
    groups = {}
    try: 
        #TODO: insert new user tuple sql query here
        query = f"SELECT * FROM grp"
        cur.execute(query)
        for group in cur:
            groups[group[0]] = group[1]
        return groups
    except mysql.connector.Error as e: 
        print(f"Error: {e}")    

def addGroup():
    print("\t-----ADDING-----\n")
    group_name = input("Enter groupname: ")
    try: 
        query = f"INSERT INTO grp (group_name) VALUES ('{group_name}')"
        cur.execute(query)
        mariadb_connection.commit()
        print(group_name,"has been created")
    except mysql.connector.Error as e: 
        print(f"Error: {e}")

def deleteGroup():
    groups = getGroups()
    for key, value in groups.items():
        print(key,"-",value)

    print("\t-----DELETING-----\n")
    groupToDelete = int(input("Enter group id: "))
    if groupToDelete not in groups.keys():
        print("The group is not existing!")
    else:
        query = f"DELETE FROM grp WHERE group_id = {groupToDelete}"
        cur.execute(query)
        mariadb_connection.commit()
        print("Succecfully deleted group",groups[groupToDelete])


def searchGroup():
    groups = getGroups()

    print("\t-----SEARCHING-----\n")
    groupToDisplay = int(input("Enter group id"))

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