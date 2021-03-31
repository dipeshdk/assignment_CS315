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
    query1(collectionA)
    query2(collectionB)
    # query3(collectionB)
    # query4(collectionA , collectionB)

def query1(collectionA):
    out = collectionA.find({"A1": {"$lte":50}}).explain()["executionStats"]["executionTimeMillis"]
    # for x in out:
    print(out, type(out))

def query2(collectionB):
    out = collectionB.explain()["verbosity"].aggregate([{"$sort":{"B3":1}}])
    print(out, type(out))

def query3(collectionB):
    out = collectionB.count()/collectionB.distinct("B2").count().explain()["executionStats"]["executionTimeMillis"]
    for x in out:
        print(x, type(x))

def query4(collectionA, collectionB):
    out = collectionB.aggregate([{"$lookup" : {"from" : "A", "localField": "B2", "foreignField": "A1", "as": "q4"}}]).explain()["executionStats"]["executionTimeMillis"]
    for x in out:
        print(x)