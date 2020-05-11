# Database-Project

# Team
- Ehren Schindelar
- Ahsanullah Sehat
- Meixin Liang
- Hongyi Huang

# Purpose
Analyzing the Covid-19 pandemic with respect to communities in the United States

## Datasets used
- COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University
- 2018 United States Census

## What's in the application
The directory contains the following files:
- `application.py`: Entry point to the application
- `database.py`: Interface/entrypoint to the database code
- `datasets.txt`: Text file containing the URLs of the two datasets being used
- `db-setup.sql`: Creates the database users and grants them privileges
- `load_data.py`: Loads the data from the datasets into the database
- `readme.md`: Setup instructions
- `requirements.txt`: Dependencies and required packages
- `schema.sql`: Sql file containing the schema that will create the tables
- `retrieve_data.py`: Download the datasets 

## Setup
1. Please download the following packages in the Ubuntu terminal: [psycopg2] [wget] [PrettyTable]
2. Set up the database and user by running `db-setup.sql` as superuser
3. Create the database tables by running `schema.sql` as the newly created user
4. Download the datasets by running `retrieve_data.py`
5. Load the data from the datasets into the database by running `load_data.py`

## Running
You may view the application by running `python3 application.py`

## Demonstration Video
-- 'https://drive.google.com/open?id=1IDB3rk6PiS1TpWHv6YWKuo-NKTx0NFxM'


