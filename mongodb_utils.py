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
    db["A"].drop()
    db["B"].drop()
    collectionA = db["A"]
    collectionB = db["B"]
    collectionA.insert_many(csv_to_json(DATABASE_PATH+csvA))
    collectionB.insert_many(csv_to_json(DATABASE_PATH+csvB))
    query1(collectionA)
    query2(collectionB)
    query3(collectionB)
    query4(db)


def query1(collectionA):
    q1time = collectionA.find({"A1": {"$lte":50}}).explain()["executionStats"]["executionTimeMillis"]
    
def query2(collectionB):
    out = collectionB.aggregate([{"$sort":{"B3":1}}])
    
    for x in out:
        print(x)

def query3(collectionB):
    out = collectionB.aggregate([
        {"$group": { "_id": "$B2", "myCount": { "$sum": 1 } }},
        {"$group": { "_id": None, "val": { "$avg": "$myCount" } }}
    ])
    
    for x in out:
        print(x)

def query4(db):

    out = db["B"].aggregate([
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
    ])
    
    for x in out:
        print(x)