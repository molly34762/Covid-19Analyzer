--Total Confirmed and Deaths ordered by household density
SELECT CountyData.countyName, CountyData.stateName,
	CAST((CAST(totalPop AS float)/numHouseholds) as NUMERIC(5,2)) as householdDensity, 
	c.confirmed, d.deaths
FROM CountyData,
	(SELECT countyName, stateName, confirmed FROM CountyConfirmed
		WHERE date = (SELECT MAX(date) FROM CountyConfirmed))
		as c,
	(SELECT countyName, stateName, deaths as deaths FROM CountyDeaths
		WHERE date = (SELECT MAX(date) FROM CountyConfirmed))
		as d
WHERE CountyData.countyName = c.countyName
	AND CountyData.stateName = c.stateName
	AND CountyData.countyName = d.countyName
	AND CountyData.stateName = d.stateName
ORDER BY householdDensity DESC
LIMIT 10;

--all counties in a state in covid dataset (has lat-lng and covid data)
SELECT countyName FROM County WHERE stateName LIKE 'California';

--all counties in a state in census dataset (will always have covid counterpart for as much as I've tested)
SELECT countyName FROM CountyData WHERE stateName LIKE 'California';

--distance between two counties in miles
SELECT 3963 * ACOS((SIN(RADIANS(c1.lat))*SIN(RADIANS(c2.lat))) + COS(RADIANS(c1.lat)) * COS(RADIANS(c2.lat)) * COS(RADIANS(c2.long) - RADIANS(c1.long))) as miles FROM County as c1, County as c2
WHERE c1.countyName LIKE 'Riverside'
AND c1.stateName LIKE 'California'
AND c2.countyName LIKE 'Josephine'
AND c2.stateName LIKE 'Oregon';
