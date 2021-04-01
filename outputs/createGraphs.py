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


for i in range(dbnum):
    for querynum in range(4):
        tmp = [float(x) for x in time_sqlite[i][querynum]]
        tmp.sort()
        tmp.pop(0)
        tmp = tmp[:-1]
# use these lists to create graphs