import mysql.connector

mariadb_connection = mysql.connector.connect(
    user="root",
    password="ilove127",
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

def viewAllGroups():
    groups = getGroups()
    
    for key, value in groups.items():
        print(key, "-", value)

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
    groupToDisplay = int(input("Enter group id: "))

    if groupToDisplay not in groups.keys():
        print("The group is not existing!")
    else:
        print(groupToDisplay,"-",groups[groupToDisplay])

def updateGroup():
    groups = getGroups()
    print("\t-----UPDATING-----\n")
    for key, value in groups.items():
        print(key,"-",value)
    group_id = int(input("Enter group id: "))

    if group_id not in groups.keys():
        print("The group is not existing!")
    else:
        print(f"\t-----UPDATING {groups[group_id]}-----\n")
        while True:
            print(f"[1] Add a friend to a {groups[group_id]}")
            print(f"[2] Remove a friend from {groups[group_id]}")
            print(f"[3] Rename {groups[group_id]}")
            print("[0] Back")
            action = int(input("Enter the number of the action you wish to perform: "))

            if action == 0:
                break
            elif action == 1:
                addFriendToGroup()
            elif action == 2:
                removeFriendFromGroup()
            elif action == 3:
                renameGroup(group_id, groups[group_id])
            else:
                print("Invalid Choice!")


    # Rename the group, add friend to the group, remove friend to a group

def addFriendToGroup(groupId):
    idOfFriendToRemove = int(input("Enter user ID: "))

def removeFriendFromGroup(groupId):
    print("Update group still WIP!")
    
def renameGroup(groupId, oldGroupName):
    newGroupName = input("Enter new group name: ")
    query = f"UPDATE grp SET group_name = '{newGroupName}' WHERE group_id = {groupId}"
    cur.execute(query)
    mariadb_connection.commit()
    print(f"Group {oldGroupName} has been successfully renamed to {newGroupName}")



def groupsManager(userChoice, userName):
    while True:
        print("\n What would you like to do?\n"
            "[1] Add Group\n"
            "[2] Delete Group\n"
            "[3] Search Group\n"
            "[4] View All Groups\n"
            "[5] Update Group\n"
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
            viewAllGroups()
        elif groupManagerOption == '5':
            updateGroup()
        else:
            print("Invalid Input!")