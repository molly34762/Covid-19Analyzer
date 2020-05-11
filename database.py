
import psycopg2
import psycopg2.extras

connection_string = "host='localhost' dbname='covid_census' user='covid_census' password='covid_census'"
cursor = psycopg2.connect(connection_string).cursor()


def ConfirmedCasesByStateQuery(state):
    queryString = """SELECT SUM(confirmed) FROM CountyConfirmed
                     WHERE stateName = %s
                     AND date = (SELECT MAX(date) FROM CountyConfirmed)"""
    cursor.execute(queryString, (state,))
    return cursor.fetchall()

def ConfirmedCasesByCountyQuery(state, county):
    #Create and execute the query string
    queryString = """SELECT SUM(confirmed)
                     FROM CountyConfirmed
                     WHERE stateName = %s
                     AND countyName = %s
                     AND date = (SELECT MAX(date) FROM CountyConfirmed);"""
    cursor.execute(queryString, (state, county))
    return cursor.fetchall()

def DeathsByCountyQuery(state, county):
    queryString = """SELECT deaths
                    FROM CountyDeaths
                    WHERE stateName = %s
                    AND countyName = %s
                    AND date = (SELECT MAX(date) from CountyConfirmed)"""
    cursor.execute(queryString, (state, county))
    return cursor.fetchall()

def StateOverTimeQuery(state):
    #Create and execute a query string
    queryString = """SELECT CountyConfirmed.date, SUM(CountyConfirmed.confirmed) AS confirmedSum
                     FROM CountyConfirmed WHERE stateName = %s
                     AND confirmed != 0 GROUP BY date ORDER BY date"""
    cursor.execute(queryString, (state,))
    return cursor.fetchall()

def CountyOverTimeQuery(state, county):
    #Create and execute a query string
    queryString = """SELECT CountyConfirmed.date, CountyConfirmed.confirmed 
                     FROM CountyConfirmed WHERE stateName = %s 
                     AND countyName = %s 
                     AND confirmed != 0 GROUP BY date, confirmed ORDER BY date;"""

    cursor.execute(queryString, (state, county))
    return cursor.fetchall()

def ConfirmedCasesbyDateAndCount(state, county, date):
    queryString = """SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = %s AND countyName = %s AND date = %s"""
    cursor.execute(queryString, (state, county, date))
    return cursor.fetchall()

def ConfirmedCasesbyDateandState(state, date):
    queryString = """SELECT SUM(confirmed) FROM CountyConfirmed WHERE stateName = %s AND date = %s"""
    cursor.execute(queryString, (state, date))
    return cursor.fetchall()

def DistanceBetweenCountiesQuery(state1, county1, state2, county2):
    queryString = """SELECT 3963 * ACOS((SIN(RADIANS(c1.lat)) * SIN(RADIANS(c2.lat))) + COS(RADIANS(c1.lat)) * COS(RADIANS(c2.lat))*COS(RADIANS(c2.long) - RADIANS(c1.long)))
                     as miles
                     FROM County as c1, County as c2
                     WHERE c1.countyName LIKE %s
                        AND c1.stateName LIKE %s
                        AND c2.countyName LIKE %s
                        AND c2.stateName LIKE %s"""
    cursor.execute(queryString, (county1, state1, county2, state2))
    return cursor.fetchall()

def CountyInfoQuery(state, county):
    queryString = ("""SELECT CountyData.totalPop, CountyData.numHouseholds, CountyData.pctMale,
                        CountyData.medianAge, CountyData.pctUnder18, CountyData.pctOver65,
                        CountyData.pctWhite, CountyData.pctBlackAA , CountyData.pctIndianAlaskanNative , CountyData.pctAsian,
                        CountyData.pctHawaiianPacificIslander, CountyData.pctOtherRace, CountyData.precentHispanicLatino
                      FROM CountyData JOIN County
                        ON CountyData.countyName = County.countyName AND CountyData.StateName = County.StateName
                      WHERE CountyData.countyName = %s AND CountyData.stateName = %s """)
    cursor.execute(queryString, (county, state))
    return cursor.fetchall()

def PopOver65Query(state, county):
    queryString = """SELECT (pctOver65/100) * totalPop FROM CountyData WHERE countyName = %s AND stateName  = %s"""
    cursor.execute(queryString, (county, state))
    return cursor.fetchall()

def top10HouseholdDensitiesQuery():
    queryString = """SELECT CountyData.countyName, CountyData.stateName,  
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
                      LIMIT 10""" 
    cursor.execute(queryString)
    return cursor.fetchall()

def allStates():
    queryString = """SELECT DISTINCT stateName FROM CountyData"""
    cursor.execute(queryString)
    return cursor.fetchall()

def countiesInState(state):
    queryString = """SELECT County.countyName FROM CountyData 
                     JOIN County 
                     ON CountyData.countyName = County.countyName AND CountyData.StateName = County.StateName
                     WHERE County.stateName = %s
                     AND EXISTS (SELECT * FROM CountyConfirmed as cc WHERE cc.confirmed != 0 AND cc.stateName = County.stateName AND cc.countyName =  County.countyName)
                     ORDER BY County.countyName"""
    cursor.execute(queryString, (state,))
    return cursor.fetchall()

def minDate():
    queryString = """SELECT MIN(date) FROM countyConfirmed"""
    cursor.execute(queryString)
    return cursor.fetchone()

def maxDate():
    queryString = """SELECT MAX(date) FROM countyConfirmed"""
    cursor.execute(queryString)
    return cursor.fetchone()

def isValidDate(date):
    queryString = """SELECT * FROM countyConfirmed WHERE date = %s"""
    cursor.execute(queryString, (date,))
    if cursor.fetchone() is None:
        return False
    return True