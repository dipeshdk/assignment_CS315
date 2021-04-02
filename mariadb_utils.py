import mariadb  
import pandas as pd

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
    cur.execute("SET GLOBAL query_cache_type = 0")
    cur.execute("SET GLOBAL query_cache_size = 0")
    cur.execute("DROP TABLE IF EXISTS A;")
    cur.execute("DROP TABLE IF EXISTS B;")
    cur.execute("CREATE TABLE A (A1 INTEGER PRIMARY KEY, A2 TEXT);")
    cur.execute("CREATE TABLE B (B1 INTEGER PRIMARY KEY, B2 INTEGER, B3 VARCHAR(500), FOREIGN KEY (B2) REFERENCES A(A1) ON DELETE CASCADE);")
    cur.execute("CREATE INDEX Bi on B(B3);")
    cur.execute(f"SET profiling = 1;")
    con.commit()
    return cur,con


def loadcsvA(csvfile, cur, con):
    data = pd.read_csv(DATABASE_PATH+csvfile)
    df = pd.DataFrame(data, columns= ['A1', 'A2'])
    for row in df.itertuples():
        cur.execute("INSERT INTO A values (?, ?);", (row.A1, row.A2))
    con.commit()


def loadcsvB(csvfile, cur, con):
    data = pd.read_csv(DATABASE_PATH+csvfile)
    df = pd.DataFrame(data, columns= ['B1', 'B2', 'B3'])
    for row in df.itertuples(): 
        cur.execute('''INSERT INTO B values (?, ?, ?);''', (row.B1, row.B2, row.B3))
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
    print(f"Open {fname} for the time taken for running queries by mariaDB")


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