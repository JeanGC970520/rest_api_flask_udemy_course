"""
- abort() method is using to help us document unsuccessful responses.

- With @blp.arguments() decorator, we can use a Schema
to validate data and this provide a validated data.
The validated data provided must be first in the 
arguments of decorated method

- With blp.response() decorator, we return a response
validated and with a specific HTTP status code
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found")
    
    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Item not found")\

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            # https://blog.teclado.com/python-dictionary-merge-update-operators/
            item |= item_data
            return item_data
        except KeyError:
            abort(404, message="Item not found")

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):  
        item = ItemModel(**item_data) # The operator ** in **item_model converts into kwargs

        try:
            db.session.add(item)
            db.session.commit()  # commit() method saves all added 
        except SQLAlchemyError:
            abort(500, message="An error ocurred while inserting the item")

        return item