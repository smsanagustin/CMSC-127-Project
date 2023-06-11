import signupLoginMenu
import friends
import mysql.connector

# make new connection
connection = mysql.connector.connect(
    user="root",
    password="ilove127",
    host="localhost",
    database= "cmsc127group3",
    )

# perform database operations here:
# used to execute sql queries on the databases
cursor  = connection.cursor()

def getGroupMembers(groupChoice):
    members = {} # stores friends of user
    # get all friends of user
    query = f"select user.user_id, name from user join belongsTo where user.user_id = belongsTo.user_id and group_id = {groupChoice};"
    cursor.execute(query)
    for row in cursor.fetchall():
        id = row[0]
        name = row[1]
        # add each friend to list
        members[id] = name

    return members

def getAffiliatedGroups(userChoice):
    groups = {} # stores friends of user
    # get all friends of user
    query = f"select grp.group_id, grp.group_name from grp join belongsTo where grp.group_id = belongsTo.group_id and user_id = {userChoice}"
    cursor.execute(query)
    for row in cursor.fetchall():
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
    cursor.execute(query)

    allExpenses = cursor.fetchall()

    for row in allExpenses:
        expense_id = row[0]
        group_name = row[1]

        usersExpenses[expense_id] = group_name

    return(usersExpenses)


def getMaxExpenseId():
	select_maxTaskNo = "SELECT MAX(expense_id) FROM expense"
	cursor.execute(select_maxTaskNo)

	for i in cursor:
		highest = i
		break
	
	if highest[0]==None:
		return 0
	return (highest[0])


def addExpense(userChoice, userName):
    # loop for the add expense functionality
    while True:
        print("\nWho would you share the expense with? \n"
            "[1] To a Friend\n" 
            "[2] To a Group\n"
            "[0] Back\n"
        )
        addExpenseOption = input("Enter choice: ")

        # User has a shared expense with a friend
        if addExpenseOption == '1':

            # get a list of friends
            allFriends = friends.getFriends(userChoice)

            # if user has friends, display them
            if len(allFriends) > 0:
                print("\nList of Friends: ")

                # Display user friends
                for id in allFriends.keys():
                    print(f"{id} - {allFriends[id]}")

                # users can select a user to log in from list of users
                # in the tuple [0] is ID and [1] is name
                friend_id = int(input("\nSelect a friend id: "))
            
                # input error catch
                if friend_id not in allFriends.keys():
                    print("Please select a correct friend id.")
                    continue
                # requesting add expense parameters
                else:
                    # request expense name
                    expense_name = input("Enter expense label: ")

                    # loop for requesting valid expense input
                    while True:
                        try: 
                            total_value = float(input("Enter total expenses: "))
                            break
                        except ValueError:
                            print("Enter decimals only!")

                    # loop for requesting valid financer response
                    while True: 
                        cash_flow = input("Are you the financer? (yes or no): ")#+ if expecting to receive from others, - if you need to pay
                        if (cash_flow not in ["yes", "no"]):
                            print("Invalid input!")
                        else:
                            break
                    
                    # loop for requesting valid split method response
                    while True:
                        split_method = input("Split Method (custom or equal): ")
                        if split_method == 'custom':
                            # loop for requesting valid percentage input for custom split
                            while True:
                                split_percentage = float(input("What percentage will you pay? (w/o % sign): "))
                                if split_percentage not in range (0,100):
                                    print("Please input percentage values from 0-100.")
                                else:
                                    if cash_flow == 'yes':
                                        split_value = round((total_value*(split_percentage/100)),2)
                                        break
                                    elif cash_flow == 'no':
                                        split_value = round((total_value*(split_percentage/100)*-1),2)
                                        break
                            break
                        elif split_method == 'equal':
                            if cash_flow == 'yes':
                                split_value = round((total_value/2),2)
                                break
                            elif cash_flow == 'no':
                                split_value = round((total_value/2*-1),2)
                                break
                        else:
                            print("Invalid input!")


                    try: 
                        # executes arguments pushing to mariadb
                        query = f"INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id,friend_id) VALUES ({total_value}, CURDATE(),0,'{split_method}',{split_value},'{expense_name}',{userChoice},{friend_id});"
                        cursor.execute(query)
                        connection.commit()
                    except mysql.connector.Error as e: 
                        print(f"Error: {e}")
                    break
            else:
                print("You have no friends yet!")

        # user has a shared expense with a group
        elif addExpenseOption == '2':
            allGroups = getAffiliatedGroups(userChoice)
          
            #prints the user's affiliated groups
            print("\nList of Groups: ")

            allGroups = getAffiliatedGroups(userChoice)

            for id in allGroups.keys():
                print(f"{id} - {allGroups[id]}")

            # users can select a user to log in from list of users
            # in the tuple [0] is ID and [1] is name
            group_id = int(input("\nSelect a group id: "))

            # error catch for group id selection
            if group_id not in allGroups.keys():
                print("Please select a correct group id.")
                continue
            else:
                # request expense name input
                expense_name = input("Enter expense label: ")

                # loop for requesting valid expense input
                while True:
                    try: 
                        total_value = float(input("Enter total expenses: "))
                        break
                    except ValueError:
                        print("Enter decimals only!")
                        
                # insert select sql query here
                allMembers = getGroupMembers(group_id)

                memberCount = len(allMembers)

                # prints selected group's members
                print(f"\nList of {allGroups[group_id]} members:")
                for id in allMembers.keys():
                    print(f"{id} - {allMembers[id]}")

                # loop for requesting a valid financer id
                while True:
                    financer = int(input("Select the group financer id: "))
                    if financer not in allMembers.keys():
                        print("Please select a valid member id")
                    else:
                        break

                
                while True:
                    split_method = input("Split Method (custom or equal): ")

                    # splitting expenses with a group in custom percentage
                    if split_method == 'custom':
                        split_percentage_list = {}

                        lastExpenseId = getMaxExpenseId()+1

                        # iterates for every member of the group
                        for id in allMembers.keys():

                            #loop for requesting valid percentage input for custom split
                            while True:
                                split_percentage_list[id] = float(input(f"What percentage will {allMembers[id]} pay? (w/o % sign): "))
                                if split_percentage_list[id] not in range (0,100):
                                    print("Please input percentage values from 0-100.")
                                else:
                                    if id == financer:
                                        split_value = round((total_value*(100-split_percentage_list[id])/100),2)
                                        break
                                    else:
                                        split_value = round((total_value*(split_percentage_list[id]/100)*-1),2)
                                        break
                            

                            query = f"INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id) VALUES ({total_value}, CURDATE(),0,'{split_method}',{split_value},'{expense_name}',{id})"
                            cursor.execute(query)
                            # query2 = f"INSERT INTO group_has_expense (group_id,expense_id) VALUES ({group_id},{lastExpenseId})"
                            # cur.execute(query2)
                            # con.commit()
                            # lastExpenseId = lastExpenseId + 1
                        break

                    # splitting expenses with a group equally    
                    elif split_method == 'equal':

                        lastExpenseId = getMaxExpenseId()+1
                        
                        # print(financer)
                        for id in allMembers.keys():
                            # print(id)
                            if id == financer:
                                split_value = round((total_value/memberCount)*(memberCount-1),2)
                            else:
                                split_value = round((total_value/memberCount*-1),2)

                        
                            query = f"INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id) VALUES ({total_value}, CURDATE(),0,'{split_method}',{split_value},'{expense_name}',{id})"
                            cursor.execute(query)
                            # query2 = f"INSERT INTO group_has_expense (group_id,expense_id) VALUES ({group_id},{lastExpenseId})"
                            # cur.execute(query2)
                            # con.commit()
                            # lastExpenseId = lastExpenseId + 1
                        break
                    else:
                        print("Invalid input!")

                # expense_name = input("Enter expense label: ")

                # lastExpenseId = getMaxExpenseId()

                try: 
                    query2 = f"INSERT INTO group_has_expense (group_id,expense_id) VALUES ({group_id},{financer})"
                    cursor.execute(query2)
                    connection.commit()
                except mysql.connector.Error as e: 
                    print(f"Error: {e}")
                break
        elif addExpenseOption == '0':
            expensesManager(userChoice, userName)
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
                cursor.execute(query)

                connection.commit()

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
    cursor.execute(query)

    searchResults = cursor.fetchall()

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
                cursor.execute(query)

                connection.commit()
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
            # close the connection
            cursor.close()
            connection.close()

            signupLoginMenu.mainPage(userChoice, userName)
            break
        elif expenseManagerOption == '1':
            addExpense(userChoice, userName)
    
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