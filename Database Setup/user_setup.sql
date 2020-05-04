DROP DATABASE IF EXISTS covid_census;
CREATE DATABASE covid_census;

DROP USER IF EXISTS covid_census;
CREATE USER covid_census WITH PASSWORD 'covid_census';

GRANT ALL PRIVILEGES ON DATABASE covid_census TO covid_census;