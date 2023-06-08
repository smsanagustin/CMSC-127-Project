# user of login info
# userChoice - id of the logged in user
import mysql.connector
import signupLoginMenu

mariadb_connect = mysql.connector.connect(
    user="root",
    password="ilove127",
    host="localhost",
    database="cmsc127group3"
)

# create cursor object
cur = mariadb_connect.cursor()

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
        
    # add friend as users friend (if they're not friends yet)
    query = f'''
        INSERT INTO friendsWith (user1, user2)
        SELECT {userChoice}, {idOfFriendToAdd}
        WHERE NOT EXISTS (
            SELECT 1
            FROM friendsWith
            WHERE (user1 = {userChoice} AND user2 = {idOfFriendToAdd})
        );
        '''
    cur.execute(query)
    
    query = f'''
        INSERT INTO friendsWith (user1, user2)
        SELECT {idOfFriendToAdd}, {userChoice}
        WHERE NOT EXISTS (
            SELECT 1
            FROM friendsWith
            WHERE (user1 = {idOfFriendToAdd} AND user2 = {userChoice})
        );
        '''
    cur.execute(query)
    mariadb_connect.commit()
    
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

            return
        elif friendManagerOption == '1':
            addFriend(userChoice)
            
            return
        elif friendManagerOption == '2':
            deleteFriend(populatedUsers)

            return
        elif friendManagerOption == '3':
            searchFriend(populatedUsers)
            
            return
        elif friendManagerOption == '4':
            updateFriend(populatedUsers)

            return
        else:
            print("Invalid Input!")

            return