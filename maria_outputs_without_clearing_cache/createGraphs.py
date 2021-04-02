import statistics as st
import matplotlib.pyplot as plt

dbnum = 9

time_mariadb = []
time_mariadbWithoutInd = []
time_mongodb = []
time_sqlite = []
extension = ".txt"


def get_time_maria(fname):
    with open(fname, "r") as f:
        data = f.readlines()
        dt = [[], [], [], []]
        
        for line in data:
            queryNum,time = line.split(',')
            time = time.strip()
            queryNum = int(queryNum) - 1
            dt[queryNum].append(time)

    return dt


def get_time_mongo(fname):
    with open(fname, "r") as f:
        data = f.readlines()
        dt = [[], [], [], []]

        for line in data:
            queryNum,time = line.split(',')
            time = time.strip()
            time = float(time) * 0.001
            queryNum = int(queryNum) - 1
            dt[queryNum].append(time)

    return dt


def get_time_sqlite(fname):
    with open(fname, "r") as f:
        data = f.readlines()
        dt = [[], [], [], []]
        
        for i,line in enumerate(data):
            cols = line.split(" ")
            queryNum = (i % 4)
            time = cols[3]
            dt[queryNum].append(time)

    return dt


for i in range(dbnum):
    fname = "output_mariaDB" + str(i) 
    x = get_time_maria(fname)
    time_mariadb.append(x)

    fname = "output_mariaDBWithoutInd" + str(i)
    x = get_time_maria(fname)
    time_mariadbWithoutInd.append(x)
    
    fname = "output_mongoDB" + str(i)
    x = get_time_mongo(fname)
    time_mongodb.append(x)

    fname = "output_sqlite" + str(i) + extension
    x = get_time_sqlite(fname)
    time_sqlite.append(x)


def calcFinalTable(time_db):
    finalTimeList = []
    for i in range(dbnum):
        td = []
        for querynum in range(4):
            tmp = [float(x) for x in time_db[i][querynum]]
            tmp.sort()
            # removing min and max elements
            tmp.pop(0)
            tmp = tmp[:-1]
            # now take average of remaining elements
            avg = round(st.mean(tmp)*1000, 2)
            stan_dev = round(st.stdev(tmp)*1000, 2)
            x = (avg,stan_dev)
            td.append(x)
        
        finalTimeList.append(td)
    return finalTimeList


finalTimeSqlite = calcFinalTable(time_sqlite)
finalTimeMongo = calcFinalTable(time_mongodb)
finalTimeMaria = calcFinalTable(time_mariadb)
finalTimeMariaWithoutInd = calcFinalTable(time_mariadbWithoutInd)


def genGraphPoints(timelist, querynum):
    y = []
    err = []
    for iter in timelist:
        a,b = iter[querynum]
        y.append(a)
        err.append(b)
    return y, err


def create_graph(querynum):
    x = [i+1 for i in range(dbnum)]
    y, y_err = genGraphPoints(finalTimeSqlite, querynum)
    plt.errorbar(x, y, yerr = y_err, label = "sqlite3")
    # plt.errorbar(x, y, label = "sqlite3")
    y, y_err = genGraphPoints(finalTimeMongo, querynum)
    plt.errorbar(x, y, yerr = y_err, label = "mongodb")
    # plt.errorbar(x, y, label = "mongodb")

    y, y_err = genGraphPoints(finalTimeMaria, querynum)
    plt.errorbar(x, y, yerr = y_err, label = "mariadb")
    # plt.errorbar(x, y, label = "mariadb")

    y, y_err = genGraphPoints(finalTimeMariaWithoutInd, querynum)
    plt.errorbar(x, y, yerr = y_err, label = "mariadb(without index)")
    # plt.errorbar(x, y, label = "mariadb(without index)")

    plt.xlabel("database number")
    plt.ylabel("time taken by the query(in ms)")
    plt.title(f"query-{querynum + 1} time analysis")
    plt.legend()
    plt.savefig(f"query-{querynum + 1} time analysis (cache enabled in mariadb) 8db")
    plt.show()


row_format = "{:<10} {:<25}" + "{:>10}" * dbnum
header = [i for i in range(1,10)]

def create_rows(querynum, id):
    qSqlite = genGraphPoints(finalTimeSqlite,querynum)
    qMaria = genGraphPoints(finalTimeMaria,querynum)
    qMongo = genGraphPoints(finalTimeMongo,querynum)
    qMariaWithoutInd = genGraphPoints(finalTimeMariaWithoutInd,querynum)
       
    print(row_format.format(f"query{querynum + 1}", "sqlite3", *qSqlite[id]))
    print(row_format.format(f"query{querynum + 1}", "mariadb(without index)", *qMariaWithoutInd[id]))
    print(row_format.format(f"query{querynum + 1}", "mariadb(with index)", *qMaria[id]))
    print(row_format.format(f"query{querynum + 1}", "mongodb", *qMongo[id]))
    print("-"*(10+25+(10*dbnum)+1))


def create_table(id):
    print(row_format.format("", "DBMS", *header))
    print("="*(10+25+(10*dbnum)+1))

    for i in range(4):
        create_rows(i,id)


create_table(0)
create_table(1)

# for i in range(4):
#     create_graph(i)
