import mariadb  
import csv

DATABASE_PATH = "./Databases/"

def connectMariaDB(db):
    con = mariadb.connect(user="root",
                        password = "",
                        host = "localhost",
                        port=3306)
    cur = con.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {db};")
    cur.execute(f"CREATE DATABASE {db};")
    cur.execute(f"USE {db};")
    cur.execute("DROP TABLE IF EXISTS A;")
    cur.execute("DROP TABLE IF EXISTS B;")
    cur.execute("CREATE TABLE A (A1 INTEGER PRIMARY KEY, A2 TEXT);")
    cur.execute("CREATE TABLE B (B1 INTEGER PRIMARY KEY, B2 INTEGER, B3 VARCHAR(255), FOREIGN KEY (B2) REFERENCES A(A1) ON DELETE CASCADE);")
    cur.execute("CREATE INDEX Bi on B(B3);")
    cur.execute(f"SET profiling = 1;")
    con.commit()
    return cur,con
    

def loadcsvA(csvfile, cur, con):
    with open(DATABASE_PATH+csvfile, 'r') as f:
        dr = csv.DictReader(f) 
        data = [(i['A1'], i['A2']) for i in dr]

    cur.executemany("INSERT INTO A values (?, ?);", data)
    con.commit()


def loadcsvB(csvfile, cur, con):
    with open(DATABASE_PATH+csvfile, 'r') as f:
        dr = csv.DictReader(f) 
        data = [(i['B1'], i['B2'], i['B3']) for i in dr]

    cur.executemany("INSERT INTO B values (?, ?, ?);", data)
    con.commit()


def runMariaDB(csvA, csvB, i):
    db = "mariaDB" + str(i)
    fname = "output_mariaDB" + str(i)
    cur, con = connectMariaDB(db)
    loadcsvA(csvA, cur, con)
    loadcsvB(csvB, cur, con)
    query1(cur, fname)
    query2(cur, fname)
    query3(cur, fname)
    query4(cur, fname)
    con.close()


def query1(cur, fname):
    cur.execute("SELECT * FROM A WHERE A1 <= 50;")
    _result = cur.fetchall() 
    cur.execute("SHOW profiles;")
    x = cur.fetchall()
    time = x[-1][1]
    with open(fname, "a") as f:
        f.write(f"1, {time}\n")


def query2(cur, fname):
    cur.execute("SELECT * FROM B ORDER BY B3;")
    _result = cur.fetchall() 
    cur.execute("SHOW profiles;")
    x = cur.fetchall()
    time = x[-1][1]
    with open(fname, "a") as f:
        f.write(f"2, {time}\n")


def query3(cur, fname):
    cur.execute("SELECT COUNT(*)/COUNT(DISTINCT B2) FROM B")
    _result = cur.fetchall() 
    cur.execute("SHOW profiles;")
    x = cur.fetchall()
    time = x[-1][1]
    with open(fname, "a") as f:
        f.write(f"3, {time}\n")


def query4(cur, fname):
    cur.execute("SELECT * FROM A INNER JOIN B ON A.A1 = B.B2;")
    _result = cur.fetchall() 
    cur.execute("SHOW profiles;")
    x = cur.fetchall()
    time = x[-1][1]
    with open(fname, "a") as f:
        f.write(f"4, {time}\n")