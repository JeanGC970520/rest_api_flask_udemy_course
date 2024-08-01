from marshmallow import Schema, fields

# This is an schema, definition of the behavior in terms of input and output 
# Helps us to validate incoming data and to convert output data according its schema
class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)

class ItemUpdateSchema(Schema):
    # Here one or both are optional
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema(), dump_only= True))
