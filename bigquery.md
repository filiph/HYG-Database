# BigQuery SQL Queries

After the HYG database (the hygxyz.csv data) is uploaded to BigQuery, here are some sample queries one can do above the data.

## Closest stars

Let's say we want to see all the stars that are less than `5` parsecs away from Sol (coordinates `0, 0, 0`) and order them by distance.

		SELECT
		  StarID,
		  HIP,
		  BayerFlamsteed,
		  ProperName,
		  SQRT(POW(X-0,2) + POW(Y-0,2) + POW(Z-0,2)) as CustomDistance
		FROM
		  [stars.all]
		HAVING
		  CustomDistance < 5
		ORDER BY
		  CustomDistance

Conversely, let's say we want to see every star that is less than 10 light years away from Groombridge 34. Therefore, we are searching for stars that are `3.066` (= 10 * 0.3066) parsecs away from the coordinates `2.55743, 0.20511, 2.47951` (= Groombridge 34 coordinates). This time, we also want to see those stars' coordinates and those stars' coordinates in relation to Groombridge 34.

		SELECT
		  StarID,
		  HIP, HD, HR, Gliese,
		  BayerFlamsteed,
		  ProperName,
		  RA, Dec, Distance, PMRA, PMDec, RV, Mag, AbsMag, Spectrum, ColorIndex,
		  X, Y, Z,
		  VX, VY, VZ,
		  (X-2.55743) * 3.066 as NX, (Y-0.20511) * 3.066 as NY, (Z-2.47951) * 3.066 as NZ,
		  SQRT(POW(X-2.55743,2) + POW(Y-0.20511,2) + POW(Z-2.47951,2)) * 3.066 as GroombridgeDistance
		FROM
		  [stars.all]
		HAVING
		  GroombridgeDistance < 10
		ORDER BY GroombridgeDistance