from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship('Location', backref='products')


class ProductMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    from_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)
    to_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product', backref='movements')
    from_location = db.relationship('Location', foreign_keys=[from_location_id], backref='outgoing_movements')
    to_location = db.relationship('Location', foreign_keys=[to_location_id], backref='incoming_movements')

# Function to initialize default locations
def init_default_locations():
    default_locations = ["Chennai", "Coimbatore", "Madurai", "Trichy", "Salem", "Bangalore"]
    for loc_name in default_locations:
        if not Location.query.filter_by(name=loc_name).first():
            db.session.add(Location(name=loc_name))
    db.session.commit()
