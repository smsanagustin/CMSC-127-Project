import expenses
import friends
import groups

import mysql.connector

mariadb_connection = mysql.connector.connect(
    user="db_user",
    password="db_user_passwd",
    host="localhost",
    database="cmsc127group3")

create_cursor = mariadb_connection.cursor()

#populatedUsers = ["Silent Marc","Mae Laban but e","Jon w/o h"]
populatedUsers = []
populatedExpenses = []
populatedGroups = []


def login():
    
    while True:
        print('\nList of Users')
        for x in range(0, len(populatedUsers)):
            print('['+ str(x+1) +']', populatedUsers[x]['name'])
        print("[0] Back")

        userChoice = input("\nSelect User: ") 
        if int(userChoice) > len(populatedUsers) or int(userChoice) < 0:
            print("Invalid Input")
        elif userChoice == '0':
            mainMenuLoop()
            break
        else:
            print("\nSuccessfully Logged In:",populatedUsers[int(userChoice)-1]['name'])
            mainPage(populatedUsers[int(userChoice)-1]['name'])
            break


#NOTE: userChoice should be the PK of the current user?
def mainPage(userChoice):    
    print("\nCurrent user is:",userChoice)

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
    inputUsername = input("Enter Username: ")

    # userInstance = {
    #     #TODO: Fill this up w/ user attributes/columns
    #     # Name serves as the PK? for now
    #     # 'name' : inputUsername:
        
        
    #     }
    
    # populatedUsers.append(userInstance) 


    #TODO: insert new user tuple sql query here
    try: 
        create_cursor.execute("INSERT INTO employees (first_name,last_name) VALUES (?, ?)", ("Maria","DB")) 
    except mariadb.Error as e: 
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