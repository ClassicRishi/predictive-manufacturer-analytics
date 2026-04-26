import pymongo as mongo
import pandas as pd

def returnFrame(collection,start,stop):
    production = collection.find({"Machine_ID": {"$gte": start, "$lte": stop}},{ "Machine_ID": 1, 'Production_Speed_units_per_hr': 1}).sort('Production_Speed_units_per_hr',mongo.DESCENDING).limit(300)
    production = list(production)

    return pd.DataFrame(production)