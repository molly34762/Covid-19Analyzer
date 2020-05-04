DROP TABLE IF EXISTS County CASCADE;
DROP TABLE IF EXISTS CountyConfirmed CASCADE;
DROP TABLE IF EXISTS CountyDeaths CASCADE;
DROP TABLE IF EXISTS CountyData CASCADE;

CREATE TABLE County (
	stateName		VARCHAR(127),
	countyName		VARCHAR(127),
	lat NUMERIC(7,3),
	long NUMERIC(7,3),
	PRIMARY KEY(stateName, countyName)
);

CREATE TABLE CountyConfirmed (
	stateName VARCHAR(127),
	countyName VARCHAR(127),
	date DATE,
	confirmed INT,
	PRIMARY KEY(stateName, countyName, date)
);

CREATE TABLE CountyDeaths(
	stateName VARCHAR(127),
	countyName VARCHAR(127),
	date DATE,
	deaths INT,
	PRIMARY KEY(stateName, countyName, date)
);

CREATE TABLE CountyData (
	stateName VARCHAR(127),
	countyName VARCHAR(127),
	
	totalPop INT,
	numHouseholds INT,
	
	pctMale NUMERIC(5,2),
	
	medianAge NUMERIC(4,1),
	pctUnder18 NUMERIC(5,2),
	pctOver65 NUMERIC(5,2),
	
	pctWhite NUMERIC(5,2),
	pctBlackAA NUMERIC(5,2),
	pctIndianAlaskanNative NUMERIC(5,2),
	pctAsian NUMERIC(5,2),
	pctHawaiianPacificIslander NUMERIC(5,2),
	pctOtherRace NUMERIC(5,2),
	
	precentHispanicLatino NUMERIC(5,2), --of any race
	PRIMARY KEY(stateName, countyName)
);
