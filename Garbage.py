import os

import psycopg2
import psycopg2.extras


connection_string = "host='localhost' dbname='covid_census' user='covid_census' password='covid_census'"
cursor = psycopg2.connect(connection_string).cursor()

def TotalCountyPopulationOver65():
    county = raw_input("Enter county: ")
    queryString = "SELECT totalPop*pctOver65 FROM CountyData WHERE countyName LIKE '" + county + "';"
    cursor.execute(queryString)
    records = cursor.fetchall()
    for row in records:
        print("There are " + str(row[0]) + " people who are over 65 years old in " + county)

def TotalStatePopulationOver65():
    state = raw_input("Enter state: ")
    queryString = "SELECT SUM(totalPop*pctOver65) FROM CountyData WHERE stateName LIKE '" + state + "';"
    cursor.execute(queryString)
    records = cursor.fetchall()
    for row in records:
        print("There are " + str(row[0]) + " people who are over 65 years old in " + state)

def ConfirmedCasesByState():
    state = raw_input("Enter state: ")
    queryString = "SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName LIKE '" + state + "';"
    cursor.execute(queryString)
    records = cursor.fetchall()
    for row in records:
        print("There are " + str(row[0]) + " confirmed cases in " + state)

def ConfirmedCasesByCounty():
    county = raw_input("Enter county: ")
    queryString = "SELECT SUM(confirmed) FROM CountyConfirmed WHERE countyName LIKE '" + county + "';"
    cursor.execute(queryString)
    records = cursor.fetchall()
    for row in records:
        print("There are " + str(row[0]) + " confirmed cases in " + county)

def ConfirmedCasesByDate():
    date = raw_input("Enter date: ")
    queryString = "SELECT SUM(confirmed) FROM CountyConfirmed WHERE countyName LIKE '" + date + "';"
    cursor.execute(queryString)
    records = cursor.fetchall()
    for row in records:
        print("There are " + str(row[0]) + " confirmed cases in " + date)


#all counties in a state in covid dataset (has lat-lng and covid data)
def CountiesInCovid():
    state = raw_input("Enter state: ")
    cursor.execute("SELECT countyName FROM County WHERE stateName LIKE '" + state + "';")
    records = cursor.fetchall()
    for row in records:
        print(row[0])

#all counties in a state in census dataset (will always have covid counterpart for as much as I've tested)
def CountiesInCensus():
    county = raw_input("Enter state: ")
    cursor.execute("SELECT countyName FROM CountyData WHERE stateName LIKE '" + county + "';")
    records = cursor.fetchall()
    for row in records:
        print(row[0])

#distance between two counties
def DistanceBetweenTwoCounties():
    state1 = raw_input("Enter the first state: ")
    county1 = raw_input("Enter the first county: ")
    state2 = raw_input("Enter the second state: ")
    county2 = raw_input("Enter the second county: ")

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
        print("The distance between " + county1 + " and " + county2 + " is " + str(row[0]) + " miles")

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

def clear():
    os.system('clear')


homeMenu = ['HOME', '1. NEW QUERY', '2. HISTORY', '3. DATA SET INFO','4. Exit']

def mainMenu():
    clear()
    # cmd = 'mode 100, 60'
    # os.system(cmd)


    
    for menuItem in homeMenu:
        print(menuItem)


    while True:
        #size = os.get_terminal_size()
        #print("Width: %s \nHeight: %s\n" % (size[0], size[1]))
        #print("###############################################################################################################################")
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
                break
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

if __name__ == '__main__':
    main()
    #TotalPopulationOver65()
    #TotalCountyPopulationOver65()
    #ConfirmedCasesByDate()
    #ConfirmedCasesByCounty()
    #ConfirmedCasesByState()
    #CountiesInCovid()
    #CountiesInCensus()
    #DistanceBetweenTwoCounties()
    #HouseholdDensity()
    #mainMenu()