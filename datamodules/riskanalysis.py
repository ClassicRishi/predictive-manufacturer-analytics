import pymongo as mongo
import pandas as pd

def returnFrame(collection,start,stop):
    riskanalysis = collection.find({"Machine_ID": {"$gte": start, "$lte": stop}},{ "Machine_ID": 1, 'Efficiency_Status': 1, 'Power_Consumption_kW': 1 })
    riskanalysis = list(riskanalysis)

    return pd.DataFrame(riskanalysis)