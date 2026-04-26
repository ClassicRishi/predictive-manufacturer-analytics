import pymongo as mongo
import pandas as pd

def returnFrame(collection):
    latency = collection.find({},{ "Power_Consumption_kW": 1, 'Network_Latency_ms': 1, 'Network_Latency_ms': 1 }).sort('Network_Latency_ms',mongo.DESCENDING)
    latency = list(latency)

    return pd.DataFrame(latency)