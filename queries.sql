SELECT * FROM A WHERE A1 <= 50;
SELECT * FROM B ORDER BY B3;
SELECT cast(COUNT(*) as real)/COUNT(DISTINCT B2) FROM B;
SELECT * FROM A INNER JOIN B ON A.A1 = B.B2;