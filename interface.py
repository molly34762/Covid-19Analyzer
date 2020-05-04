import os
# stdscr.clear()
# stdscr.refresh()

def clear():
    os.system('clear')

def mainMenu():
    clear()
    print("HOME")
    print("1. NEW QUERY")
    print("2. HISTORY")
    print("3. DATA SET INFO")
    print("4. EXIT")
    while True:
        try:
            selection=int(input("Enter choice: "))
            if selection == 1:
                MakeNewQuery()
                break
            elif selection == 2:
                History()
                break
            elif selection == 3:
                DatasetInfo()
                break
            elif selection == 4:
                exit
            else:
                print("Invalid choice. Enter 1-4")
                mainMenu()
        except ValueError:
            print("Invalid choice. Enter 1-4")
    exit
        
def MakeNewQuery():
    clear()
    print("NEW QUERY")
    anykey=input("Press anything to return to main menu \n")
    mainMenu()

def History():
    clear()
    print("HISTORY")
    anykey=input("Press anything to return to main menu \n")
    mainMenu()

def DatasetInfo():
    clear()
    print("DATA SET INFO")
    anykey=input("Press anything to return to main menu \n")
    mainMenu()

mainMenu()