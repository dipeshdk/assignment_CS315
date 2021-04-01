import pymongo
import pandas as pd

DATABASE_PATH = "./Databases/"

def connectMongoDB(dbname):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    client.drop_database(dbname)
    db = client[dbname]
    return db


def csv_to_json(filename):
    data = pd.read_csv(filename)
    return data.to_dict('records')


def runMongoDB(csvA, csvB, i):
    dbname = "mongoDB" + str(i)
    fname = "output_mongoDB" + str(i)
    db = connectMongoDB(dbname)
    collectionA = db["A"]
    collectionB = db["B"]
    collectionA.insert_many(csv_to_json(DATABASE_PATH+csvA))
    collectionB.insert_many(csv_to_json(DATABASE_PATH+csvB))
    db.set_profiling_level(2)
    query1(db, fname)
    query2(db, fname)
    query3(db, fname)
    query4(db, fname)
    print(f"Open {fname} for the time taken for running queries by mongoDB")


def query1(db,fname):
    q1time = db["A"].find({"A1": {"$lte":50}}).explain()["executionStats"]["executionTimeMillis"]
    with open(fname, "a") as f:
        f.write(f"1, {q1time}\n")
    
    

def query2(db,fname):
    out = db["B"].aggregate(pipeline=[{"$sort":{"B3":1}}],  allowDiskUse =  True )
    x = db.profiling_info()
    with open(fname, "a") as f:
        f.write(f"2, {x[-1]['millis']}\n")    


def query3(db,fname):
    out = db["B"].aggregate(pipeline=[
        {"$group": { "_id": "$B2", "countb2": { "$sum": 1 } }},
        {"$group": { "_id": None, "result": { "$avg": "$countb2" } }}
    ], allowDiskUse = True)
    x = db.profiling_info()
    with open(fname, "a") as f:
        f.write(f"3, {x[-1]['millis']}\n")


def query4(db,fname):
    out = db["B"].aggregate(pipeline=[
        {
            "$lookup":{
                "from": "A",
                "localField" : "B2",
                "foreignField" : "A1",
                "as" : "q4"
            }
        },
        {
        "$replaceRoot": { "newRoot": { "$mergeObjects": [ { "$arrayElemAt": [ "$q4", 0 ] }, "$$ROOT" ] } }
        },
        { "$project": { "B1":1,"B2":1,"B3":1,"A2":1  } }
    ], allowDiskUse = True)
    x = db.profiling_info()
    with open(fname, "a") as f:
        f.write(f"4, {x[-1]['millis']}\n")