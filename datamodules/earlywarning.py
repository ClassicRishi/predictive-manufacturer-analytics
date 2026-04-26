import pymongo as mongo
import pandas as pd

def returnFrame(collection,start,stop):
    production = collection.find({"Efficiency_Status": { "$in": ["Medium","Low"] },"Machine_ID": {"$gte": start, "$lte": stop}},{ "Machine_ID": 1, 'Date': 1, "Timestamp": 1, "Efficiency_Status": 1, "Temperature_C": 1})
    production = list(production)

    return pd.DataFrame(production)