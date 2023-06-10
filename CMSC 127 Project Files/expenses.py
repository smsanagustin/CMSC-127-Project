import signupLoginMenu
import friends
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

def getGroupMembers(groupChoice):
    members = {} # stores friends of user
    # get all friends of user
    query = f"select user.user_id, name from user join belongsTo where user.user_id = belongsTo.user_id and group_id = {groupChoice};"
    cur.execute(query)
    for row in cur.fetchall():
        id = row[0]
        name = row[1]
        # add each friend to list
        members[id] = name

    return members

def getAffiliatedGroups(userChoice):
    groups = {} # stores friends of user
    # get all friends of user
    query = f"select grp.group_id, grp.group_name from grp join belongsTo where grp.group_id = belongsTo.group_id and user_id = {userChoice}"
    cur.execute(query)
    for row in cur.fetchall():
        id = row[0]
        name = row[1]
        # add each friend to list
        groups[id] = name

    return groups

# get all expense
def getAllExpenses(userChoice):
    # stores user's expenses
    usersExpenses = {}
    
    # get all expenses of currently logged in user
    query = f"select expense_id, expense_name from expense where user_id = {userChoice}"
    cur.execute(query)

    allExpenses = cur.fetchall()

    for row in allExpenses:
        expense_id = row[0]
        group_name = row[1]

        usersExpenses[expense_id] = group_name

    return(usersExpenses)


def getMaxExpenseId():
	select_maxTaskNo = "SELECT MAX(expense_id) FROM expense"
	cur.execute(select_maxTaskNo)

	for i in cur:
		highest = i
		break
	
	if highest[0]==None:
		return 0
	return (highest[0])


def addExpense(userChoice):
    while True:
        print("\nWho would you share the expense with? \n"
            "[1] To a Friend\n" 
            "[2] To a Group\n"
            "[0] Back\n"
        )
        addExpenseOption = input("Enter choice: ")

        # User has a shared expense with a friend
        if addExpenseOption == '1':

            print("List of Friends: \n")

            allFriends = friends.getFriends(userChoice)

            for id in allFriends.keys():
                print(f"{id} - {allFriends[id]}")

            # users can select a user to log in from list of users
            # in the tuple [0] is ID and [1] is name
            friend_id = int(input("\nSelect a friend id: "))

            if friend_id not in allFriends.keys():
                print("Please select a correct friend id.")
                continue
            else:
                while True:
                    try: 
                        total_value = float(input("Enter total expenses: "))
                        break
                    except ValueError:
                        print("Enter decimals only!")
                while True: 
                    cash_flow = input("Are you the financer? (yes or no): ")#+ if expecting to receive from others, - if you need to pay
                    if (cash_flow not in ["yes", "no"]):
                        print("Invalid input!")
                    else:
                        break
                split_method = input("Split Method (custom or equal): ")

                if split_method == 'custom':
                    split_percentage = float(input("Your expense percentage allocation (in decimal): "))
                    if cash_flow == 'yes':
                        split_value = (total_value*split_percentage)
                        break
                    elif cash_flow == 'no':
                        split_value = (total_value*split_percentage*-1)
                elif split_method == 'equal':
                    if cash_flow == 'yes':
                        split_value = (total_value/2)
                    elif cash_flow == 'no':
                        split_value = (total_value/2*-1)
                else:
                    print("Invalid input!")

                expense_name = input("Enter expense label: ")


                try: 
                    #TODO: insert new user tuple sql query here
                    # query = f"INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id,friend_id) VALUES ({total_value},CURDATE(),false,{split_method},{split_value},{expense_name},{userChoice},{friend_id})"
                    query = f"INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id,friend_id) VALUES ({total_value}, CURDATE(),0,'{split_method}',{split_value},'{expense_name}',{userChoice},{friend_id});"
                    # INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id,friend_id) VALUES (200,CURDATE(),0,'equal',+100,'Mcdo',1,2)
                    cur.execute(query)
                    con.commit()
                except mysql.connector.Error as e: 
                    print(f"Error: {e}")
                break
        # user has a shared expense with a group
        elif addExpenseOption == '2':
            allGroups = getAffiliatedGroups(userChoice)
          
            print("List of Groups: \n")

            allGroups = getAffiliatedGroups(userChoice)

            for id in allGroups.keys():
                print(f"{id} - {allGroups[id]}")

            # users can select a user to log in from list of users
            # in the tuple [0] is ID and [1] is name
            group_id = int(input("\nSelect a group id: "))

            if group_id not in allGroups.keys():
                print("Please select a correct group id.")
                continue
            else:
                while True:
                    try: 
                        total_value = float(input("Enter total expenses: "))
                        break
                    except ValueError:
                        print("Enter decimals only!")
                        
                expense_name = input("Enter expense label: ")

                # insert select sql query here
                allMembers = getGroupMembers(group_id)

                memberCount = len(allMembers)

                for id in allMembers.keys():
                    print(f"{id} - {allMembers[id]}")

                financer = int(input("\nSelect the group financer id: "))

                split_method = input("\nSplit Method (custom or equal): ")

                # splitting expenses with a group in custom percentage
                if split_method == 'custom':
                    split_percentage_list = {}
                    split_percentage_list[userChoice] = float(input("\nYour expense percentage allocation (in decimal): "))
                    
                    if userChoice == financer:
                        split_value = (total_value*split_percentage_list[userChoice])
                    else:
                        split_value = (total_value*split_percentage_list[userChoice]*-1)

                    expense_name = input("Enter expense label: ")
                    query = f"INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id) VALUES ({total_value}, CURDATE(),0,'{split_method}',{split_value},'{expense_name}',{userChoice})"
                    cur.execute(query)


                    # insert select sql query here
                    # allMembers = groups.getGroupMembers(group_id)

                    for id in allMembers.keys():
                        # print(f"{id} - {allMembers[id]}\n")
                        split_percentage_list[id] = float(input(f"{allMembers[id]}'s expense percentage allocation (in decimal): "))
                    
                        if id == financer:
                            split_value = (total_value*split_percentage_list[id])
                        else:
                            split_value = (total_value*split_percentage_list[id]*-1)

                        query = f"INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id) VALUES ({total_value}, CURDATE(),0,'{split_method}',{split_value},'{expense_name}',{id})"
                        cur.execute(query)

                # splitting expenses with a group equally    
                elif split_method == 'equal':
                    
                    print(financer)
                    for id in allMembers.keys():
                        print(id)
                        if id == financer:
                            split_value = (total_value/memberCount)
                        else:
                            split_value = (total_value/memberCount*-1)

                        query = f"INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id) VALUES ({total_value}, CURDATE(),0,'{split_method}',{split_value},'{expense_name}',{id})"
                        cur.execute(query)

                else:
                    print("Invalid input!")

                expense_name = input("Enter expense label: ")

                lastExpenseId = getMaxExpenseId()

                try: 
                    #TODO: insert new user tuple sql query here
                    # query = f"INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id) VALUES ({total_value}, CURDATE(),0,'{split_method}',{split_value},'{expense_name}',{userChoice})"
                    query2 = f"INSERT INTO group_has_expense (group_id,expense_id) VALUES ({group_id},{lastExpenseId})"
                    # INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id) VALUES (900, CURDATE(),0,"equal",600,"1st Group Expense",1);
                    # cur.execute(query)
                    # con.commit()
                    cur.execute(query2)
                    con.commit()
                except mysql.connector.Error as e: 
                    print(f"Error: {e}")
                break
        elif addExpenseOption == '0':
            expensesManager(userChoice)
            break
        else: 
            print("Invalid Input")

def deleteExpense(userChoice):
    # get all user's expenses
    usersExpenses = getAllExpenses(userChoice)

    # show to user all expenses
    if len(usersExpenses) > 0:
        print("Your expenses: ")
        for expense_id in usersExpenses.keys():
            print(f"{expense_id} - {usersExpenses[expense_id]}")
            
        # delete expense
        while True:
            # ask user which expense to delete by id
            while True:
                try:
                    idOfExpenseToDelete = int(input("Enter id of expense to delete (Enter 0 to exit): "))
                    break
                except ValueError:
                    print("Enter integers only!")
                    
            # delete expense if it's in the list of user's expense
            if idOfExpenseToDelete in usersExpenses.keys():
                query = f"DELETE FROM expense WHERE expense_id = {idOfExpenseToDelete}"
                cur.execute(query)

                con.commit()

                print("Successfully delete expense!")

                break
            elif idOfExpenseToDelete == 0:
                print("Exiting...")
                break
            else:
                print("Invalid input!")

    else:
        print("You haven't made any expenses.")

    #Request for the expenseID to be deleted

def searchExpense(userChoice):
    # get user input to search
    nameOfExpenseToSearch = input("Enter expense name: ")

    # query from db using user input
    query = f"SELECT expense_name FROM expense WHERE expense_name LIKE '%{nameOfExpenseToSearch}%' AND user_id = {userChoice}"
    cur.execute(query)

    searchResults = cur.fetchall()

    # if there are results from search, print each result
    if len(searchResults) > 0:
        print("Search results: ")
        for row in searchResults:
            print(row[0])
    else:
        print("No group found.")

def updateExpense(userChoice):
    # print all expenses 
    usersExpenses = getAllExpenses(userChoice)

    # if user has expenses, print each
    if len(usersExpenses) > 0:
        for expense_id in usersExpenses.keys():
            print(f"{expense_id} - {usersExpenses[expense_id]}")

        # ask user for input
        while True:
            while True:
                try: 
                    idOfExpenseToUpdate = int(input("Enter id of expense to update (Enter 0 to exit): "))
                    break
                except ValueError:
                    print("Invalid input!")

            # update expense if it exists
            if idOfExpenseToUpdate in usersExpenses.keys():
                # query to update
                query = f"UPDATE expense SET isSettled = 1 WHERE expense_id = {idOfExpenseToUpdate}"
                cur.execute(query)

                con.commit()
                print("Expense successfully updated!")
                break
            
            elif idOfExpenseToUpdate == 0:
                print("Exiting...")
                break

            else:
                print("Expense does not exist!")

    else:
        print("You have made no expenses yet.")


def expensesManager(userChoice, userName):
    while True:
        print("\nWhat would you like to do?\n"
            "[1] Add Expense\n"
            "[2] Delete Expense\n"
            "[3] Search Expense\n"
            "[4] Update Expense\n"
            "[0] Back"
            )
        expenseManagerOption = input("\nEnter choice: ")

        if expenseManagerOption == '0':

            signupLoginMenu.mainPage(userChoice, userName)
            break
        elif expenseManagerOption == '1':
            addExpense(userChoice)
    
            signupLoginMenu.mainPage(userChoice, userName)
            break
        elif expenseManagerOption == '2':
            deleteExpense(userChoice)
            
            signupLoginMenu.mainPage(userChoice, userName)
            break
        elif expenseManagerOption == '3':
            searchExpense(userChoice)

            signupLoginMenu.mainPage(userChoice, userName)
            break
        elif expenseManagerOption == '4':
            updateExpense(userChoice)

            signupLoginMenu.mainPage(userChoice, userName)
            break
        else:
            print("Invalid Input!")
            
            signupLoginMenu.mainPage(userChoice, userName)
            break