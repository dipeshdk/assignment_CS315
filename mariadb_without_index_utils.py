import mariadb  
import csv

DATABASE_PATH = "./Databases/"

def connectMariaDB(db):
    con = mariadb.connect(user="root",
                        password = "",
                        host = "localhost",
                        port=3306)

    cur = con.cursor()
    cur.execute(f"DROP DATABASE IF IF EXISTS {db};")
    cur.execute(f"CREATE DATABASE {db};")
    cur.execute(f"USE {db};")
    cur.execute("DROP TABLE IF EXISTS A;")
    cur.execute("DROP TABLE IF EXISTS B;")
    cur.execute("CREATE TABLE A (A1 INTEGER , A2 TEXT);")
    cur.execute("CREATE TABLE B (B1 INTEGER , B2 INTEGER, B3 TEXT);")
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


def runMariaDbWithoutInd(csvA, csvB, i):
    db = "mariaDB" + str(i)
    cur, con = connectMariaDB(db)
    loadcsvA(csvA, cur, con)
    loadcsvB(csvB, cur, con)
    query1(cur,con)
    con.close()


def query1(cur, con):
    cur.execute("SELECT * FROM A WHERE A1 <= 50;")
    result = cur.fetchall()
    print(result)

# def query2(cur, con):
#     cur.execute("SELECT * FROM B ORDER BY B3;")
#     cur.fetchall()

# def query3(cur, con):
#     cur.execute("SELECT COUNT(*)/COUNT(DISTINCT B2) FROM B")
#     cur.fetchall()

# def query4(cur, con):
#     cur.execute("SELECT B1, B2, B3, A2 FROM INNER JOIN A, B; ;")
#     cur.fetchall()

