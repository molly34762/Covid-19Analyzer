import os
import time
import psycopg2
import psycopg2.extras
import tabulate
from prettytable import PrettyTable


connection_string = "host='localhost' dbname='covid_census' user='covid_census' password='covid_census'"
cursor = psycopg2.connect(connection_string).cursor()
# stdscr.clear()
# stdscr.refresh()

def clear():
    os.system('clear')

homeMenu = ['HOME', '--------', '  ', '1. NEW QUERY', '2. HISTORY', '3. DATA SET INFO', ' ', '4. Exit']
queryMenu = ['New Query', '--------', '  ', 'INSTRUCTIONS', '  ', '1. EXPLORE', '2. COMPARE', '3. INVESTIGATE', ' ','4. HOME']
exploreMenu = ['EXPLORE', '--------', '  ', 'INSTRUCTIONS', '  ', '1. STATE', '2. COUNTY', '3. State Over Time', '4. County Over Time','5. STATE BY DATE', '6. COUNTY BY DATE', ' ', '7. HOME']
compareMenu = ['COMPARE', '--------', '  ', 'INSTRUCTIONS', '  ', '1. DISTANCE BETWEEN TWO COUNTIES', '2. COMPARISON BETWEEN TWO COUNTIES', ' ', '3. HOME']
investigateMenu = ['INVESTIGATE', '--------', '  ', 'INSTRUCTIONS', '  ', '1. APPROXIMATE VULNERABLE POPULATIONS', '2. CALCULATE HOUSEHOLD DENSITIES', ' ', '3. HOME']
emptySpace = ' '
newQueryMsg = 'Would you like to perform another query?'
history = []
tick = '▇'
smallTick = '▏'

#######################################################################
                                ## Menus ##
def mainMenu():
    clear()
 
    size = os.get_terminal_size()
    # print("Width: %s \nHeight: %s\n" % (size[0], size[1]))
    print('\n')
    print('#' * size[0])
    for menuItem in homeMenu:
        print('# ' + menuItem.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('#' * size[0])
    print('\n')

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
                clear()
                break
            else:
                print("Invalid choice. Enter 1-4")
                time.sleep(2)
                mainMenu()
                break
        except ValueError:
            print("Invalid choice. Enter 1-4")
    exit

def MakeNewQuery():
    clear()
    
    size = os.get_terminal_size()
    print('\n')
    print('#' * size[0])
    for menuItem in queryMenu:
        print('# ' + menuItem.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('#' * size[0])
    print('\n')

    while True:
        try:
            selection=int(input("Enter choice: "))
            if selection == 1:
                Explore()
                break
            elif selection == 2:
                Compare()
                break
            elif selection == 3:
                Investigate()
                break
            elif selection == 4:
                mainMenu()
                break
            else:
                print("Invalid choice. Enter 1-4")
                time.sleep(2)
                MakeNewQuery()
                break
        except ValueError:
            print("Invalid choice. Enter 1-4")
    exit

#######################################################################
                                ## Explore ##
def Explore():
    
    #ConfirmedCasesByDate()
    #ConfirmedCasesByCounty()
    #ConfirmedCasesByState()
    
    clear()
    size = os.get_terminal_size()
    print('\n')
    print('#' * size[0])
    for menuItem in exploreMenu:
        print('# ' + menuItem.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('#' * size[0])
    print('\n')

    while True:
        try:
            selection=int(input("Enter choice: "))
            if selection == 1:
                ConfirmedCasesByState()
                return
            elif selection == 2:
                ConfirmedCasesByCounty()
                return
            elif selection == 3:
                StateOverTime()
                return
            elif selection == 4:
                CountyOverTime()
                return
            elif selection == 5:
                ConfirmedCasesByDateAndState()
                return
            elif selection == 6:
                ConfirmedCasesByDateAndCounty()
                return
            elif selection == 7:
                mainMenu()
                return
            else:
                print("Invalid choice. Enter 1-7")
                time.sleep(2)
                MakeNewQuery()
                return
        except ValueError:
            print("Invalid Input")
    exit
        
        
def ConfirmedCasesByState():
    state = InputState()
    queryString = "SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = '" + state + "' AND date = (SELECT MAX(date) FROM CountyConfirmed)"
    cursor.execute(queryString)
    records = cursor.fetchall()

    size = os.get_terminal_size()
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


def ConfirmedCasesByCounty():
    state = InputState()
    county = InputCounty(state)
    queryString = "SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = '"+ state + "' AND countyName = '" + county + "' AND date = (SELECT MAX(date) FROM CountyConfirmed);"
    cursor.execute(queryString)
    records = cursor.fetchall()

    size = os.get_terminal_size()
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


def StateOverTime():
    state = input("Enter state: ")
    queryString = "SELECT CountyConfirmed.date, SUM(CountyConfirmed.confirmed) AS confirmedSum FROM CountyConfirmed WHERE stateName = '" + state + "' AND confirmed != 0 GROUP BY date ORDER BY date;"
    # queryString = "SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = '" + state + "' AND date = (SELECT MAX(date) FROM CountyConfirmed);"
    cursor.execute(queryString)
    records = cursor.fetchall()

    size = os.get_terminal_size()
    print('\n')
    print('#' * size[0])
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')

    day = 0
    for row in records:
        if day % 7 == 0:
            result = "There are {} confirmed cases in {} state on {}.".format(str(row[1]), state, row[0])
            print('# ' + result.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
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



def ConfirmedCasesByDateAndCounty():
    state = input("Enter state: ")
    county = input("Enter county: ")
    date = input("Enter date (YYYY-MM-DD): ")
    queryString = "SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = '"+ state + "' AND countyName = '" + county + "' AND date = '" + date + "';"
    cursor.execute(queryString)
    records = cursor.fetchall()

    
    size = os.get_terminal_size()
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


def ConfirmedCasesByDateAndState():
    state = input("Enter state: ")
    date = input("Enter date (YYYY-MM-DD): ")
    queryString = "SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = '"+ state + "' AND date = '" + date + "';"
    cursor.execute(queryString)
    records = cursor.fetchall()

    size = os.get_terminal_size()
    print('\n')
    print('#' * size[0])
    print('# ' + emptySpace.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    for row in records:
        result = "{} confirmed cases in {} on {}.".format(str(row[0]), state, date)
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
                                ## Compare ##
def Compare():    
    clear()
    size = os.get_terminal_size()
    print('\n' * 2)
    print('#' * size[0])
    for menuItem in compareMenu:
        print('# ' + menuItem.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('#' * size[0])
    print('\n')

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


#distance between two counties
def DistanceBetweenTwoCounties():
    state1 = input("Enter the first state: ")
    county1 = input("Enter the first county: ")
    state2 = input("Enter the second state: ")
    county2 = input("Enter the second county: ")

    t1 = "SELECT 3963 * ACOS((SIN(RADIANS(c1.lat)) * SIN(RADIANS(c2.lat))) + COS(RADIANS(c1.lat)) * COS(RADIANS(c2.lat))"
    t2 = "*COS(RADIANS(c2.long) - RADIANS(c1.long))) as miles FROM County as c1, County as c2 "
    t3 = "WHERE c1.countyName LIKE '" + county1 + "' "
    t4 = "AND c1.stateName LIKE '" + state1 + "' "
    t5 = "AND c2.countyName LIKE '" + county2 + "' "
    t6 = "AND c2.stateName LIKE '" + state2 + "';"
    queryString = t1 + t2 + t3 + t4 + t5 + t6
    cursor.execute(queryString)
    records = cursor.fetchall()
    for row in records:
        print("The distance between " + county1 + " and " + county2 + " is " + str(round(row[0], 2)) + " miles")

def compareCounties():
    state1 = input("Enter the first state: ")
    county1 = input("Enter the first county: ")
    state2 = input("Enter the second state: ")
    county2 = input("Enter the second county: ")
    #info for one county
    confirmedCase1 = "SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = '" + state1 + "' AND countyName = '" + county1 + "';"
    confirmedCase2 = "SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = '" + state2 + "' AND countyName = '" + county2 + "';"
    deathCase1 = "SELECT SUM(deaths) FROM CountyDeaths WHERE stateName = '" + state1 + "' AND countyName = '" + county1 + "';"
    deathCase2 = "SELECT SUM(deaths) FROM CountyDeaths WHERE stateName = '" + state2 + "' AND countyName = '" + county2 + "';"
    
    county1Info = ("SELECT CountyData.totalPop, CountyData.numHouseholds, CountyData.pctMale, "
    "CountyData.medianAge, CountyData.pctUnder18, CountyData.pctOver65, "
    "CountyData.pctWhite, CountyData.pctBlackAA , CountyData.pctIndianAlaskanNative , CountyData.pctAsian, "
    "CountyData.pctHawaiianPacificIslander, CountyData.pctOtherRace, CountyData.precentHispanicLatino "
    "FROM CountyData JOIN County "
    "ON CountyData.countyName = County.countyName AND CountyData.StateName = County.StateName "
    "WHERE CountyData.countyName = '" + county1 + "' AND CountyData.stateName = '" + state1 + "'; ")

    county2Info = ("SELECT CountyData.totalPop, CountyData.numHouseholds, CountyData.pctMale, "
    "CountyData.medianAge, CountyData.pctUnder18, CountyData.pctOver65, "
    "CountyData.pctWhite, CountyData.pctBlackAA , CountyData.pctIndianAlaskanNative , CountyData.pctAsian, "
    "CountyData.pctHawaiianPacificIslander, CountyData.pctOtherRace, CountyData.precentHispanicLatino "
    "FROM CountyData JOIN County "
    "ON CountyData.countyName = County.countyName AND CountyData.StateName = County.StateName "
    "WHERE CountyData.countyName = '" + county2 + "' AND CountyData.stateName = '" + state2 + "'; ")

    cursor.execute(confirmedCase1)
    confirmedCase1Query = cursor.fetchall()
    cursor.execute(confirmedCase2)
    confirmedCase2Query = cursor.fetchall()
    cursor.execute(deathCase1)
    deathCase1Query = cursor.fetchall()
    cursor.execute(deathCase2)
    deathCase2Query = cursor.fetchall()

    cursor.execute(county1Info)
    county1InfoQuery = cursor.fetchall()
    cursor.execute(county2Info)
    county2InfoQuery = cursor.fetchall()

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
                                ## Investigate ##
def Investigate():    
    clear()
    size = os.get_terminal_size()
    print('\n' * 2)
    print('#' * size[0])
    for menuItem in investigateMenu:
        print('# ' + menuItem.center(size[0] + 13 -  len(homeMenu[5]), ' ') + '#')
    print('#' * size[0])
    print('\n')

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

#######################idk if we need
def TotalCountyPopulationOver65():
    county = input("Enter county: ")
    queryString = "SELECT totalPop*pctOver65 FROM CountyData WHERE countyName LIKE '" + county + "';"
    cursor.execute(queryString)
    records = cursor.fetchall()
    for row in records:
        print("There are " + str(row[0]) + " people who are over 65 years old in " + county)

def TotalStatePopulationOver65():
    state = input("Enter state: ")
    queryString = "SELECT SUM(totalPop*pctOver65) FROM CountyData WHERE stateName LIKE '" + state + "';"
    cursor.execute(queryString)
    records = cursor.fetchall()
    for row in records:
        print("There are " + str(row[0]) + " people who are over 65 years old in " + state)

#Total Confirmed and Deaths ordered by household density
#confirmed and deaths

            
def HouseholdDensity():
    queryString = ("SELECT CountyData.countyName, CountyData.stateName, " 
    "CAST((CAST(totalPop AS float)/numHouseholds) as NUMERIC(5,2)) as householdDensity, " 
    "c.confirmed, d.deaths " 
    "FROM CountyData, "
	"(SELECT countyName, stateName, SUM(confirmed) as confirmed FROM CountyConfirmed "
	"GROUP BY (countyName, stateName)) as c, "
	"(SELECT countyName, stateName, SUM(deaths) as deaths FROM CountyDeaths "
	"GROUP BY (countyName, stateName)) as d "
    "WHERE CountyData.countyName = c.countyName "
    "AND CountyData.stateName = c.stateName "
    "AND CountyData.countyName = d.countyName "
    "AND CountyData.stateName = d.stateName "
    "ORDER BY householdDensity DESC "
    "LIMIT 10;" )

    cursor.execute(queryString)
    records = cursor.fetchall()
    
    t = PrettyTable(['County Name', 'State Name', 'Household Density', 'Confirmed Cases', 'Confirmed Deaths'])
    t.add_row([records[0][0]], records[0][1], records[0][2], records[0][3], records[0][4])
    print(t)


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
    returnKey = int(input(""))
    mainMenu()
    return
        
    # print("HISTORY")
    # for element in history:
    #     print(element)
    # anykey=input("Press anything to return to main menu \n")
    # mainMenu()

def DatasetInfo():
    clear()
    print("DATA SET INFO")
    anykey=input("Press anything to return to main menu \n")
    mainMenu()

def ListAllStates():
    queryString = ("SELECT DISTINCT stateName FROM CountyData ORDER BY stateName;")

    cursor.execute(queryString)
    records = cursor.fetchall()
    print(tabulate(records, headers=["State"]))

def InputState():
    queryString = ("SELECT DISTINCT stateName FROM CountyData")
    cursor.execute(queryString)
    records = cursor.fetchall()
    state = None
    while(state == None):
        state = input("State: ")
        if (state,) in records:
            return state
        print("That's not a supported state.")


def InputCounty(state):
    queryString = ("SELECT countyName FROM CountyData WHERE stateName = %s ORDER BY countyName")
    cursor.execute(queryString, (state))

    print("Counties in " + state + ":")
    records = cursor.fetchall()
    for r in records:
        print("   " + r)

    
    records = cursor.fetchall()
    county = None
    while(county == None):
        county = input("Choose a county: ")
        if (county,) in records:
            return county
        print("That's not a supported county.")
    
if __name__ == '__main__':
    mainMenu()
