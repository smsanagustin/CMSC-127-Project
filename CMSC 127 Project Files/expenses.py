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

            print("\nList of Friends: ")

            allFriends = friends.getFriends(userChoice)

            # Display user friends
            for id in allFriends.keys():
                print(f"{id} - {allFriends[id]}")

            # users can select a user to log in from list of users
            # in the tuple [0] is ID and [1] is name
            while True:
                try:
                    friend_id = int(input("\nSelect a friend id (Enter 0 to exit): "))
                    break
                except ValueError:
                    print("Input integers only!")
          
            # if user chooses exit
            if friend_id == 0:
                print("Exiting...")
                break
            # input error catch
            elif friend_id not in allFriends.keys():
                print("Please select a correct friend id.")
                break
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
                            cashToPay = float(input("How much will you pay (enter exact value): "))
                            if cashToPay > total_value:
                                print("Your input is not within the acceptable range.")
                            else:
                                if cash_flow == 'yes':
                                    split_value = round(total_value-cashToPay,2)
                                    break
                                elif cash_flow == 'no':
                                    split_value = round((cashToPay*-1),2) 
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
                    print("Successfully added expense!")
                except mysql.connector.Error as e: 
                    print(f"Error: {e}")
                break

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
                            
                            #insert group_has_expense insert query below
                            query2 = f"INSERT INTO group_has_expense (group_id,expense_id,user_id,cash_flow) VALUES ({group_id},{lastExpenseId},{id},{split_value})"
                            cursor.execute(query2)
                            connection.commit()
                            # break
                        
                            if id == userChoice:
                                query = f"INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id) VALUES ({total_value}, CURDATE(),0,'{split_method}',{split_value},'{expense_name}',{id})"
                                cursor.execute(query)
                                connection.commit()
                            # break
                        break
        
                    # splitting expenses with a group equally    
                    elif split_method == 'equal':

                        lastExpenseId = getMaxExpenseId()+1
                        
                        for id in allMembers.keys():
                            # print(id)
                            if id == financer:
                                split_value = round((total_value/memberCount)*(memberCount-1),2)
                            
                            else:
                                split_value = round((total_value/memberCount*-1),2)

                            query2 = f"INSERT INTO group_has_expense (group_id,expense_id,user_id,cash_flow) VALUES ({group_id},{lastExpenseId},{id},{split_value})"
                            cursor.execute(query2)
                            connection.commit()

                            if id == userChoice:
                                query = f"INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id) VALUES ({total_value}, CURDATE(),0,'{split_method}',{split_value},'{expense_name}',{id})"
                                cursor.execute(query)
                                connection.commit()
                        break
                    else:
                        print("Invalid input!")

                # try: 
                #     query = f"INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id) VALUES ({total_value}, CURDATE(),0,'{split_method}',{split_value},'{expense_name}',{id})"
                #     cur.execute(query)
                #     con.commit()
                # except mysql.connector.Error as e: 
                #     print(f"Error: {e}")
                break
        elif addExpenseOption == '0':
            # expensesManager(userChoice, userName)
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
        print("No expense found.")

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
                query = f"Select isSettled from expense where expense_id = {idOfExpenseToUpdate}"       
                cursor.execute(query)
                isSettled = cursor.fetchone()

                if isSettled[0] == 1:
                    print("Expense is already settled")
                else:
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
                break

    else:
        print("You have made no expenses yet.")

def viewExpensesInMonth(userChoice):
    # get all expenses of currently logged in user
    # query = f"SELECT * FROM expense WHERE user_id = {userChoice} or friend_id = {userChoice} AND isSettled = 0 AND date_incurred IN (CURDATE(),DATE_SUB(CURDATE(), INTERVAL 1 MONTH));"
    query = f"""select * from expense id 
    where user_id = {userChoice} or friend_id = {userChoice} or 
    expense_id in (select expense_id from group_has_expense where user_id = {userChoice});"""
    cursor.execute(query)

    viewExpensesInAMonth = cursor.fetchall()

    if len(viewExpensesInAMonth) > 0:
        for expense in viewExpensesInAMonth:
            print(f"{expense[2]}\n Expense ID: {expense[0]} | Expense Name: {expense[6]} \n")
    else:
        print("You haven't made expenses within this month.")

def viewExpensesWFriend(userChoice):
    # get all expenses of currently logged in user with friends
    # query = f"select * from expense join user on expense.friend_id = user.user_id where expense.user_id = {userChoice} or expense.friend_id = {userChoice} and friend_id is not null;"
    query = f"select * from expense join user u join user v on expense.user_id = u.user_id and expense.friend_id = v.user_id where expense.user_id = {userChoice} or expense.friend_id = {userChoice} and friend_id is not null;"

    # select * from expense join user u join user v on expense.user_id = u.user_id and expense.friend_id = v.user_id where expense.user_id = 1 or expense.friend_id = 1 and friend_id is not null;
    cursor.execute(query)

    expensesWFriends = cursor.fetchall()

    for expense in expensesWFriends:
        if expense[7] == userChoice:
            # print("cond1")
            print(f"Friend Name: {expense[14]} | Expense ID: {expense[0]} | Expense Name: {expense[6]} | Expense Total: {expense[1]} | Cash Flow: {expense[5]} | Settled?: {'Expense Settled' if expense[3] == 1 else 'Not Yet Settled'}")
            # totalBalance = totalBalance + expense[5]
        elif expense[8] == userChoice:
            if expense[5] < 0:
                # print("cond2.1")
                print(f"Friend Name: {expense[10]} | Expense ID: {expense[0]} | Expense Name: {expense[6]} | Expense Total: {expense[1]} | Cash Flow: {expense[1]+expense[5]} | Settled?: {'Expense Settled' if expense[3] == 1 else 'Not Yet Settled'}")
                # totalBalance = totalBalance + (expense[1]+expense[5])
            else:
                # print("cond2.2")
                print(f"Friend Name: {expense[10]} | Expense ID: {expense[0]} | Expense Name: {expense[6]} | Expense Total: {expense[1]} | Cash Flow: {(expense[1]-expense[5])*-1} | Settled?: {'Expense Settled' if expense[3] == 1 else 'Not Yet Settled'}")
                # totalBalance = totalBalance + ((expense[1]-expense[5])*-1)

def viewExpensesWGroup(userChoice):
    # get all expenses of currently logged in user with groups
    query = f"select group_name, h.expense_id, expense_name, total_value, h.cash_flow, e.isSettled from expense e join group_has_expense h join grp on e.expense_id = h.expense_id and h.group_id = grp.group_id where h.user_id = {userChoice};"
    cursor.execute(query)

    expensesWFriends = cursor.fetchall()

    for expense in expensesWFriends:
        print(f"Group Name: {expense[0]} | Expense ID: {expense[1]} | Expense Name: {expense[2]} | Expense Total: {expense[3]} | Cash Flow: {expense[4]} | Settled?: {'Expense Settled' if expense[5] == 1 else 'Not Yet Settled'}")
        # totalBalance = totalBalance + expense[5]


def viewTotalBalance(userChoice):
    totalBalance = 0

    # total balance from friends
    query = f"""select COALESCE(sum(cash_flow),0) from expense 
    where user_id = {userChoice} and cash_flow < 0 and isSettled = 0 
    or expense_id = (select expense_id from expense where friend_id = {userChoice} 
    and cash_flow > 1 and isSettled = 0);"""
    cursor.execute(query)
    result = cursor.fetchone()
    totalBalance += result[0] # add to total balance the sum of balance from friends

    # total balance from group
    query = f"select COALESCE(sum(g.cash_flow),0) from group_has_expense g JOIN expense e ON g.expense_id = e.expense_id where g.user_id = {userChoice} and g.cash_flow < 0 and e.isSettled = 0;"
    cursor.execute(query)
    result = cursor.fetchone()
    totalBalance += result[0] # add to total balance the sum of balance from friend
    totalBalance *= -1

    if totalBalance > 0:
        print(f"Your balance is: {totalBalance}")
    else:
        print("You have no balance yet.")

def expensesManager(userChoice, userName):
    while True:
        print("\nWhat would you like to do?\n"
            "[1] Add Expense\n"
            "[2] Delete Expense\n"
            "[3] Search Expense\n"
            "[4] Update Expense\n"
            "[5] View All Expenses made within a month\n"
            "[6] View all expenses made with a friend\n"
            "[7] View all expenses made with a group\n"
            "[8] View current balance from all expenses\n"
            "[0] Back"
            )
        expenseManagerOption = input("\nEnter choice: ")

        if expenseManagerOption == '0':
            signupLoginMenu.mainPage(userChoice, userName)
            break
        elif expenseManagerOption == '1':
            addExpense(userChoice, userName)
        elif expenseManagerOption == '2':
            deleteExpense(userChoice)
        elif expenseManagerOption == '3':
            searchExpense(userChoice)
        elif expenseManagerOption == '4':
            updateExpense(userChoice)
        elif expenseManagerOption == '5':
            viewExpensesInMonth(userChoice)
        elif expenseManagerOption == '6':
            viewExpensesWFriend(userChoice)
        elif expenseManagerOption == '7':
            viewExpensesWGroup(userChoice)
        elif expenseManagerOption == '8':
            viewTotalBalance(userChoice)
        else:
            print("Invalid Input!")