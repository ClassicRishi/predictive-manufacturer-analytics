import pymongo as mongo
import pandas as pd

def returnFrame(collection,start,stop):
    highrisk = collection.find({"Machine_ID": {"$gte": start, "$lte": stop}, "Efficiency_Status": {"$eq": "High"}},{ "Machine_ID": 1, 'Power_Consumption_kW': 1, 'Error_Rate_%': 1 })
    highrisk = list(highrisk)

    return pd.DataFrame(highrisk).groupby("Machine_ID").agg({
        "Error_Rate_%": "max",
        "Power_Consumption_kW": "max"
    }).reset_index()