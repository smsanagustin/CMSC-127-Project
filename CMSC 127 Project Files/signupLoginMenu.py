import expenses
import friends
import groups
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

#populatedUsers = ["Silent Marc","Mae Laban but e","Jon w/o h"]
populatedUsers = {}
populatedExpenses = []
# populatedGroups = []


def login():
    while True:
        # shows a list of users
        query = "SELECT user_id, name FROM user"
        cur.execute(query)

        # display all users
        for row in cur.fetchall():
            id = row[0]
            name = row[1]
            populatedUsers[id] = name
            # print each instance to the console
            print(f"{id} - {name}")
        print("0 - Back")

        # users can select a user to log in from list of users
        # in the tuple [0] is ID and [1] is name
        userChoice = int(input("\nSelect User: "))
        print(userChoice)

        if userChoice == 0:
            mainMenuLoop()
            break
        elif userChoice not in populatedUsers.keys():
            print("Invalid Input")
        else:
            print(f"\nSuccessfully Logged In: {populatedUsers[userChoice]}")
            mainPage(userChoice, populatedUsers[userChoice])
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
            expenses.expensesManager(userChoice, userName)
            break
        elif managerChoice == '2':
            import friends
            #params should be current user pk and users table?
            friends.friendsManager(userChoice, userName)
            break
        elif managerChoice == '3':
            import groups
            #params should be current user pk and groups table?
            groups.groupsManager(userChoice, userName)
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
        con.commit()
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