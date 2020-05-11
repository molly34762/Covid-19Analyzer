import os
import time
import psycopg2
import psycopg2.extras
from prettytable import PrettyTable
import database as db

#Database connection string
connection_string = "host='localhost' dbname='covid_census' user='covid_census' password='covid_census'"
cursor = psycopg2.connect(connection_string).cursor()

#Clears user's screen
def clear():
    os.system('clear')

#Repetitive strings used
newQueryMsg = 'Would you like to perform another query?'
emptySpace = ' '
history = ['HISTORY', '---------', emptySpace]
tick = '\u2588'
smallTick = '\u258C'

#Menu items 
homeMenu = ['HOME', '---------', emptySpace, '1. NEW QUERY', '2. HISTORY', '3. DATA SET INFO', emptySpace, '4. Exit']
queryMenu = ['NEW QUERY', '---------', emptySpace, 'PERFORM A NEW QUERY - SELECT 1-3', emptySpace, '1. EXPLORE', '2. COMPARE', '3. INVESTIGATE', emptySpace,'4. HOME']
exploreMenu = ['EXPLORE', '---------', emptySpace, 'EXPLORE CONFIRMED COVID-19 CASES - SELECT 1-6', emptySpace, '1. STATE', '2. COUNTY', '3. STATE OVER TIME', '4. COUNTY OVER TIME','5. STATE BY DATE', '6. COUNTY BY DATE', emptySpace, '7. HOME']
compareMenu = ['COMPARE', '---------', emptySpace, 'COMPARE TWO COUNTIES - SELECT 1-2', emptySpace, '1. CALCULATE DISTANCE BETWEEN COUNTIES', '2. COMPARE COUNTY ANALYTICS', emptySpace, '3. HOME']
investigateMenu = ['INVESTIGATE', '---------', emptySpace, 'FURTHER DATA ANALYSIS - SELECT 1-2', emptySpace, '1. APPROXIMATE VULNERABLE POPULATIONS', '2. TOP 10 HOUSEHOLD DENSITIES', emptySpace, '3. HOME']

def displayStartOfBox():
    size = os.get_terminal_size()
    print('\n')
    print('#' * size[0])
    print('# ' + ' '.center(size[0] - 3) + '#')

def displayEndOfBox():
    size = os.get_terminal_size()
    print('# ' + ' '.center(size[0] - 3) + '#')
    print('#' * size[0])
    print('\n')

def displayLinesInBox(lines):
    clear()
    displayStartOfBox()
    size = os.get_terminal_size()
    for line in lines:
        prettyWrapCenterText(line, size[0])
    displayEndOfBox()

def prettyWrapCenterText(text, maxSize):
    line = ""
    for word in text.split():
        if(len(line) + len(word) >= maxSize - 5):
            print("# " + line.center(maxSize - 5) + "  #")
            line = word
        else:
            line = line + " " + word
    print("# " + line.center(maxSize - 5) + "  #")

def menuSelect(selections, recursefunct):
    try:
        selection=int(input("Enter choice: "))
        if(selection < 1 or selection > len(selections)):
            print("Invalid choice. Enter 1-" + str(len(selections)))
            time.sleep(2)
            recursefunct()
        else:
            selections[selection-1]()
    except ValueError:
        print("Invalid choice. Enter 1-" + str(len(selections)))
        time.sleep(2)
        recursefunct()

################################   MENUS   #######################################
## Main Menu ##
def mainMenu():
    displayLinesInBox(homeMenu)
    selections = [MakeNewQuery, History, DatasetInfo, clear] #clear does nothing, falls through and exits application.
    menuSelect(selections, mainMenu)

## Make a New Query Menu ##
def MakeNewQuery():
    displayLinesInBox(queryMenu)
    selections = [Explore, Compare, Investigate, mainMenu]
    menuSelect(selections, MakeNewQuery)

## Explore Menu ##
def Explore():
    displayLinesInBox(exploreMenu)
    selections = [ConfirmedCasesByState, ConfirmedCasesByCounty, StateOverTime, CountyOverTime, ConfirmedCasesByDateAndState, ConfirmedCasesByDateAndCounty, mainMenu]
    menuSelect(selections, Explore)

## Investigate Menu ##
def Investigate():
    displayLinesInBox(investigateMenu)
    selections = [TotalCountyPopulationOver65, HouseholdDensity, mainMenu]
    menuSelect(selections, Investigate)

## Compare Menu ##
def Compare():
    displayLinesInBox(compareMenu)
    selections = [DistanceBetweenTwoCounties, compareCounties, mainMenu]
    menuSelect(selections, Compare)

################################   QUERIES   #######################################
#Find the number of confirmed cases by the state name 
def ConfirmedCasesByState():
    #Get user input
    state = InputState("Enter state: ")

    #Create and execute the query string\
    records = db.ConfirmedCasesByStateQuery(state)

    #Print output
    lines = []
    for row in records:
        result = "There are {} confirmed cases in {} State.".format(str(row[0]), state)
        history.append(result)
        lines.append(result)
    lines.append(emptySpace)
    lines.append(newQueryMsg)
    lines.append('1. Yes')
    lines.append('2. No')
    displayLinesInBox(lines)

    redo = int(input("Enter choice: "))
    if redo == 1:
        Explore()
    else:
        mainMenu()
        return 

#Find the number of confirmed cases by the state name and county name
def ConfirmedCasesByCounty():
    #Get user input
    state = InputState("Enter state: ")
    county = InputCounty("Choose a county: ", state)

    #Create and execute the query string
    records = db.ConfirmedCasesByCountyQuery(state, county)

    #Print output
    lines = []
    for row in records:
        result = "There are {} confirmed cases in {}, {}.".format(str(row[0]), county, state)
        history.append(result)
        lines.append(result)
    lines.append(emptySpace)
    lines.append(newQueryMsg)
    lines.append('1. Yes')
    lines.append('2. No')
    displayLinesInBox(lines)

    redo = int(input("Enter choice: "))
    if redo == 1:
        Explore()
    else:
        mainMenu()
        return 

#View a histogram of the confirmed cases over time in a state
def StateOverTime():
    state = InputState("Enter state: ")

    records = db.StateOverTimeQuery(state)

    size = os.get_terminal_size()
    displayStartOfBox()
    print('# ' + ("Total confirmed Cases in " + state + " over time.").center(size[0] - 3) + '#')
    print('# ' + "--------".center(size[0] - 3) + '#')
    print('# ' + emptySpace.center(size[0] - 3) + '#')
    drawDateValueHistogram(records)
    print('# ' + emptySpace.center(size[0] - 3) + '#')
    print('# ' + newQueryMsg.center(size[0] - 3) + '#')
    print('# ' + '1. Yes'.center(size[0] - 3) + '#')
    print('# ' + '2. No'.center(size[0] - 3) + '#')
    displayEndOfBox()

    redo = int(input("Enter choice: "))
    if redo == 1:
        Explore()
    else:
        mainMenu()
        return 


#View a histogram of the confirmed cases over time in a state
def CountyOverTime():
    state = InputState("Enter state: ")
    county = InputCounty("Choose a county: ", state)

    records = db.CountyOverTimeQuery(state, county)

    size = os.get_terminal_size()
    displayStartOfBox()
    print('# ' + ("Total confirmed Cases in " + state + ", " + county + " over time.").center(size[0] - 3) + '#')
    print('# ' + "--------".center(size[0] - 3) + '#')
    print('# ' + emptySpace.center(size[0] - 3) + '#')
    drawDateValueHistogram(records)
    print('# ' + emptySpace.center(size[0] - 3) + '#')
    print('# ' + newQueryMsg.center(size[0] - 3) + '#')
    print('# ' + '1. Yes'.center(size[0] - 3) + '#')
    print('# ' + '2. No'.center(size[0] - 3) + '#')
    displayEndOfBox()
            
    redo = int(input("Enter choice: "))
    if redo == 1:
        Explore()
    else:
        mainMenu()
        return 

def drawDateValueHistogram(records):
    size = os.get_terminal_size()
    lgbSize = size[0] - 27 #enough space for number labels less than 10 billion
    barFactor = lgbSize / records[len(records) - 1][1]

    #Format bars in graph
    day = -(len(records) % 7) + 1 #from most recent date in weekly increments
    for row in records:
        if day % 7 == 0:
            if int(int(row[1]) * barFactor) > 0:
                barRow = "#   <" + str(row[0]) + ">: " + tick * int(int(row[1])*barFactor) + " " + str(row[1])
                barPaddingAmount = size[0] - len(barRow) - 1
                print(barRow + barPaddingAmount*' ' + "#")
                print('# ' + emptySpace.center(size[0] - 3) + '#')
            else:
                barRow = "#   <" + str(row[0]) + ">: " + smallTick + " " + str(row[1])
                barPaddingAmount = size[0] - len(barRow) - 1
                print(barRow + barPaddingAmount*' ' + "#")
                print('# ' + emptySpace.center(size[0] - 3) + '#')
        day = day + 1

#Find the number of confirmed cases by entering a state name, county name, and date
def ConfirmedCasesByDateAndCounty():
    #Get user input
    state = InputState("Enter state: ")
    county = InputCounty("Choose a county: ", state)
    date = InputDate("Enter date (YYYY-MM-DD): ")

    #Create and execute a query string
    records = db.ConfirmedCasesbyDateAndCount(state, county, date)
    size = os.get_terminal_size()

    lines = []
    for row in records:
        result = "{} confirmed cases in {}, {} on {}.".format(str(row[0]), county, state, date)
        history.append(result)
        lines.append(result)
    lines.append(emptySpace)
    lines.append(newQueryMsg)
    lines.append('1. Yes')
    lines.append('2. No')
    displayLinesInBox(lines)

    redo = int(input("Enter choice: "))
    if redo == 1:
        Explore()
    else:
        mainMenu()
        return 

#Find the number of confirmed cases by entering a state name and a date
def ConfirmedCasesByDateAndState():
    #Get user input
    state = InputState("Enter state: ")
    date = InputDate("Enter date (YYYY-MM-DD): ")

    #Create and execute a query string
    records = db.ConfirmedCasesbyDateandState(state, date)
    size = os.get_terminal_size()

    lines = []
    
    #Print output
    for row in records:
        result = "{} total confirmed cases in {} by {}.".format(str(row[0]), state, date)
        history.append(result)
        lines.append(result)
    lines.append(emptySpace)
    lines.append(newQueryMsg)
    lines.append('1. Yes')
    lines.append('2. No')
    displayLinesInBox(lines)

    redo = int(input("Enter choice: "))
    if redo == 1:
        Explore()
    else:
        mainMenu()
        return 

#Find the distance between two counties
def DistanceBetweenTwoCounties():
    #Get user input
    state1 = InputState("Enter the first state: ")
    county1 = InputCounty("Choose the first county: ", state1)
    state2 = InputState("Enter the second state: ")
    county2 = InputCounty("Enter the second county: ", state2)

    #Create and execute a query string
    records = db.DistanceBetweenCountiesQuery(state1, county1, state2, county2)

    #Print output
    lines = []
    for row in records:
        result = "The distance between " + county1 + " and " + county2 + " is " + str(round(row[0], 2)) + " miles"
        history.append(result)
        lines.append(result)
    lines.append(emptySpace)
    lines.append(newQueryMsg)
    lines.append('1. Yes')
    lines.append('2. No')
    displayLinesInBox(lines)

    redo = int(input("Enter choice: "))
    if redo == 1:
        Compare()
    else:
        mainMenu()
        return 

#View and compare information between two counties
def compareCounties():
    #Get user input
    state1 = InputState("Enter the first state: ")
    county1 = InputCounty("Choose the first county: ", state1)
    state2 = InputState("Enter the second state: ")
    county2 = InputCounty("Enter the second county: ", state2)

    #Execute queries
    confirmedCase1Query = db.ConfirmedCasesByCountyQuery(state1, county1)
    confirmedCase2Query = db.ConfirmedCasesByCountyQuery(state2, county2)
    deathCase1Query = db.DeathsByCountyQuery(state1, county1)
    deathCase2Query = db.DeathsByCountyQuery(state2, county2)
    county1InfoQuery = db.CountyInfoQuery(state1, county1)
    county2InfoQuery = db.CountyInfoQuery(state2, county2)

    #Print output
    t = PrettyTable(['Statistic', county1 + ", " + state1, county2 + ", " + state2])
    t.add_row(['Confirmed Cases', confirmedCase1Query[0][0], confirmedCase2Query[0][0]])
    t.add_row(['Death Cases', deathCase1Query[0][0], deathCase2Query[0][0]])
    t.add_row(['Total Population', county1InfoQuery[0][0], county2InfoQuery[0][0]])
    t.add_row(['Number of Households', county1InfoQuery[0][1],county2InfoQuery[0][1] ])
    t.add_row(['Percentage Male', str(county1InfoQuery[0][2]) + " %", str(county2InfoQuery[0][2]) + " %"])
    t.add_row(['Median Age', county1InfoQuery[0][3], county2InfoQuery[0][3]])
    t.add_row(['Percentage under 18', str(county1InfoQuery[0][4]) + " %", str(county2InfoQuery[0][4]) + " %"])
    t.add_row(['Percentage over 65', str(county1InfoQuery[0][5]) + " %", str(county2InfoQuery[0][5]) + " %" ])
    t.add_row(['Percentage White', str(county1InfoQuery[0][6]) + " %", str(county2InfoQuery[0][6]) + " %"])
    t.add_row(['Percentage Black', str(county1InfoQuery[0][7]) + " %", str(county2InfoQuery[0][7]) + " %"])
    t.add_row(['Percentage pctIndianAlaskanNative', str(county1InfoQuery[0][8]) + " %" , str(county2InfoQuery[0][8]) + " %"])
    t.add_row(['Percentage pctAsian', str(county1InfoQuery[0][9]) + " %" , str(county2InfoQuery[0][9]) + " %"])
    t.add_row(['Percentage pctHawaiianPacificIslander', str(county1InfoQuery[0][10]) + " %",  str(county2InfoQuery[0][10]) + " %"])
    t.add_row(['Percentage pctOtherRace', str(county1InfoQuery[0][11]) + " %", str(county2InfoQuery[0][11]) + " %"])
    t.add_row(['Percentage precentHispanicLatino', str(county1InfoQuery[0][12]) + " %", str(county2InfoQuery[0][12]) + " %"])
    print(emptySpace)
    print(t)
    print("\n" + newQueryMsg + "\n1. Yes\n2. No")
    redo = int(input("\nEnter choice: "))
    if redo == 1:
        Compare()
    else:
        mainMenu()
        return 

#Find the amount of people over 65 in a county 
def TotalCountyPopulationOver65():
    #Get user input
    state = InputState("Enter state: ")
    county = InputCounty("Choose a county: ", state)

    #Create and execute a query string
    records = db.PopOver65Query(state, county)

    #Print output
    lines = []
    for row in records:
        result = "There are " + str(round(row[0])) + " people who are over 65 years old in " + county + ", " + state
        history.append(result)
        lines.append(result)
    lines.append(emptySpace)
    lines.append(newQueryMsg)
    lines.append('1. Yes')
    lines.append('2. No')
    displayLinesInBox(lines)

    redo = int(input("Enter choice: "))
    if redo == 1:
        Investigate()
    else:
        mainMenu()
        return 


#Find the top10 housesehold densities and display the county name and state name
def HouseholdDensity():
    #Create and execute query string
    records = db.top10HouseholdDensitiesQuery()
    
    #Print output
    print(emptySpace)
    t = PrettyTable(['County Name', 'State Name', 'Household Density', 'Confirmed Cases', 'Confirmed Deaths'])
    for i in range(10):
        t.add_row([ records[i][0], records[i][1], records[i][2], records[i][3], records[i][4]])
    print(t)
    print("\n" + newQueryMsg + "\n1. Yes\n2. No")
    redo = int(input("\nEnter choice: "))
    if redo == 1:
        Investigate()
    else:
        mainMenu()
        return 

################################   OTHER   #######################################
#View user's history
def History():
    lines = history.copy()
    lines.append(emptySpace)
    lines.append('Press anything to return to main menu')
    displayLinesInBox(lines)
    returnKey = input("")
    mainMenu()
    return
        
#View information about the two datasets
def DatasetInfo():
    lines = []
    lines.append("DATASET INFO")
    lines.append("--------")
    lines.append("")
    string1 = """The first dataset is provided by the Johns Hopkins University Center for 
                Systems Science and Engineering. It provides an account of all the confirmed cases
                and deaths concerning COVID-19, grouped both within the U.S. by county, and 
                worldwide by country. The data is updated daily and contains records from as 
                far back as January 22nd. This application focuses solely on the United States segment.
                The second dataset is provided by the U.S. census data from data.census.gov. 
                Tables covering state and county populations are used along with 
                gender, age, and race distributions within those populations."""
    lines.append(string1)
    lines.append("")
    displayLinesInBox(lines)
    anykey=input("Press anything to return to main menu \n")
    mainMenu()

################################   USER INPUT HELPERS   #######################################
#Input state name
def InputState(input_string):
    records = db.allStates()
    while True:
        state = input(input_string)
        if (state,) in records:
            return state
        print("That's not a supported state.")

#display all counties in the selected state, let the user choose one.
def InputCounty(input_string, state):
    records = db.countiesInState(state)

    print("Recorded counties in " + state + ":\n")
    any = False
    line = ""
    size = os.get_terminal_size()
    for r in records:
        any = True
        if(line == ""):
            line = r[0]
        else:
            if(len(line) + len(r[0]) + 2 > size[0]):
                print(line)
                line = r[0]
            else:
                line = line + ", " + r[0]
    print(line)
    if(not any): #no major counties in state.
        return
    print('')
    while True:
        county = input(input_string)
        if (county,) in records:
            return county
        print("That's not a supported county.")

#Input date within range
def InputDate(input_string):
    maxdate = db.maxDate()
    mindate = db.minDate()

    while True:
        date = input(input_string)
        if(db.isValidDate(date)):
            return date
        print("That date is not within the valid date range: " + mindate[0].strftime("%Y-%m-%d") + " - " + maxdate[0].strftime("%Y-%m-%d"))

################################   MAIN   #######################################
if __name__ == '__main__':
    mainMenu()
