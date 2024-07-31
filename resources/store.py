"""
- abort() method is using to help us document unsuccessful responses.
"""

import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint("stores", __name__, description="Operations on stores")

# With the Blueprint flask_smorest knwons where enroute
# by example '/store/sf4jk23sdf-3sfjk-dsk2-a322'
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted"}
        except KeyError:
            abort(404, message="Store not found")

@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores" : list(stores.values())}

    def post(self):
        # Request is an object that Flask provides and contains iformation about the HTTP request
        store_data = request.get_json()
        if "name" not in store_data:
            abort(
                400, 
                message="Bad request. Ensure 'name' is included in the JSON payload"
            )
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"{store} already exist")
        store_id = uuid.uuid4().hex
        store = {
            "id" : store_id,
            **store_data,
        }
        stores[store_id] = store
        return store, 201