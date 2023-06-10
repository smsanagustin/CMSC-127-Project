import expenses
import friends
import groups
import mysql.connector

connection = mysql.connector.connect(
    user="root",
    password="ilove127",
    host="localhost",
    database="cmsc127group3")

cursor = connection.cursor()

#populatedUsers = ["Silent Marc","Mae Laban but e","Jon w/o h"]
populatedUsers = {}
populatedExpenses = []
# populatedGroups = []


def login():
        # get the number of users
        query = "SELECT count(user_id) FROM user"
        cursor.execute(query)
        count = cursor.fetchone()

        # if there are users, let the current user log in
        if count[0] > 0:

            # users can select a user to log in from list of users
            userNameInput = input("Enter your username (Enter 0 to exit): ")

            # if user enters 0, exit prompt
            if userNameInput == "0":
                mainMenuLoop()
            # if username exists, ask for user's password
            else:
                userCredentials = {}
                query = f"SELECT username, password FROM user WHERE username = %s"
                cursor.execute(query, (userNameInput,))

                # if users exists in db, save their credentials
                result = cursor.fetchone()
                if result is not None:
                    username = result[0]
                    password = result[1]
                    userCredentials[username] = password

                    # ask for password
                    userPasswordInput = input("Enter your password: ")

                    # check if the password matches
                    if userPasswordInput == userCredentials[username]:
                        # get user's name and id
                        query = f"SELECT user_id, name FROM user WHERE username = %s"
                        cursor.execute(query, (userNameInput,))
                        result = cursor.fetchone()

                        user_id = result[0]
                        name = result[1]

                        print(f"Successfully logged in: {name}")
                        # call mainpage and pass current user's id and their name 
                        mainPage(user_id, name)
                    else:
                        print("Wrong password!")
                        mainMenuLoop()

                else:
                    print("username not found!")
                    mainMenuLoop()

            # if userChoice == '0':
            #     mainMenuLoop()
            # else:
            #     # ask for the password of the chosen user
            #     # userPasswordInput = input("Enter your password: ")

            #     # check if the password matches the chosen id
            #     # query = "SELECT password FROM "

            #     print(f"\nSuccessfully Logged In: {populatedUsers[userChoice]}")

            #     # call mainpage and pass current user's id (userChoice) and their name 
            #     mainPage(userChoice, usersDict[userChoice])
        else:
            print("There are no users yet. Create one to login.")
            mainMenuLoop()

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
        cursor.execute(query)
        connection.commit()

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
            # close cursor and connections
            cursor.close()
            connection.close()
            break
        else:
            print("Invalid Input")