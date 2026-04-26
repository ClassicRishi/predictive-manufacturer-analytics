import pymongo as mongo
import pandas as pd

def returnFrame(collection,start,stop):
    highest_powerconsumption = collection.find({"Machine_ID": { "$gte": start, "$lte": stop }},{ "Machine_ID": 1, 'Power_Consumption_kW': 1 }).sort('Power_Consumption_kW',mongo.DESCENDING).limit(1000)
    highest_powerconsumption = list(highest_powerconsumption)

    return pd.DataFrame(highest_powerconsumption)