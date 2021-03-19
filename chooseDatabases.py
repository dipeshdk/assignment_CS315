import sqlite3
import csv

rollNumber = [2,4,9]
suffix = []
for x in rollNumber:
    for y in rollNumber:
        suffix.append(int((x*y)/5))

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


def connectSqlite3(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    return cur,con

def loadTableInSqlite3(cur, con, csvfile, identifier):
    col1 = str(identifier) + "1"
    col2 = str(identifier) + "2"
    cur.execute(f"DROP TABLE IF EXISTS table{identifier};")
    cur.execute(f"CREATE TABLE table{identifier} ({col1}, {col2});")
    
    with open("./Databases/"+csvfile, 'r') as f:
        dr = csv.DictReader(f) 
        flag = 0
        data = [(i[col1], i[col2]) for i in dr]
        
    cur.executemany("INSERT INTO tableA values (?,?);", data)
    con.commit()

for i in range(len(databases)):
    # load these databases in sqlite3
    csvA, csvB = databases[0].strip("()").split(",")
    db = "DB" + str(i)
    cur, con = connectSqlite3(db)
    loadTableInSqlite3(cur, con, csvA, "A")
    loadTableInSqlite3(cur, con, csvB, "b")
# load these databases in mariadb(without index)
# load these databases in mariadb(with index)
# load these databases in mongodb