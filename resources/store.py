"""
- abort() method is using to help us document unsuccessful responses.

- With @blp.arguments() decorator, we can use a Schema
to validate data and this provide a validated data.
The validated data provided must be first in the 
arguments of decorated method

- With blp.response() decorator, we return a response
validated and with a specific HTTP status code
"""

import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

# With the Blueprint flask_smorest knwons where enroute
# by example '/store/sf4jk23sdf-3sfjk-dsk2-a322'
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
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
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"{store} already exist")
        store_id = uuid.uuid4().hex
        store = {
            "id" : store_id,
            **store_data,
        }
        stores[store_id] = store
        return store