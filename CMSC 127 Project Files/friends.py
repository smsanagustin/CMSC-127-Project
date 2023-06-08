# user of login info
userInstance = {
    # TODO: Fill this up w/ user attributes/columns
    # Name serves as the PK for now?
    'name' : ''
}

def addFriend(populatedUsers):
    print("Add friend still WIP!")

    #TODO: Add friend details here    # for res in result_iterator:
    #     print("Running query: ", res)  # Will print out a short representation of the query
    #     print(f"Affected {res.rowcount} rows" )

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

def friendsManager(userChoice, populatedUsers):
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

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif friendManagerOption == '1':
            addFriend(populatedUsers)
            
            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif friendManagerOption == '2':
            deleteFriend(populatedUsers)

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif friendManagerOption == '3':
            searchFriend(populatedUsers)
            
            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif friendManagerOption == '4':
            updateFriend(populatedUsers)

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        else:
            print("Invalid Input!")

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break