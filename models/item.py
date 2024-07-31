from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"),unique=False, nullable=False)
    # When we have a relationship attribute, we can ad another attribute to show the objects it is related to.
    store = db.relationship("StoreModel", back_populates="items")



