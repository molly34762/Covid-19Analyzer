import wget
import psycopg2
import csv
import sys

url_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
url_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
try:
    f = open("confirmed.csv")
    f.close()
except IOError:
    wget.download(url_confirmed, "confirmed.csv")

try:
    f = open("deaths.csv")
    f.close()
except IOError:
    wget.download(url_deaths, "deaths.csv")

conn = psycopg2.connect("host=localhost dbname=covid_census user=covid_census password=covid_census")

cursor = conn.cursor()

counties = []
values = []

with open("census_data.csv") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
        if line_count != 0 and line_count != 1:
            name = row['NAME']
            if " County, " in name:
                countyName = name.split(" County, ")[0]
                stateName = name.split(" County, ")[1]
            else:
                countyName = name.split(", ")[0]
                stateName = name.split(", ")[1]
            population = row['DP05_0001E'] if row['DP05_0001E'] != 'N' else 0
            households = row['DP05_0086E'] if row['DP05_0086E'] != 'N' else 0
            percentmale = row['DP05_0002PE'] if row['DP05_0002PE'] != 'N' else 0
            medianage = row['DP05_0018E'] if row['DP05_0018E'] != 'N' else 0
            percentunder18 = row['DP05_0019PE'] if row['DP05_0019PE'] != 'N' else 0
            percentover65 = row['DP05_0024PE'] if row['DP05_0024PE'] != 'N' else 0
            raceWhite = row['DP05_0064PE'] if row['DP05_0064PE'] != 'N' else 0
            raceBlackAA = row['DP05_0065PE'] if row['DP05_0065PE'] != 'N' else 0
            raceIndianAlaskaNnative = row['DP05_0066PE'] if row['DP05_0066PE'] != 'N' else 0
            raceAsian = row['DP05_0067PE'] if row['DP05_0067PE'] != 'N' else 0
            raceHawaiianIslander = row['DP05_0068PE'] if row['DP05_0068PE'] != 'N' else 0
            raceOther = row['DP05_0069PE'] if row['DP05_0069PE'] != 'N' else 0
            raceHispanicLatino = row['DP05_0071PE']
            values.append((stateName, countyName, population, households, percentmale, medianage,
                        percentunder18, percentover65, raceWhite, raceBlackAA,
                        raceIndianAlaskaNnative, raceAsian, raceHawaiianIslander, raceOther, raceHispanicLatino))
        line_count += 1

print('parsed census data, adding rows..')
cursor.executemany("INSERT INTO CountyData VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", values)

values = []
with open("confirmed.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            columns = row
            line_count += 1
        else:
            if(not row[5].startswith("Out of") and not row[5] == "Unassigned" and not row[5] == ""):
                county = row[5]
                state = row[6]
                lat = row[8]
                long = row[9]
                counties.append((state, county, lat, long))
                for i in range(11, len(columns)):
                    values.append((state, county, columns[i], row[i]))
                line_count += 1

print('parsed confirmed data, adding rows..')
cursor.executemany("INSERT INTO County VALUES (%s, %s, %s, %s)", counties)
cursor.executemany("INSERT INTO CountyConfirmed VALUES (%s, %s, %s, %s)", values)

values = []

with open("deaths.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            columns = row
            line_count += 1
        else:
            if(not row[5].startswith("Out of") and not row[5] == "Unassigned" and not row[5] == ""):
                county = row[5]
                state = row[6]
                for i in range(12, len(columns)):
                    values.append((state, county, columns[i], row[i]))
                line_count += 1

print('parsed deaths data, adding rows..')
cursor.executemany("INSERT INTO CountyDeaths VALUES (%s, %s, %s, %s)", values)

print('committing..')
conn.commit()
    
    
    
    
    
    