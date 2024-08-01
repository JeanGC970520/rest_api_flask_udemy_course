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
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

# With the Blueprint flask_smorest knwons where enroute
# by example '/store/sf4jk23sdf-3sfjk-dsk2-a322'
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("Deleting a store is not implemented.")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            # This is a integrity error, occurs when any constraints was bailed
            abort(
                400,
                message="A store with that name already exists"
            )
        except SQLAlchemyError:
            abort(500, message="An error ocurred creating the store")
        
        return store