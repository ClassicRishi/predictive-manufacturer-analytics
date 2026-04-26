import pymongo as mongo
import pandas as pd

def returnFrame(collection,start,stop):
    downtimeanalysis = collection.find({"Machine_ID": {"$gte": start, "$lte": stop}},{ "Machine_ID": 1, 'Predictive_Maintenance_Score': 1, 'Packet_Loss_%': 1, 'Error_Rate_%': 1})
    downtimeanalysis = list(downtimeanalysis)

    return pd.DataFrame(downtimeanalysis)