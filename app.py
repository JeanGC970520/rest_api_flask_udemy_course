from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name" : "My Store",
        "items" : [
            {
                "name" : "Chair",
                "price" : 15.99,
            },
        ],
    },
]

# All this compose a VIEW FUNCTION
# This is a Flask endpoint
@app.get("/store")
def get_store():
    return {"stores" : stores}

@app.post("/store")
def create_store():
    # Request is an object that Flask provides and contains iformation about the HTTP request
    request_data = request.get_json()
    new_store = {
        "name" : request_data["name"],
        "items" : [],
    }
    stores.append(new_store)
    return new_store, 201

# Dealing with URL parameters
@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                "name" : request_data['name'],
                "price" : request_data['price'],
            }
            store['items'].append(new_item)
            return new_item, 201
    return {"message" : "Store not found"}, 404
        

