import pymongo as mongo
import pandas as pd

def returnFrame(collection,start,stop):
    efficiency = collection.find({"Machine_ID": {"$gte": start, "$lte": stop}},{ "Machine_ID": 1, "Efficiency_Status": 1,'Network_Latency_ms': 1, 'Network_Latency_ms': 1 }).sort('Network_Latency_ms',mongo.DESCENDING)
    efficiency = list(efficiency)

    return pd.DataFrame(efficiency)