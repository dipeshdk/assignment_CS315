import sqlite3
import csv
import time

import mariadb  
import pymongo 
import pandas as pd

DATABASE_PATH = "./Databases/"

def connectMongoDB(dbname):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[dbname]
    return db

def csv_to_json(filename):
    data = pd.read_csv(filename)
    return data.to_dict('records')


def runMongoDB(csvA, csvB, i):
    dbname = "mongoDB" + str(i)
    db = connectMongoDB(dbname)
    collectionA = db['A']
    collectionB = db['B']
    collectionA.insert_many(csv_to_json(DATABASE_PATH+csvA))
    collectionB.insert_many(csv_to_json(DATABASE_PATH+csvB))


def connectSqlite3(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(".timer ON")
    cur.execute("DROP TABLE IF EXISTS A;")
    cur.execute("DROP TABLE IF EXISTS B;")
    cur.execute("CREATE TABLE A (A1 INTEGER PRIMARY KEY, A2 TEXT);")
    cur.execute("CREATE TABLE B (B1 INTEGER PRIMARY KEY, B2 INTEGER, B3 TEXT, FOREIGN KEY (B2) REFRENCES A(A1) ON DELETE CASCADE)")
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


def runsqlite3(csvA, csvB, i):
    db = "sqliteDB" + str(i)
    cur, con = connectSqlite3(db)
    loadcsvA(csvA, cur, con)
    loadcsvB(csvB, cur, con)
    
def query1(cur, con):
    '''
        SELECT * 
        FROM A
        WHERE A1 <= 50
    '''
    cur.execute("SELECT * FROM A WHERE A1 <= 50;")
    cur.fetchall()

rollNumber = [2,4,9]
suffix = []
for x in rollNumber:
    for y in rollNumber:
        suffix.append(int((x*y) % 5))

databases = ["(A-100.csv,B-100-3-",
"(A-100.csv,B-100-5-",
"(A-100.csv,B-100-10-",
"(A-1000.csv,B-1000-5-",
"(A-1000.csv,B-1000-10-",
"(A-1000.csv,B-1000-50-",
"(A-10000.csv,B-10000-5-",
"(A-10000.csv,B-10000-50-",
"(A-10000.csv,B-10000-500-"]

addExtension = ".csv)"


for i in range(len(suffix)):
    databases[i] = databases[i] + str(suffix[i]) + addExtension

for i in range(len(databases)):
    csvA, csvB = databases[i].strip("()").split(",")
    print(csvA, csvB)
    # load these databases in sqlite3
    runsqlite3(csvA, csvB, i)
    # load these databases in mariadb(without index)
    runMongoDB(csvA, csvB, i)
    # load these databases in mariadb(with index)
    # load these databases in mongodb