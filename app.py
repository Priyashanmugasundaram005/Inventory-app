from flask import Flask
from models import db, init_default_locations
from views import product_bp, location_bp, movement_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Init DB
db.init_app(app)

@app.before_first_request
def ensure_db_initialized():
    with app.app_context():
        db.create_all()
        init_default_locations()

# Register Blueprints
app.register_blueprint(product_bp)
app.register_blueprint(location_bp)
app.register_blueprint(movement_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8089)
