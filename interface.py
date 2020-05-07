import os
import curses
import time
import psycopg2
import psycopg2.extras
import tabulate


connection_string = "host='localhost' dbname='covid_census' user='covid_census' password='covid_census'"
cursor = psycopg2.connect(connection_string).cursor()
# stdscr.clear()
# stdscr.refresh()

def clear():
    os.system('clear')

homeMenu = ['HOME', '--------', '  ', '1. NEW QUERY', '2. HISTORY', '3. DATA SET INFO', ' ', '4. Exit']
queryMenu = ['New Query', '--------', '  ', 'INSTRUCTIONS', '  ', '1. EXPLORE', '2. COMPARE', '3. INVESTIGATE', ' ','4. HOME']
exploreMenu = ['EXPLORE', '--------', '  ', 'INSTRUCTIONS', '  ', '1. STATE', '2. COUNTY', '3. STATE BY DATE', '4. COUNTY BY DATE', ' ', '5. HOME']
compareMenu = ['COMPARE', '--------', '  ', 'INSTRUCTIONS', '  ', '1. COMPARISON BETWEEN TWO COUNTIES', '2. COMPARISON BETWEEN TWO STATES', ' ', '3. HOME']
investigateMenu = ['INVESTIGATE', '--------', '  ', 'INSTRUCTIONS', '  ', '1. APPROXIMATE VULNERABLE POPULATIONS', '2. CALCULATE HOUSEHOLD DENSITIES', ' ', '3. HOME']
emptySpace = ' '
newQueryMsg = 'Would you like to perform another query?'
history = []

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
                # print('\n')
                # print('Would you like to peform another query? \n1. Yes\n2. No')
                # redo = int(input("Enter choice: "))
                # if redo == 1:
                #     if Explore() == -1:
                #         return -1
                # else:
                #     return -1    
                return
            elif selection == 2:
                ConfirmedCasesByCounty()
                # print('\n')
                # print('Would you like to peform another query? \n1. Yes\n2. No')
                # redo = int(input("Enter choice: "))
                # if redo == 1:
                #     if Explore() == -1:
                #         return -1
                # else:
                #     return -1
                return
            elif selection == 3:
                ConfirmedCasesByDateAndState()
                # print('\n')
                # print('Would you like to peform another query? \n1. Yes\n2. No')
                # redo = int(input("Enter choice: "))
                # if redo == 1:
                #     if Explore() == -1:
                #         return -1
                # else:
                #     return  -1
                return
            elif selection == 4:
                ConfirmedCasesByDateAndCounty()
                # print('\n')
                # print('Would you like to peform another query? \n1. Yes\n2. No')
                # redo = int(input("Enter choice: "))
                # if redo == 1:
                #     if Explore() == -1:
                #         return -1
                # else:
                #     return -1
                return
            elif selection == 5:
                mainMenu()
                return
            else:
                print("Invalid choice. Enter 1-4")
                time.sleep(2)
                MakeNewQuery()
                return
        except ValueError:
            print("Invalid Input")
    exit
        
def ConfirmedCasesByState():
    state = input("Enter state: ")
    queryString = "SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = '" + state + "' AND date = (SELECT MAX(date) FROM CountyConfirmed);"
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
    state = input("Enter state: ")
    county = input("Enter county: ")
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

    print("Confirmed Cases")
    print(confirmedCase1Query[0][0])
    print(confirmedCase2Query[0][0])
    print("Confirmed Death Numbers")
    print(deathCase1Query[0][0])
    print(deathCase2Query[0][0])
    print("Total Population")


    for i in county1InfoQuery:
        print(str(i[0]) +" " + str(i[1]))

    #print(county1InfoQuery[0][0])
    
    print("Number of Households")
    print("Population Male")
    print("Median Age")
    print("Percentage under 18")
    print("Percentage over 65")
    print("Percentage White")
    print("Percentage Black")

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
    for row in records:
        print(row)


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

def ListAllCounties():
    queryString = ("SELECT County.countyName, County.stateName, CountyData.totalPop FROM CountyData JOIN County "
    "ON CountyData.countyName = County.countyName AND CountyData.StateName = County.StateName "
    "ORDER BY County.StateName, County.countyName;")
    
    cursor.execute(queryString)
    records = cursor.fetchall()
    print (records)
    # print(tabulate(records, headers=["County", "State", "Population"]))

    
if __name__ == '__main__':
    mainMenu()
    # ConfirmedCasesByDate()
    #ConfirmedCasesByCounty()
    #ConfirmedCasesByState()
    #CountiesInCovid()
    #CountiesInCensus()
    #DistanceBetweenTwoCounties()
    #HouseholdDensity()
    #mainMenu()

    ##Explore by queries
    #SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = 'New York';
    #SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = 'New York' AND countyName = 'Albany';
    #SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = 'New York' AND countyName = 'Albany' AND date = (SELECT MAX(date) FROM CountyConfirmed);


# SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = 'New York' AND countyName = 'Albany';
# SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = 'California' AND countyName = 'Riverside';
# SELECT SUM(deaths) FROM CountyDeaths WHERE stateName = 'New York' AND countyName = 'Albany';
# SELECT SUM(deaths) FROM CountyDeaths WHERE stateName = 'California' AND countyName = 'Riverside';
# SELECT CountyData.totalPop, CountyData.numHouseholds, CountyData.pctMale,  
# CountyData.medianAge, CountyData.pctUnder18, CountyData.pctOver65, 
# CountyData.pctWhite, CountyData.pctBlackAA , CountyData.pctIndianAlaskanNative , CountyData.pctAsian,
# CountyData.pctHawaiianPacificIslander, CountyData.pctOtherRace, CountyData.precentHispanicLatino
# FROM CountyData JOIN County 
# ON CountyData.countyName = County.countyName AND CountyData.StateName = County.StateName
# WHERE CountyData.countyName = 'Albany' AND CountyData.stateName = 'New York';

# SELECT CountyData.totalPop, CountyData.numHouseholds, CountyData.pctMale,  
# CountyData.medianAge, CountyData.pctUnder18, CountyData.pctOver65, 
# CountyData.pctWhite, CountyData.pctBlackAA , CountyData.pctIndianAlaskanNative , CountyData.pctAsian,
# CountyData.pctHawaiianPacificIslander, CountyData.pctOtherRace, CountyData.precentHispanicLatino
# FROM CountyData JOIN County 
# ON CountyData.countyName = County.countyName AND CountyData.StateName = County.StateName
# WHERE CountyData.countyName = 'Albany' AND CountyData.stateName = 'New York';
