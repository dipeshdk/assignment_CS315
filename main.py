import time
from mongodb_utils import runMongoDB
from sqlite3_utils import runsqlite3
from mariadb_utils import runMariaDB
from mariadb_without_index_utils import runMariaDbWithoutInd
from chooseDatabases import getDatabases


rollNumber = [2,4,9]  # last 3 digits of your roll number 
databases = getDatabases(rollNumber)

for i in range(len(databases)):
    csvA, csvB = databases[i].strip("()").split(",")
    print(databases[i])
    runsqlite3(csvA, csvB, i)
    runMariaDbWithoutInd(csvA, csvB, i)
    runMariaDB(csvA, csvB, i)
    runMongoDB(csvA, csvB, i)
    time.sleep(0.1)


# csvA, csvB = databases[0].strip("()").split(",")
# # # runMongoDB(csvA, csvB, 8)
# # runsqlite3(csvA, csvB, 0)
# runMariaDB(csvA, csvB, 0)
# runMariaDbWithoutInd(csvA, csvB, 0)
