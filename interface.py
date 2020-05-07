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
history = []
tick = '\u2588'
smallTick = '\u258C'

#Menu items 
homeMenu = ['HOME', '--------', emptySpace, '1. NEW QUERY', '2. HISTORY', '3. DATA SET INFO', emptySpace, '4. Exit']
queryMenu = ['New Query', '--------', emptySpace, 'INSTRUCTIONS', emptySpace, '1. EXPLORE', '2. COMPARE', '3. INVESTIGATE', emptySpace,'4. HOME']
exploreMenu = ['EXPLORE', '--------', emptySpace, 'INSTRUCTIONS', emptySpace, '1. STATE', '2. COUNTY', '3. State Over Time', '4. County Over Time','5. STATE BY DATE', '6. COUNTY BY DATE', emptySpace, '7. HOME']
compareMenu = ['COMPARE', '--------', emptySpace, 'INSTRUCTIONS', emptySpace, '1. DISTANCE BETWEEN TWO COUNTIES', '2. COMPARISON BETWEEN TWO COUNTIES', emptySpace, '3. HOME']
investigateMenu = ['INVESTIGATE', '--------', emptySpace, 'INSTRUCTIONS', emptySpace, '1. APPROXIMATE VULNERABLE POPULATIONS', '2. CALCULATE HOUSEHOLD DENSITIES', emptySpace, '3. HOME']

def drawMenu(menu):
    clear()
    size = os.get_terminal_size()
    print('\n')
    print('#' * size[0])
    for menuItem in menu:
        print('# ' + menuItem.center(size[0] - 3, ' ') + '#')
    print('#' * size[0])
    print('\n')

#######################################################################
## Main Menu ##
def mainMenu():
    drawMenu(homeMenu)

    #menu options
    selections = [MakeNewQuery, History, DatasetInfo]
    try:
        selection=int(input("Enter choice: "))
        if(selection < 0 or selection > len(selections)):
            print("Invalid choice. Enter 1-4")
            time.sleep(2)
            mainMenu()
        else:
            selections[selection]()
    except ValueError:
        print("Invalid choice. Enter 1-4")
        time.sleep(2)
        mainMenu()

#Make a New Query Menu
def MakeNewQuery():
    drawMenu(queryMenu)

    #Menu Options
    try:
        selection=int(input("Enter choice: "))
        if selection == 1:
            Explore()
        elif selection == 2:
            Compare()
        elif selection == 3:
            Investigate()
        elif selection == 4:
            mainMenu()
        else:
            print("Invalid choice. Enter 1-4")
            time.sleep(2)
            MakeNewQuery()
    except ValueError:
        print("Invalid choice. Enter 1-4")
        time.sleep(2)
        MakeNewQuery()

#######################################################################
## Explore Menu ##
def Explore():
    drawMenu(exploreMenu)

    #Menu Options
    try:
        selection=int(input("Enter choice: "))
        if selection == 1:
            ConfirmedCasesByState()
        elif selection == 2:
            ConfirmedCasesByCounty()
        elif selection == 3:
            StateOverTime()
        elif selection == 4:
            CountyOverTime()
        elif selection == 5:
            ConfirmedCasesByDateAndState()
        elif selection == 6:
            ConfirmedCasesByDateAndCounty()
        elif selection == 7:
            mainMenu()
        else:
            print("Invalid choice. Enter 1-7")
            time.sleep(2)
            MakeNewQuery()
    except ValueError:
        print("Invalid Input")
        time.sleep(2)
        MakeNewQuery()

#Find the number of confirmed cases by the state name 
def ConfirmedCasesByState():
    #Get user input
    state = InputState("Enter state: ")

    #Create and execute the query string
    queryString = """SELECT SUM(confirmed) FROM CountyConfirmed
                     WHERE stateName = %s
                     AND date = (SELECT MAX(date) FROM CountyConfirmed)"""
    cursor.execute(queryString, (state,))
    records = cursor.fetchall()
    size = os.get_terminal_size()

    #Print output
    print('\n')
    print('#' * size[0])
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    for row in records:
        result = "There are {} confirmed cases in {} state.".format(str(row[0]), state)
        history.append(result)
        print('# ' + result.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + newQueryMsg.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + '1. Yes'.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + '2. No'.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('#' * size[0])
    print('\n')
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
    queryString = """SELECT SUM(confirmed)
                     FROM CountyConfirmed
                     WHERE stateName = %s
                     AND countyName = %s
                     AND date = (SELECT MAX(date) FROM CountyConfirmed);"""
    cursor.execute(queryString, (state, county))
    records = cursor.fetchall()
    size = os.get_terminal_size()

    #Print output
    print('\n')
    print('#' * size[0])
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    for row in records:
        result = "There are {} confirmed cases in {}, {}.".format(str(row[0]), county, state)
        history.append(result)
        print('# ' + result.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + newQueryMsg.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + '1. Yes'.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + '2. No'.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('#' * size[0])
    print('\n')
    redo = int(input("Enter choice: "))
    if redo == 1:
        Explore()
    else:
        mainMenu()
        return 

#View a histogram of the confirmed cases over time in a state
def StateOverTime():
    #Get user input
    state = InputState("Enter state: ")

    #Create and execute a query string
    queryString = """SELECT CountyConfirmed.date, SUM(CountyConfirmed.confirmed) AS confirmedSum
                     FROM CountyConfirmed WHERE stateName = %s
                     AND confirmed != 0 GROUP BY date ORDER BY date"""
    cursor.execute(queryString, (state,))
    records = cursor.fetchall()
    size = os.get_terminal_size()

    #Print output
    print('\n')
    print('#' * size[0])
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')

    lgbSize = size[0] * .85
    barFactor = records[len(records) - 1][1] / lgbSize

    #Format bars in graph
    day = 0
    for row in records:
        if day % 7 == 0:
            if int(int(row[1])/barFactor) > 0:
                barRow = "# <" + str(row[0]) + ">: " + tick * int(int(row[1])/barFactor) + " " + str(row[1])
                barPaddingAmount = size[0] - len(barRow) - 1
                print(barRow + barPaddingAmount*' ' + "#")
                print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
            else:
                print("# <" + str(row[0]) + ">: " + smallTick + " " + str(row[1]))
                print('')    
        day = day + 1
            
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + newQueryMsg.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + '1. Yes'.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + '2. No'.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('#' * size[0])
    print('\n')
    redo = int(input("Enter choice: "))
    if redo == 1:
        Explore()
    else:
        mainMenu()
        return 

#Find the number of confirmed cases by entering a state name, county name, and date
def ConfirmedCasesByDateAndCounty():
    #Get user input
    state = InputState("Enter state: ")
    county = InputCounty("Choose a county: ", state)
    date = InputDate("Enter date (YYYY-MM-DD): ")

    #Create and execute a query string
    queryString = """SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = %s AND countyName = %s AND date = %s"""
    cursor.execute(queryString, (state, county, date))
    records = cursor.fetchall()
    size = os.get_terminal_size()

    #Print output
    print('\n')
    print('#' * size[0])
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    for row in records:
        result = "{} confirmed cases in {}, {} on {}.".format(str(row[0]), county, state, date)
        history.append(result)
        print('# ' + result.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + newQueryMsg.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + '1. Yes'.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + '2. No'.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('#' * size[0])
    print('\n')
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
    queryString = """SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = %s AND date = %s"""
    cursor.execute(queryString, (state, date))
    records = cursor.fetchall()
    size = os.get_terminal_size()

    #Print output
    print('\n')
    print('#' * size[0])
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    for row in records:
        result = "{} total confirmed cases in {} by {}.".format(str(row[0]), state, date)
        history.append(result)
        print('# ' + result.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + newQueryMsg.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + '1. Yes'.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + '2. No'.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('#' * size[0])
    print('\n')
    redo = int(input("Enter choice: "))
    if redo == 1:
        Explore()
    else:
        mainMenu()
        return 

#######################################################################
## Compare Menu ##
def Compare():    
    clear()
    size = os.get_terminal_size()
    print('\n' * 2)
    print('#' * size[0])
    for menuItem in compareMenu:
        print('# ' + menuItem.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('#' * size[0])
    print('\n')

    #Menu options
    while True:
        try:
            selection=int(input("Enter choice: "))
            if selection == 1:
                DistanceBetweenTwoCounties()
                break
            elif selection == 2:
                compareCounties()
                break
            elif selection == 3:
                mainMenu()
                break
            else:
                print("Invalid choice. Enter 1-2")
                time.sleep(2)
                MakeNewQuery()
                break
        except ValueError:
            print("Invalid choice. Enter 1-2")
    exit

#Find the distance between two counties
def DistanceBetweenTwoCounties():
    #Get user input
    state1 = InputState("Enter the first state: ")
    county1 = InputCounty("Choose the first county: ", state1)
    state2 = InputState("Enter the second state: ")
    county2 = InputCounty("Enter the second county: ", state2)

    #Create and execute a query string
    queryString = """SELECT 3963 * ACOS((SIN(RADIANS(c1.lat)) * SIN(RADIANS(c2.lat))) + COS(RADIANS(c1.lat)) * COS(RADIANS(c2.lat))*COS(RADIANS(c2.long) - RADIANS(c1.long)))
                     as miles
                     FROM County as c1, County as c2
                     WHERE c1.countyName LIKE %s
                        AND c1.stateName LIKE %s
                        AND c2.countyName LIKE %s
                        AND c2.stateName LIKE %s"""
    cursor.execute(queryString, (county1, state1, county2, state2))
    records = cursor.fetchall()

    #Print output
    for row in records:
        print("The distance between " + county1 + " and " + county2 + " is " + str(round(row[0], 2)) + " miles")

#View and compare information between two counties
def compareCounties():
    #Get user input
    state1 = InputState("Enter the first state: ")
    county1 = InputCounty("Choose the first county: ", state1)
    state2 = InputState("Enter the second state: ")
    county2 = InputCounty("Enter the second county: ", state2)
    
    #Create queries to obtain information
    confirmQuery = """SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = %s AND countyName = %s"""
    deathQuery = """SELECT SUM(deaths) FROM CountyDeaths WHERE stateName = %s AND countyName = %s"""
    countyQuery = ("""SELECT CountyData.totalPop, CountyData.numHouseholds, CountyData.pctMale,
                        CountyData.medianAge, CountyData.pctUnder18, CountyData.pctOver65,
                        CountyData.pctWhite, CountyData.pctBlackAA , CountyData.pctIndianAlaskanNative , CountyData.pctAsian,
                        CountyData.pctHawaiianPacificIslander, CountyData.pctOtherRace, CountyData.precentHispanicLatino
                      FROM CountyData JOIN County
                        ON CountyData.countyName = County.countyName AND CountyData.StateName = County.StateName
                      WHERE CountyData.countyName = %s AND CountyData.stateName = %s """)

    #Execute queries
    cursor.execute(confirmQuery, (state1, county1))
    confirmedCase1Query = cursor.fetchall()
    cursor.execute(confirmQuery, (state1, county1))
    confirmedCase2Query = cursor.fetchall()
    cursor.execute(deathQuery, (state1, county1))
    deathCase1Query = cursor.fetchall()
    cursor.execute(deathQuery, (state2, county2))
    deathCase2Query = cursor.fetchall()
    cursor.execute(countyQuery, (county1, state1))
    county1InfoQuery = cursor.fetchall()
    cursor.execute(countyQuery, (county2, state2))
    county2InfoQuery = cursor.fetchall()

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
    print(t)
    
#######################################################################
## Investigate Menu ##
def Investigate():    
    clear()
    size = os.get_terminal_size()
    print('\n' * 2)
    print('#' * size[0])
    for menuItem in investigateMenu:
        print('# ' + menuItem.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('#' * size[0])
    print('\n')

    #Menu options
    while True:
        try:
            selection=int(input("Enter choice: "))
            if selection == 1:
                TotalCountyPopulationOver65()
                break
            elif selection == 2:
                HouseholdDensity()
                break
            elif selection == 3:
                mainMenu()
                break
            else:
                print("Invalid choice. Enter 1-3")
                time.sleep(2)
                MakeNewQuery()
                break
        except ValueError:
            print("Invalid choice. Enter 1-3")
    exit

#Find the amount of people over 65 in a county 
def TotalCountyPopulationOver65():
    #Get user input
    state = InputState("Enter state: ")
    county = InputCounty("Choose a county: ", state)

    #Create and execute a query string
    queryString = """SELECT (pctOver65/100) * totalPop FROM CountyData WHERE countyName = %s AND stateName  = %s"""
    cursor.execute(queryString, (county, state))
    records = cursor.fetchall()

    #Print output
    for row in records:
        print("There are " + str(row[0]) + " people who are over 65 years old in " + county)

#Find the top10 housesehold densities and display the county name and state name
def HouseholdDensity():
    #Create and execute query string
    queryString = ("""SELECT CountyData.countyName, CountyData.stateName,  
                        CAST((CAST(totalPop AS float)/numHouseholds) as NUMERIC(5,2)) as householdDensity, 
                        c.confirmed, d.deaths 
                      FROM CountyData, 
	                    (SELECT countyName, stateName, SUM(confirmed) as confirmed FROM CountyConfirmed
	                        GROUP BY (countyName, stateName)) as c,
	                    (SELECT countyName, stateName, SUM(deaths) as deaths FROM CountyDeaths
	                        GROUP BY (countyName, stateName)) as d
                      WHERE CountyData.countyName = c.countyName
                        AND CountyData.stateName = c.stateName
                        AND CountyData.countyName = d.countyName
                        AND CountyData.stateName = d.stateName
                      ORDER BY householdDensity DESC
                      LIMIT 10""" )
    cursor.execute(queryString)
    records = cursor.fetchall()
    
    #Print output
    t = PrettyTable(['County Name', 'State Name', 'Household Density', 'Confirmed Cases', 'Confirmed Deaths'])
    for i in range(10):
        t.add_row([ records[i][0], records[i][1], records[i][2], records[i][3], records[i][4]])
    print(t)

#View user's history
def History():
    clear()
    size = os.get_terminal_size()
    print('\n')
    print('#' * size[0])
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    for element in history:
        result = element
        print('# ' + result.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + 'Press anything to return to main menu'.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('#' * size[0])
    print('\n')
    returnKey = input("")
    mainMenu()
    return
        
#View information about the two datasets
def DatasetInfo():
    clear()
    print("DATA SET INFO")
    anykey=input("Press anything to return to main menu \n")
    mainMenu()

#Input state name
def InputState(input_string):
    queryString = """SELECT DISTINCT stateName FROM CountyData"""
    cursor.execute(queryString)
    records = cursor.fetchall()
    while True:
        state = input(input_string)
        if (state,) in records:
            return state
        print("That's not a supported state.")

#Input county name
def InputCounty(input_string, state):
    queryString = """SELECT County.countyName FROM CountyData 
                     JOIN County 
                     ON CountyData.countyName = County.countyName AND CountyData.StateName = County.StateName
                     WHERE County.stateName = %s
                     AND EXISTS (SELECT * FROM CountyConfirmed as cc WHERE cc.confirmed != 0 AND cc.stateName = County.stateName AND cc.countyName =  County.countyName)
                     ORDER BY County.countyName"""

    cursor.execute(queryString, (state,))

    print("Recorded counties in " + state + ":\n")
    records = cursor.fetchall()
    line = ""
    size = os.get_terminal_size()
    for r in records:
        if(line == ""):
            line = r[0]
        else:
            if(len(line) + len(r[0]) + 2 > size[0]):
                print(line)
                line = r[0]
            else:
                line = line + ", " + r[0]
    print('')
    while True:
        county = input(input_string)
        if (county,) in records:
            return county
        print("That's not a supported county.")

#Input date
def InputDate(input_string):
    queryString = """SELECT MAX(date) FROM countyConfirmed"""
    cursor.execute(queryString)
    maxdate = cursor.fetchone()

    queryString = """SELECT MIN(date) FROM countyConfirmed"""
    cursor.execute(queryString)
    mindate = cursor.fetchone()

    queryString = """SELECT * FROM countyConfirmed WHERE date = %s"""
    while True:
        date = input(input_string)
        cursor.execute(queryString, (date,))
        res = cursor.fetchone()
        if(res is not None):
            return date
        print("That date is not within the valid date range: " + mindate[0].strftime("%Y-%m-%d") + " - " + maxdate[0].strftime("%Y-%m-%d"))

#main function
if __name__ == '__main__':
    mainMenu()
