expenseInstance = {
    #TODO: Fill this up w/ expense attributes/columns
    'expenseID' : '',
    'total' : 0
}

# get all expense
def getAllExpenses(userChoice):
    # stores user's expenses
    usersExpenses = {}
    
    # get all expenses of currently logged in user
    query = f"select expense_id, expense_name from expense where user_id = $userChoice"
    cur.execute()

    allExpenses = cur.fetchall()

    for row in cur.fetchall:
        expense_id = row[0]
        group_name = row[1]

        usersExpenses[expense_id] = group_name

    return(usersExpenses)


def addExpense(populatedExpenses):
    while True:
        print("\nWho would you share the expense with?\n"
            "[1] To a Friend\n" 
            "[2] To a Group\n"
        )
        addExpenseOption = input("Enter choice: ")

        if addExpenseOption == '1':
            #TODO: Add expense attributes inputs here
            print("Add Expense with a Friend still WIP!")
            break
        elif addExpenseOption == '2':
            #TODO: Add expense attributes inputs here
            print("Add Expense with a Group still WIP!")
            break
        else: 
            print("Invalid Input")

def deleteExpense(populatedExpenses):
    print("Delete Expense still WIP!")

    #TODO: Request for the expenseID to be deleted

def searchExpense(populatedExpenses):
    print("Search Expense still WIP!")

    #TODO: Request for the expenseID to be searched
    #then display the details of the expense

def updateExpense(populatedExpenses):
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
            addExpense(populatedExpenses)
    
            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif expenseManagerOption == '2':
            deleteExpense(populatedExpenses)
            
            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif expenseManagerOption == '3':
            searchExpense(populatedExpenses)

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif expenseManagerOption == '4':
            updateExpense(populatedExpenses)

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        else:
            print("Invalid Input!")
            
            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break