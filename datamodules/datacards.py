import pymongo as mongo
import pandas as pd

def returnActiveMachines(collection):
    active_status = collection.find({}, {"Machine_ID": 1, 'Operation_Mode': 1})
    active_status = list(active_status)
    return pd.DataFrame(active_status).groupby('Operation_Mode').agg({
        'Machine_ID': "count"
    }).reset_index()

def returnTemperature(collection):
    temperature = collection.find({}, {"Machine_ID": 1, 'Temperature_C': 1})
    temperature = list(temperature)
    return pd.DataFrame(temperature)

def highPowerConsumption(collection):
    powerconsumption = collection.find({}, {"Machine_ID": 1, "Power_Consumption_kW": 1})
    powerconsumption = list(powerconsumption)
    df = pd.DataFrame(powerconsumption)
    df = df.groupby('Machine_ID').agg({
        "Power_Consumption_kW": "max"
    }).reset_index().sort_values('Power_Consumption_kW',ascending=False).head(1)
    return df

def highErrorRate(collection):
    error_rate = collection.find({}, {"Machine_ID": 1, "Error_Rate_%": 1})
    error_rate = list(error_rate)
    df = pd.DataFrame(error_rate)
    df = df.groupby('Machine_ID').agg({
        "Error_Rate_%": "max"
    }).reset_index().sort_values('Error_Rate_%',ascending=False).head(1)
    return df

def highPacketLoss(collection):
    packetloss = collection.find({}, {"Machine_ID": 1, "Packet_Loss_%": 1})
    packetloss = list(packetloss)
    df = pd.DataFrame(packetloss)
    df = df.groupby('Machine_ID').agg({
        "Packet_Loss_%": "max"
    }).reset_index().sort_values('Packet_Loss_%',ascending=False).head(1)
    return df

def highProduction(collection):
    production = collection.find({}, {"Machine_ID": 1, "Production_Speed_units_per_hr": 1})
    production = list(production)
    df = pd.DataFrame(production)
    df = df.groupby('Machine_ID').agg({
        "Production_Speed_units_per_hr": "max"
    }).reset_index().sort_values('Production_Speed_units_per_hr',ascending=False).head(1)
    return df