import expenses
import friends
import groups
import mysql.connector

mariadb_connection = mysql.connector.connect(
    user="root",
    password="elvinbautista",
    host="localhost",
    database="cmsc127group3")

cur = mariadb_connection.cursor()

#populatedUsers = ["Silent Marc","Mae Laban but e","Jon w/o h"]
populatedUsers = []
populatedExpenses = []
populatedGroups = []


def login():
    
    while True:
        
        # shows a list of users
        query = "SELECT user_id, name FROM user"
        cur.execute(query)

        # display all users
        for row in cur.fetchall():
            id = row[0]
            name = row[1]
            populatedUsers.append(row)
            # print each instance to the console
            print(f"{id} - {name}")


        # users can select a user to log in from list of users
        # in the tuple [0] is ID and [1] is name
        userChoice = input("\nSelect User: ") 
        print(userChoice)
        if int(userChoice) > len(populatedUsers) or int(userChoice) < 0:
            print("Invalid Input")
        elif userChoice == '0':
            mainMenuLoop()
            break
        else:
            print("\nSuccessfully Logged In:",populatedUsers[int(userChoice)-1][1])
            mainPage(populatedUsers[int(userChoice)-1][0],populatedUsers[int(userChoice)-1][1])
            break


#NOTE: userChoice should be the PK of the current user?
def mainPage(userChoice,userName):    
    print("\nCurrent user is:",userName)

    #select an option to manage a user's expenses, friends, or groups
    while True:
        print('\nEXPENSES MANAGEMENT SYSTEM')
        print(
            "[1] EXPENSE MANAGER\n"
            "[2] FRIEND MANAGER\n"
            "[3] GROUP MANAGER\n"
            "[0] SIGN OUT"
            )
        managerChoice = input("\nEnter choice: ")

        if managerChoice == '1':
            import expenses
            #params should be current user pk and expense table?
            expenses.expensesManager(userChoice, populatedExpenses)
            break
        elif managerChoice == '2':
            import friends
            #params should be current user pk and users table?
            friends.friendsManager(userChoice, populatedUsers)
            break
        elif managerChoice == '3':
            import groups
            #params should be current user pk and groups table?
            groups.groupsManager(userChoice, populatedGroups)
            break
        elif managerChoice == '0':
            mainMenuLoop()
            break
        else:
            print("Invalid Input")


def signup():
    inputName = input("Name: ")
    inputUsername = input("Enter Username: ")
    inputPassword = input("Enter password: ")

    try: 
        #TODO: insert new user tuple sql query here
        query = f"INSERT INTO user (name, username, password) VALUES ('{inputName}', '{inputUsername}', '{inputPassword}')"
        cur.execute(query)
        mariadb_connection.commit()
    except mysql.connector.Error as e: 
        print(f"Error: {e}")
    mainMenuLoop()


def mainMenuLoop():
    while True:
        print('\nPERSONAL EXPENSES TRACKER')
        print(
        "[1] Login\n"
        "[2] Create Account\n"
        "[0] Exit\n"
        )

        mainMenuChoice = input("Enter Choice: ")

        if mainMenuChoice == "1":
            login()
            break
        elif mainMenuChoice == "2":
            signup()
            break
        elif mainMenuChoice == "0":
            break
        else:
            print("Invalid Input")