# user of login info
# userChoice - id of the logged in user
import mysql.connector

# connects to a mariadb database
con = mysql.connector.connect(
    user="root",
    password="ilove127",
    host="localhost",
    database= "cmsc127group3",
    )

# perform database operations here:
# used to execute sql queries on the databases
cur  = con.cursor()

# lets logged in user add a user
def addFriend(userChoice):
    # get all users from the db
    query = "SELECT user_id, name FROM user"
    cur.execute(query)

    # create list of friends that can be added
    listOfFriendsToAdd = []

    # display all users
    for row in cur.fetchall():
        id = row[0]
        name = row[1]

        # print user if it's not the logged in user or the admin
        if userChoice != id and id !=1: 
            listOfFriendsToAdd.append(id)
            print(f"ID: {id}, Name: {name}")

    # ask user which friend to add
    while True:
        idOfFriendToAdd = int(input("Enter ID of the friend you want to add: "))

        if idOfFriendToAdd in listOfFriendsToAdd:
            break
        else:
            print("Friend does not exist!")
        
    # add friend as users friend
    query = f"INSERT INTO friendsWith (user1, user2) VALUES ({userChoice},{idOfFriendToAdd})"
    cur.execute(query)

    con.commit()
    
    print("Added friend successfully!")

def deleteFriend(populatedUsers):
    print("Delete friend still WIP!")

    #TODO: Request for the friendID to be deleted

def searchFriend(populatedUsers):
    print("Search friend still WIP!")
            
    #TODO: Request for the friendID to be searched
    #display input fields for the friend details

def updateFriend(populatedUsers):
    print("Update friend still WIP!")

    #TODO: Request for the friendID to be updated
    #then display input fields for the new values

def friendsManager(userChoice):
    while True:
        print("\n What would you like to do?\n"
            "[1] Add Friend\n"
            "[2] Delete Friend\n"
            "[3] Search Friend\n"
            "[4] Update Friend Details\n"
            "[0] Back"
            )
        friendManagerOption = input("\nEnter choice: ")
        
        if friendManagerOption == '0':

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif friendManagerOption == '1':
            addFriend(userChoice)
            
            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif friendManagerOption == '2':
            # deleteFriend(populatedUsers)

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif friendManagerOption == '3':
            # searchFriend(populatedUsers)
            
            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif friendManagerOption == '4':
            # updateFriend(populatedUsers)

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        else:
            print("Invalid Input!")

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
