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