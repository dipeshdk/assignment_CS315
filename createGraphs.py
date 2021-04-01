import statistics as st
import matplotlib.pyplot as plt

dbnum = 6

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

    fname = "sqlite_output" + str(i) + extension
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
            avg = st.mean(tmp)
            stan_dev = st.stdev(tmp)
            x = (avg,stan_dev)
            td.append(x)
        
        finalTimeList.append(td)
    return finalTimeList


finalTimeSqlite = calcFinalTable(time_sqlite)
finalTimeMongo = calcFinalTable(time_mongodb)
finalTimeMaria = calcFinalTable(time_mariadb)
finalTimeMariaWithoutInd = calcFinalTable(time_mariadbWithoutInd)


def gen_y(timelist, querynum):
    q = []
    for dbno, iter in enumerate(timelist):
        a,_ = iter[querynum]
        q.append(a)
    return q


def create_graph(querynum):
    x = [i+1 for i in range(dbnum)]
    y = gen_y(finalTimeSqlite, querynum)
    plt.plot(x,y, label = "sqlite3")

    y = gen_y(finalTimeMongo, querynum)
    plt.plot(x,y, label = "mongodb")

    y = gen_y(finalTimeMaria, querynum)
    plt.plot(x,y, label = "mariadb")

    y = gen_y(finalTimeMariaWithoutInd, querynum)
    plt.plot(x,y, label = "mariadb(without index)")

    plt.xlabel("database number")
    plt.ylabel("time taken by the query")
    plt.title(f"query-{querynum} time analysis")
    plt.legend()
    plt.savefig(f"query-{querynum} time analysis")
    plt.show()


create_graph(0)
create_graph(1)
create_graph(2)
create_graph(3)

# use these lists to create graphs
# query 1 -> time taken by each dbms in each database
# basically 4 lines representing the 4 dbms
# and x axis pe 9 databases
# and y axis pe time
