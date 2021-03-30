from mongodb_utils import runMongoDB
from sqlite3_utils import runsqlite3
from mariadb_utils import runMariaDB

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
    # print(csvA, csvB)
    # load these databases in sqlite3
    runsqlite3(csvA, csvB, i)
    # load these databases in mariadb(without index)
    # runMongoDB(csvA, csvB, i)
    # load these databases in mariadb(with index)
    # runMariaDB(csvA, csvB, i)
    # load these databases in mongodb

# csvA, csvB = databases[0].strip("()").split(",")
# # runMongoDB(csvA, csvB, 0)
# runsqlite3(csvA, csvB, 0)
# # runMariaDB(csvA, csvB, 0)
