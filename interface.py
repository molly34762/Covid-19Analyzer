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

homeMenu = ['HOME', '--------','1. NEW QUERY', '2. HISTORY', '3. DATA SET INFO','4. Exit']
queryMenu = ['New Query', '--------', '  ', 'INSTRUCTIONS', '  ', '1. EXPLORE', '2. COMPARE', '3. INVESTIGATE', ' ','4. HOME']
exploreMenu = ['EXPLORE', '--------', '  ', 'INSTRUCTIONS', '  ', '1. STATE', '2. COUNTY', '3. DATE', ' ', '4. HOME']
compareMenu = ['COMPARE', '--------', '  ', 'INSTRUCTIONS', '  ', '1. COMPARISON BETWEEN TWO COUNTIES', '2. COMPARISON BETWEEN TWO STATES', ' ', '3. HOME']
investigateMenu = ['INVESTIGATE', '--------', '  ', 'INSTRUCTIONS', '  ', '1. APPROXIMATE VULNERABLE POPULATIONS', '2. CALCULATE HOUSEHOLD DENSITIES', ' ', '3. HOME']

#######################################################################
                                ## Menus ##
def mainMenu():
    clear()
 
    size = os.get_terminal_size()
    # print("Width: %s \nHeight: %s\n" % (size[0], size[1]))
    print('\n' * 2)
    print('#' * size[0])
    for menuItem in homeMenu:
        print('# ' + menuItem.center(size[0] + 13 -  len(homeMenu[4]), ' ') + '#')
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
    print('\n' * 2)
    print('#' * size[0])
    for menuItem in queryMenu:
        print('# ' + menuItem.center(size[0] + 13 -  len(homeMenu[4]), ' ') + '#')
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
    print('\n' * 2)
    print('#' * size[0])
    for menuItem in exploreMenu:
        print('# ' + menuItem.center(size[0] + 13 -  len(homeMenu[4]), ' ') + '#')
    print('#' * size[0])
    print('\n')

    while True:
        try:
            print("Enter 5 for possible inputs")
            selection=int(input("Enter choice: "))
            if selection == 1:
                ConfirmedCasesByState()
                break
            elif selection == 2:
                ConfirmedCasesByCounty()
                break
            elif selection == 3:
                
                ConfirmedCasesByDate()
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
        
def ConfirmedCasesByState():
    state = input("Enter state: ")
    queryString = "SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName LIKE '" + state + "';"
    cursor.execute(queryString)
    records = cursor.fetchall()
    for row in records:
        print("There are " + str(row[0]) + " confirmed cases in " + state)

def ConfirmedCasesByCounty():
    county = input("Enter county: ")
    queryString = "SELECT SUM(confirmed) FROM CountyConfirmed WHERE countyName LIKE '" + county + "';"
    cursor.execute(queryString)
    records = cursor.fetchall()
    for row in records:
        print("There are " + str(row[0]) + " confirmed cases in " + county)

def ConfirmedCasesByDate():
    date = input("Enter date: ")
    queryString = "SELECT SUM(confirmed) FROM CountyConfirmed WHERE countyName LIKE '" + date + "';"
    cursor.execute(queryString)
    records = cursor.fetchall()
    for row in records:
        print("There are " + str(row[0]) + " confirmed cases in " + date)

#######################################################################
                                ## Compare ##
def Compare():    
    clear()
    size = os.get_terminal_size()
    print('\n' * 2)
    print('#' * size[0])
    for menuItem in compareMenu:
        print('# ' + menuItem.center(size[0] + 13 -  len(homeMenu[4]), ' ') + '#')
    print('#' * size[0])
    print('\n')

    while True:
        try:
            selection=int(input("Enter choice: "))
            if selection == 1:
                DistanceBetweenTwoCounties()
                break
            elif selection == 2:
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

#######################################################################
                                ## Investigate ##
def Investigate():    
    clear()
    size = os.get_terminal_size()
    print('\n' * 2)
    print('#' * size[0])
    for menuItem in investigateMenu:
        print('# ' + menuItem.center(size[0] + 13 -  len(homeMenu[4]), ' ') + '#')
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
    print("HISTORY")
    anykey=input("Press anything to return to main menu \n")
    mainMenu()

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
