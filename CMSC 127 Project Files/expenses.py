# expenseInstance = {
#     #TODO: Fill this up w/ expense attributes/columns
#     'expenseID' : '',
#     'total' : 0
# }

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

def getMaxExpenseId():
	select_maxTaskNo = "SELECT MAX(expense_id) FROM expense"
	cur.execute(select_maxTaskNo)

	for i in cur:
		highest = i
		break
	
	if highest[0]==None:
		return 0
	return (highest[0])

def getAllFriends():
	select_maxTaskNo = "SELECT name FROM user JOIN friendsWith ON user.user_id=friendsWith.user2 WHERE friendsWith.user1=2 GROUP BY friendsWith.user2;"
	cur.execute(select_maxTaskNo)

	for i in cur:
		highest = i
		break
	
	if highest[0]==None:
		return 0
	return (highest[0])


def addExpense(userChoice, populatedExpenses):
    while True:
        print("\nWho would you share the expense with?\n"
            "[1] To a Friend\n" 
            "[2] To a Group\n"
        )
        addExpenseOption = input("Enter choice: ")

        if addExpenseOption == '1':
            #TODO: Add expense attributes inputs here
            print("Add Expense with a Friend still WIP!")

            total_value = input("Enter total expenses: ")
            split_method = input("Split Method (custom or equal):")
            cash_flow = input("Cash Flow:")
            expense_name = input("Enter expense label: ")

            
            friend_name = input("Enter friend name:")



            try: 
                #TODO: insert new user tuple sql query here
                query = f"INSERT INTO expense (total_value,date_incurred,isSettled,split_method,cash_flow,expense_name,user_id,friend_id) VALUES ('{getMaxExpenseId()}', '{total_value}', 'CURDATE()', 'False','{split_method}', '{cash_flow}', '{expense_name}','{userChoice}', '{CURDATE()}')"
                cur.execute(query)
                con.commit()
            except mysql.connector.Error as e: 
                print(f"Error: {e}")

    


            break
        elif addExpenseOption == '2':
            #TODO: Add expense attributes inputs here
            print("Add Expense with a Group still WIP!")





            break
        else: 
            print("Invalid Input")

def deleteExpense(userChoice, populatedExpenses):
    print("Delete Expense still WIP!")

    #TODO: Request for the expenseID to be deleted

def searchExpense(userChoice, populatedExpenses):
    print("Search Expense still WIP!")

    #TODO: Request for the expenseID to be searched
    #then display the details of the expense

def updateExpense(userChoice, populatedExpenses):
    print("Update Expense still WIP!")

    #TODO: Request for the expenseID to be updated
    #then display input fields for the new values


def expensesManager(userChoice, populatedExpenses):
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

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif expenseManagerOption == '1':
            addExpense(userChoice, populatedExpenses)
    
            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif expenseManagerOption == '2':
            deleteExpense(userChoice, populatedExpenses)
            
            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif expenseManagerOption == '3':
            searchExpense(userChoice, populatedExpenses)

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif expenseManagerOption == '4':
            updateExpense(userChoice, populatedExpenses)

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        else:
            print("Invalid Input!")
            
            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break