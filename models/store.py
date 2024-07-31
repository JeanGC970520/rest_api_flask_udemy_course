from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    # lazy="dynamic" prevent to SQLAlchemy get the Items and we make manually when need it.
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")

