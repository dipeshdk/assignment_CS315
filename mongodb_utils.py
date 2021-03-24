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
