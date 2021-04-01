import sqlite3
import os
import time
import pandas as pd

DATABASE_PATH = "./Databases/"


def connectSqlite3(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS A;")
    cur.execute("DROP TABLE IF EXISTS B;")
    cur.execute("CREATE TABLE A (A1 INTEGER PRIMARY KEY, A2 TEXT);")
    cur.execute("CREATE TABLE B (B1 INTEGER PRIMARY KEY, B2 INTEGER, B3 TEXT, FOREIGN KEY (B2) REFERENCES A(A1) ON DELETE CASCADE);")
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


def runsqlite3(csvA, csvB, i):
    db = "sqliteDB" + str(i)
    cur, con = connectSqlite3(db)
    loadcsvA(csvA, cur, con)
    loadcsvB(csvB, cur, con)
    con.close()
    os.popen(f"./run_sqlite_queries.sh {i} >> output_sqlite{i}.txt")
    time.sleep(0.1)
    os.popen(f"rm -rf sql_query_result{i}.txt {db}")
    print(f"database {db} and its temp files deleted. output time stored in sqlite_output{i}.txt")
