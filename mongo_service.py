from pymongo import MongoClient
from datetime import datetime
from langchain_core.messages import HumanMessage,AIMessage


connection_string = "mongodb://localhost:27017/"

def save_chat(data:dict):
    data["created_at"] = datetime.now()
    with MongoClient(connection_string) as client:
        client["DSClass"]["chat"].insert_one(data)

def fetch_chat(userid:str):
    with MongoClient(connection_string) as client:
        data = list(
            client["DSClass"]["chat"].find({"userid": userid}).sort("created_at", -1).limit(10)
        )

    messages = []
    for item in reversed(data):
        if item["role"] == "user":
            message = HumanMessage(content=item["content"])
        else:
            message = AIMessage(content=item["content"])
        messages.append(message)
    return messages
