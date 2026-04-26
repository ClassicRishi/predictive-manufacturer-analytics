import pymongo as mongo
import streamlit as stl

class MongoConnectDriver:
    def __init__(self) -> None:
        self.client = mongo.MongoClient(stl.secrets.get("MONGODB_URI"))
        self.db = self.client['manufacturers']
        self.collection = self.db['records']
    def connect(self):
        return self.collection