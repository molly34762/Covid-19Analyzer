# Database-Project

https://github.com/molly34762/Database-Project

## Datasets used in the application

1) https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series
2) https://data.census.gov/cedsci/profile?q=United%20States&g=0100000US&tid=ACSDP1Y2018.DP05

## What's in the application

The directory contains the following files:

- `README.md`: This document
- `get_data.py`: a python script that obtains data from the two sources and populates the postgres database
- `user_setup.sql`: a sql file that sets up the database `covid_census` and the user `covid_census` 
- `tables_setup.sql`: a sql file that creates the table for the database `covid_census`
- `interface.py`: a python script that will run this application
- `census_data.csv`: The census data we are using for this project

## Setup

Please download the following packages: [psycopg2] [wget] [PrettyTable]
You may run `pip3 install psycopg2 wget PrettyTable`
All files for set up are located in the folder `Database-Setup`
Set up the `covid_census` database by running `user_setup.sql` and `tables_setup.sql`.
Insert the data from the datasets by running `python3 get_data.py`.

## Running

You may view the application by running `python3 interface.py`.


Requirements.txt

[psycopg2] [wget] [PrettyTable]
