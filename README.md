# Database-Project

https://github.com/molly34762/Database-Project

## Datasets used in the application

1) https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series
2) https://data.census.gov/cedsci/profile?q=United%20States&g=0100000US&tid=ACSDP1Y2018.DP05

## What's in the application

The directory contains the following files:

- `README.md`: This document
- `census_data.csv`: The census data we are using for this project
- `get_data.py`: a python script that obtains data from the two sources and populates the postgres database
- `user_setup.sql`: a sql file that sets up the database `covid_census` and the user `covid_census` 
- `tables_setup.sql`: a sql file that creates the table for the database `covid_census`
- `interface.py`: a python script that will run this application

## Setup

Set up the `covid_census` database by running `user_setup.sql` and `tables_setup.sql`

## Running

You may view the application by running `python3 interface.py`
