# user of login info
# userChoice - id of the logged in user
import mysql.connector

mariadb_connect = mysql.connector.connect(
    user="root",
    password="ilove127",
    host="localhost",
    database="cmsc127group3"
)

# create cursor object
cur = mariadb_connect.cursor()

# get user friends
def getFriends(userChoice):
    friends = {} # stores friends of user
    # get all friends of user
    query = f"select user2, name from friendsWith join user on user_id = user2 where user1 = {userChoice}"
    cur.execute(query)
    for row in cur.fetchall():
        id = row[0]
        name = row[1]
        # add each friend to list
        friends[id] = name

    return friends

# lets logged in user add a user
def addFriend(userChoice):
    userFriends = getFriends(userChoice) # user choice has the id of the logged in user

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
        while True:
            try:
                idOfFriendToAdd = int(input("Enter ID of the friend you want to add (Enter 0 to exit): "))
                break
            except ValueError:
                print("Invalid input. Please enter an integer only!")


        # add friend as users friend if its in the list
        if idOfFriendToAdd in listOfFriendsToAdd:
            # add friends if they're not friends yet
            if idOfFriendToAdd not in userFriends.keys():
                print(idOfFriendToAdd)
                query = f"INSERT INTO friendsWith (user1, user2) VALUES ({userChoice}, {idOfFriendToAdd})"
                cur.execute(query)
                
                query = f"INSERT INTO friendsWith (user1, user2) VALUES ({idOfFriendToAdd}, {userChoice})"
                cur.execute(query)
            
                mariadb_connect.commit()

                print("Added friend successfully!")

                break
            else:
                print("You are already friends with that user!")
        elif idOfFriendToAdd == userChoice:
            print("You cannot add yourself.")
        elif idOfFriendToAdd == 0 :
            print("Exiting...")
            break
        else:
            print("Friend does not exist!")

    mariadb_connect.commit()

def deleteFriend(userChoice):
    # get users friends
    userFriends = getFriends(userChoice)
    
    # print each friend
    print("Choose which friend to remove: ")
    for friend_id in userFriends.keys():
        print(f"{friend_id} - {userFriends[friend_id]}")

    # if user input a friend, remove that user as friend
    while True:
        idOfFriendToRemove = int(input("Enter id of friend to remove (Enter 0 to exit): "))

        if idOfFriendToRemove in userFriends.keys():
            # remove friend
            print("Removing friend...")

            # sql query to remove friend
            query = (f"DELETE FROM friendsWith WHERE user1 = {userChoice} and user2 = {idOfFriendToRemove}")
            cur.execute(query)

            query = (f"DELETE FROM friendsWith WHERE user1 = {idOfFriendToRemove} and user2 = {userChoice}")
            cur.execute(query)

            mariadb_connect.commit()

            print("Removed friend successfully!")
            break
        elif idOfFriendToRemove == userChoice:
            print("You cannot delete yourself.")
        elif idOfFriendToRemove == 0:
            print("Exiting...")
            break
        else:
            print("Friend does not exist!")  

def searchFriend(userChoice):
    # get user input while friend is not found
    while True:
        nameOfFriendToSearch = input("Enter name of friend (Enter 0 to exit): ")

        # query to find friend
        query = f"select user_id, name from friendsWith join user on user2=user_id where user1 = {userChoice} AND name LIKE '%{nameOfFriendToSearch}%'"
        cur.execute(query)

        # search results from query
        searchResults = cur.fetchall()

        if len(searchResults) != 0:
            print("Finding friend...")
            print("Friend/s found!")
            for row in searchResults:
                id = row[0]
                name = row[1]
                print(f"{id} - {name}")
            break
        elif nameOfFriendToSearch == "0":
            print("Exiting...")
            break
        else:
            print("Friend not found!")
            
    #TODO: Request for the friendID to be searched
    #display input fields for the friend details

# NO LONGER INCLUDED (ACCORDING TO MA'AM MONINA) WILL CLARIFY W/ SIR PRINCE
# def updateFriend(userChoice):
#     # get all friends
#     userFriends = getFriends(userChoice)
    
#     #TODO: Request for the friendID to be updated
#     #then display input fields for the new values

def friendsManager(userChoice, userName):
    while True:
        print("\n What would you like to do?\n"
            "[1] Add Friend\n"
            "[2] Delete Friend\n"
            "[3] Search Friend\n"
            # "[4] Update Friend Details\n"
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
            signupLoginMenu.mainPage(userChoice, userName)
            break
        elif friendManagerOption == '2':
            deleteFriend(userChoice)

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice, userName)
            break
        elif friendManagerOption == '3':
            searchFriend(userChoice)
            
            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice, userName)
            break
        # elif friendManagerOption == '4':
        #     updateFriend(populatedUsers)

        #     import signupLoginMenu
        #     signupLoginMenu.mainPage(userChoice, userName)
        #     break
        else:
            print("Invalid Input!")

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break