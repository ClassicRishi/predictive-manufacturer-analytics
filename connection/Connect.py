import pymongo as mongo
import streamlit as stl

class MongoConnectDriver:
    def __init__(self) -> None:
        self.client = mongo.MongoClient(stl.secrets.get("MONGODB_URI"))
        self.db = self.client[stl.secrets.get("DB")]
        self.collection = self.db[stl.secrets.get("COLLECTION")]
    def connect(self):
        return self.collection