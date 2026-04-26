import streamlit as stl
import numpy as np
import pandas as pd
import plotly.express as px
from connection.Connect import MongoConnectDriver
from datamodules.powerconsumption import returnFrame as pc
from datamodules.temperature import returnFrame as temperature
from datamodules.networklatency import returnFrame as latency
from datamodules.efficiency import returnFrame as efficiency
from datamodules.riskanalysis import returnFrame as riskanalysis
from datamodules.productionspeed import returnFrame as production
from datamodules.earlywarning import returnFrame as earlywarning
from datamodules.downtime import returnFrame as downtime
from datamodules.datacards import returnActiveMachines as activemachines,returnTemperature,highPowerConsumption,highErrorRate,highPacketLoss,highProduction

stl.set_page_config(layout="wide",page_title="Predictive Maintenance and Anomaly Detection in 6G integrated systems",page_icon="📉")

stl.markdown("<h3 style='text-align: center;text-transform: uppercase'>📉 Predictive Maintenance and Anomaly Detection in <ins>6G integrated systems</ins></h3><hr />",unsafe_allow_html=True)

collection = MongoConnectDriver().connect()


col13,col14,col15,col16,col17,col18 = stl.columns([1,1,1,1,1,1])
with col13:
    stl.metric(label="Active Machines",value=activemachines(collection).iloc[0]['Machine_ID'],delta=str(activemachines(collection).iloc[0]['Machine_ID']-activemachines(collection).iloc[1]['Machine_ID'])+" from Idle",delta_arrow="off")
with col14:
    data = returnTemperature(collection).groupby("Machine_ID").agg({
        "Temperature_C": "max"
    }).reset_index()
    high_count = returnTemperature(collection).groupby('Machine_ID').agg({
        "Machine_ID": "count",
        "Temperature_C": "max"
    }).sort_values('Temperature_C',ascending=False).head(1)
    stl.metric(label="High Temperature",value=data['Temperature_C'].max(),delta_arrow="off",delta=str(high_count['Machine_ID'].iloc[0])+" machines")
with col15:
    data = highPowerConsumption(collection)
    stl.metric("High_Power", value=data["Power_Consumption_kW"].iloc[0], delta_arrow="off", delta='Machine - '+str(data['Machine_ID'].iloc[0]))
with col16:
    data = highErrorRate(collection)
    stl.metric("High Error Rate", value=data["Error_Rate_%"].iloc[0], delta_arrow="off", delta='Machine - '+str(data['Machine_ID'].iloc[0]))
with col17:
    data = highPacketLoss(collection)
    stl.metric("High Packet Loss", value=data["Packet_Loss_%"].iloc[0], delta_arrow="off", delta='Machine - '+str(data['Machine_ID'].iloc[0]))
with col18:
    data = highProduction(collection)
    stl.metric("High Production", value=data["Production_Speed_units_per_hr"].iloc[0], delta_arrow="off", delta='Machine - '+str(data['Machine_ID'].iloc[0]))

stl.markdown("<hr />",unsafe_allow_html=True)
slidercol = stl.slider("Select Machine Range",min_value=0,max_value=50,value=(10,45))

col1, col2 = stl.columns([2,2])
with col1:
    df1 = pc(collection,slidercol[0],slidercol[1])
    df1 = df1.groupby('Machine_ID').agg({
        'Power_Consumption_kW': "max"
    })
    fig = px.bar(df1,x=df1.index,y="Power_Consumption_kW")
    fig.update_layout({
        "title": "Power_Consumption_Analysis",
        "yaxis_range": [df1['Power_Consumption_kW'].min(), df1['Power_Consumption_kW'].max()],
    })
    stl.plotly_chart(fig)

with col2:
    df1 = riskanalysis(collection,slidercol[0],slidercol[1])
    df1 = df1.groupby('Efficiency_Status').agg({
        "Machine_ID": "count",
    })
    deviations = np.floor((df1['Machine_ID']/df1['Machine_ID'].max())*360)
    df1['deviations'] = deviations
    fig = px.bar_polar(df1,r='deviations',theta=df1.index,title="Anomaly Score")
    fig.update_layout(
        plot_bgcolor="black",
        polar=dict(
            bgcolor="#030a1b",
            radialaxis=dict(
                linecolor="black",linewidth=2,
                tickfont=dict(color="black"),
                gridcolor="white"
            ),
            angularaxis=dict(
                linecolor="white",linewidth=1,
                gridcolor="white"
            )
        )
    )
    stl.plotly_chart(fig)

stl.markdown("<hr />",unsafe_allow_html=True)

col3, col4 = stl.columns([2.5,1.5])
with col3:
    df1 = latency(collection)
    df1 = df1.groupby('Power_Consumption_kW').max('Network_Latency_ms').head(30)
    fig = px.bar(df1,x=df1.index,y="Network_Latency_ms")
    fig.update_layout({
        'title': "Latency VS Power"
    })
    stl.plotly_chart(fig)
with col4:
    df1 = efficiency(collection,slidercol[0],slidercol[1])
    df1 = df1.groupby('Efficiency_Status').agg({
        "Network_Latency_ms": "max",
        "Machine_ID": "count"
    })
    df1['machine_frequency'] = df1['Machine_ID']
    fig = px.bar(df1,x=df1.index,y="Network_Latency_ms",color="machine_frequency")
    fig.update_layout({
        'yaxis_range': [df1['Network_Latency_ms'].min()-0.05,df1['Network_Latency_ms'].max()],
        'title': "Efficiency Analysis"
    })
    stl.plotly_chart(fig)

stl.markdown("<hr />",unsafe_allow_html=True)

col5, col6 = stl.columns([2,2])
with col5:
    df1 = riskanalysis(collection,slidercol[0],slidercol[1])
    df1 = df1.groupby('Efficiency_Status').agg({
        'Machine_ID': "count",
        "Power_Consumption_kW": "max"
    })
    fig = px.pie(
        df1,
        names=[i+' Risk' for i in df1.index], values='Machine_ID',title="Risk Analysis",
    )
    fig.update_traces(pull=[0.3 if i == df1['Machine_ID'].min() else 0.01 for i in df1['Machine_ID']])
    stl.plotly_chart(fig)
with col6:
    df1 = temperature(collection,slidercol[0],slidercol[1])
    df1 = df1.groupby('Machine_ID').agg({
        "Temperature_C": "max",
        "Vibration_Hz": "max"
    }).reset_index()
    fig = px.bar(df1,x="Machine_ID",y="Temperature_C",color="Vibration_Hz")
    fig.update_layout({
        "title": "Temperature_Analysis",
        "yaxis_range": [df1['Temperature_C'].min(),df1['Temperature_C'].max()]
    })
    stl.plotly_chart(fig)

stl.markdown("<hr />",unsafe_allow_html=True)

col7, col8 = stl.columns([3.5,0.5])
productiondata = None
with col7:
    df1 = production(collection,slidercol[0],slidercol[1])
    df1 = df1.sort_values('Machine_ID').groupby('Machine_ID').max('Production_Speed_units_per_hr')
    productiondata = df1
    fig = px.bar(df1, x=df1.index,y="Production_Speed_units_per_hr")
    top3 = df1.reset_index().sort_values('Production_Speed_units_per_hr',ascending=False).head(3)
    fig.update_layout({
        "yaxis_title": "Production-Units_Hour",
        "yaxis_range": [df1['Production_Speed_units_per_hr'].min(), df1['Production_Speed_units_per_hr'].max()],
        "title": "Performance Analysis"
    })
    fig.update_traces(marker_color=["aqua" if i in list(top3['Production_Speed_units_per_hr']) else "#5588dd" for i in df1['Production_Speed_units_per_hr']])
    stl.plotly_chart(fig)
with col8:
    highest_lead_time = productiondata.sort_values('Production_Speed_units_per_hr',ascending=False).head(4)
    for i in range(0,3):
        stl.metric(label="High Production",value=highest_lead_time.iloc[i]['Production_Speed_units_per_hr'],delta=highest_lead_time.iloc[i]['Production_Speed_units_per_hr']-highest_lead_time.iloc[i+1]['Production_Speed_units_per_hr'])

stl.markdown("<hr />",unsafe_allow_html=True)

col9, col10 = stl.columns([3.5,0.5])
leadtimedata = None
with col9:
    df = earlywarning(collection,slidercol[0],slidercol[1])
    df1 = df[df['Efficiency_Status'] == 'Low'].sort_values('Machine_ID')
    df2 = df[df['Efficiency_Status'] == 'Medium'].sort_values('Machine_ID')
    df1['Datetime'] = pd.to_datetime(df1['Date']+" "+df1['Timestamp'],format="%d-%m-%Y %H:%M:%S")
    df2['Datetime'] = pd.to_datetime(df2['Date']+" "+df2['Timestamp'],format="%d-%m-%Y %H:%M:%S")
    df1 = df1.drop(columns=['Date','Timestamp'])
    df2 = df2.drop(columns=['Date','Timestamp'])
    df1 = df1.groupby("Machine_ID").agg({"Datetime": "max"}).reset_index()
    df2 = df2.groupby("Machine_ID").agg({"Datetime": "max"}).reset_index()
    df3 = pd.merge(df1, df2, on="Machine_ID", how="inner")
    df3['Leadtime'] = np.abs(df3['Datetime_x']-df3['Datetime_y'])
    df3['Leadtime'] = df3['Leadtime'].dt.total_seconds()/60
    top3 = df3.sort_values('Leadtime',ascending=False).head(3)
    leadtimedata = df3
    fig = px.bar(df3,x="Machine_ID",y="Leadtime")
    fig.update_layout(dict(yaxis_title="Leadtime(Minutes)",title="Failure Leadtime Analysis"))
    fig.update_traces(marker_color=["aqua" if i in list(top3['Leadtime']) else "#5588dd" for i in df3['Leadtime']])
    stl.plotly_chart(fig)
with col10:
    highest_lead_time = leadtimedata.sort_values('Leadtime',ascending=False).head(4)
    for i in range(0,3):
        stl.metric(label="Leadtime(Minutes)",value=highest_lead_time.iloc[i]['Leadtime'],delta=str(highest_lead_time.iloc[i]['Leadtime']-highest_lead_time.iloc[i+1]['Leadtime'])+' min')

stl.markdown("<hr />",unsafe_allow_html=True)

col11, col12 = stl.columns([3,1])
downtimeindex = None
with col11:
    df = downtime(collection,slidercol[0],slidercol[1])
    df = df.groupby('Machine_ID').agg({
        'Packet_Loss_%': "mean",
        'Predictive_Maintenance_Score': "mean",
        'Error_Rate_%': "mean"
    }).reset_index()
    df['Leadtime'] = leadtimedata['Leadtime']
    downtimeindex = df
    fig = px.bar(df,x='Machine_ID',y="Leadtime",color="Predictive_Maintenance_Score")
    stl.plotly_chart(fig)

with col12:
    top_maintenance = downtimeindex.groupby('Machine_ID').agg({
        "Predictive_Maintenance_Score": "max"
    }).reset_index().sort_values('Machine_ID',ascending=False).head(4)
    for i in range(0,3):
        stl.metric(label="Maintenance_Score",value=round(top_maintenance.iloc[i]['Predictive_Maintenance_Score'],6),delta=str(top_maintenance.iloc[i]['Predictive_Maintenance_Score']-top_maintenance.iloc[i+1]['Predictive_Maintenance_Score']))

stl.markdown("<hr />",unsafe_allow_html=True)