import mysql.connector

# make new connection
connection = mysql.connector.connect(
    user="root",
    password="ilove127",
    host="localhost",
    database="cmsc127group3")

cursor = connection.cursor()

# get all the groups created by the user
def getGroups(userChoice):
    groups = {}
    try: 
        #TODO: insert new user tuple sql query here
        query = f"select * from grp join belongsTo on grp.group_id = belongsTo.group_id where user_id = {userChoice}"
        cursor.execute(query)
        for group in cursor:
            groups[group[0]] = group[1]
        return groups
    except mysql.connector.Error as e: 
        print(f"Error: {e}")  

# prints all groups of user
def viewAllGroups(userChoice):
    groups = getGroups(userChoice)
    
    for key, value in groups.items():
        print(key, "-", value)

def createGroup(userChoice):
    print("\t-----ADDING-----\n")
    group_name = input("Enter groupname (Enter 0 to exit): ")
    if group_name == "0":
        print("Exiting...")
    else:
        try: 
            query = f"INSERT INTO grp (group_name) VALUES ('{group_name}')"
            cursor.execute(query) 
            query = f"SELECT MAX(group_id) FROM grp"
            cursor.execute(query)
            idTuple = cursor.fetchone()
            latestGroupId = idTuple[0]
            query = f"INSERT INTO belongsTo (user_id,group_id) VALUES ({userChoice},{latestGroupId})"
            cursor.execute(query)
            connection.commit()
            print(group_name,"has been created")
        except mysql.connector.Error as e: 
            print(f"Error: {e}")

def deleteGroup(userChoice):
    groups = getGroups(userChoice)
    viewAllGroups(userChoice)

    print("\t-----DELETING-----\n")
    groupToDelete = int(input("Enter group id: "))
    if groupToDelete not in groups.keys():
        print("The group is not existing!")
    else:
        query = f"DELETE FROM grp WHERE group_id = {groupToDelete}"
        cursor.execute(query)
        connection.commit()
        print("Succecfully deleted group",groups[groupToDelete])


def searchGroup(userChoice):
    groups = getGroups(userChoice)
    
    # if there are groups, ask for user input:
    if len(groups) > 0:
        print("\t-----SEARCHING-----\n")
        groupToDisplay = input("Type the name of the group: ")

        query = f"select * from grp where group_name like '%{groupToDisplay}%'"
        cursor.execute(query)

        # if there are results, print them
        result = cursor.fetchall()
        if len(result) > 0:
            print("Found these groups: ")
            for row in result:
                group_id = row[0]
                group_name = row[1]
                print(f"{group_id} - {group_name}")
        else:
            print("No group with that name was found.")
    else:
        print("There are no groups yet!")

def updateGroup(userChoice):
    groups = getGroups(userChoice)
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
                addFriendToGroup(userChoice, group_id, groups[group_id])
            elif action == 2:
                removeFriendFromGroup()
            elif action == 3:
                renameGroup(group_id, groups[group_id])
            else:
                print("Invalid Choice!")
    # Rename the group, add friend to the group, remove friend to a group

def addFriendToGroup(userId, groupId, groupName):
    import friends
    friendsOfUser = friends.getFriends(userId)
    for key,value in friendsOfUser.items():
        print(key, "-", value)

    friendId = int(input("Enter friend ID: "))
    if friendId in friendsOfUser.keys():
        query = f"INSERT INTO belongsTo (user_id,group_id) VALUES ({friendId},{groupId})"
        cursor.execute(query)
        print(f"{friendsOfUser[friendId]} has been added to {groupName}")
    else:
        print("Friend does not exist!")


def removeFriendFromGroup(userId, groupId, groupName):
    import friends
    friendsOfUser = friends.getFriends(userId)
    for key,value in friendsOfUser.items():
        print(key, "-", value)
    friendId = int(input("Enter friend ID: "))

    if friendId in friendsOfUser.keys():
        query = f"DELETE FROM belongsTo (user_id,group_id) VALUES ({friendId},{groupId})"
        cursor.execute(query)
        print(f"{friendsOfUser[friendId]} has been removed from {groupName}")
        # should catch the case where the friend cannot be removed from the group if the group still
        #  has an unsettled expense
    else:
        print("Friend does not exist!")

def renameGroup(groupId, oldGroupName):
    newGroupName = input("Enter new group name: ")
    query = f"UPDATE grp SET group_name = '{newGroupName}' WHERE group_id = {groupId}"
    cursor.execute(query)
    connection.commit()
    print(f"Group {oldGroupName} has been successfully renamed to {newGroupName}")

def viewAllGroupsWithOB(userId):
    query = f"""SELECT group_name, SUM(new.cash_flow) as 'Balance' FROM (SELECT grp.group_name, h.cash_flow FROM group_has_expense h JOIN expense e ON h.expense_id = e.expense_id JOIN grp on h.group_id = grp.group_id WHERE h.user_id = 1) as new;"""
    cursor.execute(query)
    

    print("Groups with outstanding balance")
    for row in cursor.fetchall():
        group_name = row[0]
        balance = row[1]
        print(f"{group_name} - {balance}")

        
def groupsManager(userChoice, userName):
    while True:
        print("\n What would you like to do?\n"
            "[1] Add Group\n"
            "[2] Delete Group\n"
            "[3] Search Group\n"
            "[4] View All Groups\n"
            "[5] Update Group\n"
            "[6] View All Groups with an Outstanding Balance\n"
            "[0] Back"
            )
        groupManagerOption = input("\nEnter choice: ")
        
        if groupManagerOption == '0':

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice,userName)
            break
        elif groupManagerOption == '1':
            createGroup(userChoice)
        elif groupManagerOption == '2':
            deleteGroup(userChoice)
        elif groupManagerOption == '3':
            searchGroup(userChoice)
        elif groupManagerOption == '4':
            viewAllGroups(userChoice)
        elif groupManagerOption == '5':
            updateGroup(userChoice)
        elif groupManagerOption == '6':
            viewAllGroupsWithOB(userChoice)
        else:
            print("Invalid Input!")