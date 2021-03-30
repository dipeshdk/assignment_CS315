-- .timer True;
-- .timer ON
-- .output output.txt  
-- .read queries.sql
SELECT * FROM A WHERE A1 <= 50;
SELECT * FROM B ORDER BY B3;
SELECT COUNT(*)/COUNT(DISTINCT B2) FROM B;
SELECT B1, B2, B3, A2 FROM A INNER JOIN B;