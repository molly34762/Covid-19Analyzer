
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