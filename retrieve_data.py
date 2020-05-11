import wget

url_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
url_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
url_census = "https://raw.githubusercontent.com/molly34762/Database-Project/master/census_data.csv"
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

try:
    f = open("census_data.csv")
    f.close()
except IOError:
    wget.download(url_census, "census_data.csv")