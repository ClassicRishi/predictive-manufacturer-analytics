import pymongo as mongo
import pandas as pd

def returnFrame(collection,start,stop):
    temperature = collection.find({"Machine_ID": {"$gte": start, "$lte": stop}},{ "Machine_ID": 1, 'Temperature_C': 1, 'Vibration_Hz': 1 }).sort('Temperature_C',mongo.DESCENDING).limit(300)
    temperature = list(temperature)

    return pd.DataFrame(temperature)