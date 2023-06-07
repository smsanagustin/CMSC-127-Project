groupInstance = {
    #TODO: Fill this up w/ group attributes/columns
    'groupID': '',
    'name' : ''
}

def addGroup(populatedGroups):
    print("Add group still WIP!")

    #TODO: Add group inputs here

def deleteGroup(populatedGroups):
    print("Delete group still WIP!")

    #TODO: Request for the groupID to be deleted

def searchGroup(populatedGroups):
    print("Search group still WIP!")

    #TODO: Request for the groupID to be searched
    #then display the details of the group

def updateGroup(populatedGroups):
    print("Update group still WIP!")

    #TODO: Request for the groupID to be updated
    #then display input fields for the new values

def addFriendtoGroup(populatedGroups):
    print("Update group still WIP!")

    #TODO: Request for the groupID to be updated
    #TODO: Request for the userID to be added
    #then display prompt if successful


def groupsManager(userChoice, populatedGroups):
    while True:
        print("\n What would you like to do?\n"
            "[1] Add Group\n"
            "[2] Delete Group\n"
            "[3] Search Group\n"
            "[4] Update Group\n"
            "[5] Add Friend to a Group\n"
            "[0] Back"
            )
        groupManagerOption = input("\nEnter choice: ")
        
        if groupManagerOption == '0':

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif groupManagerOption == '1':
            addGroup(populatedGroups)

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif groupManagerOption == '2':
            deleteGroup(populatedGroups)

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif groupManagerOption == '3':
            searchGroup(populatedGroups)

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif groupManagerOption == '4':
            updateGroup(populatedGroups)

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        elif groupManagerOption == '5':
            addFriendtoGroup(populatedGroups)

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break
        else:
            print("Invalid Input!")

            import signupLoginMenu
            signupLoginMenu.mainPage(userChoice)
            break