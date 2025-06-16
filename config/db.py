from pymongo import MongoClient
db_connection = MongoClient("mongodb+srv://boat:123456789_Za@cluster0.rmsa1et.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = db_connection.myDB
collection = db["chat"]

collection_account = db["account"]

collection_line = db["account_Line"]
