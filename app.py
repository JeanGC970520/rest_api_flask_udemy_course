"""
- abort() method is using to help us document unsuccessful responses.
"""

import uuid
from flask import Flask, request
from flask_smorest import abort

from db import items, stores

app = Flask(__name__)

# All this compose a VIEW FUNCTION
# This is a Flask endpoint
@app.get("/store")
def get_stores():
    return {"stores" : list(stores.values())}

@app.post("/store")
def create_store():
    # Request is an object that Flask provides and contains iformation about the HTTP request
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {
        "id" : store_id,
        **store_data,
    }
    stores[store_id] = store
    return store, 201
''
# Dealing with URL parameters
@app.post("/item")
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")
    item_id = uuid.uuid4().hex
    item = {**item_data, "id" : item_id}
    items[item_id] = item
    return item, 201
        
@app.get("/item")
def get_all_items():
    return {"items" : list(items.values())}

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found")

@app.get("/item/<int:item_id>")
def get_item(item_id):
    try:
        return items[item_id], 200
    except KeyError:
        abort(404, message="Item not found")