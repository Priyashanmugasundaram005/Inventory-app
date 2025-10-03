from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import db, Product, ProductMovement, LOCATIONS
from datetime import datetime

# ---------------- Blueprints ----------------
product_bp = Blueprint('product', __name__)
location_bp = Blueprint('location', __name__)
movement_bp = Blueprint('movement', __name__)

# ---------------- Home / View Products ----------------
@product_bp.route('/', methods=['GET'])
def index():
    products = Product.query.all()
    enumerated_products = []
    for idx, product in enumerate(products):
        enumerated_products.append({
            'id': product.id,
            'index': idx + 1,
            'name': product.name,
            'price': product.price,
            'quantity': product.quantity,
            'location': product.location if product.location else "N/A"
        })
    return render_template('index.html', products=enumerated_products)

# ---------------- Add Product ----------------
@product_bp.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        location = request.form['location']

        # Check if a product with same name, price, and location already exists
        existing_product = Product.query.filter_by(
            name=name, 
            price=price, 
            location=location
        ).first()

        if existing_product:
            # Update quantity of existing product
            existing_product.quantity += quantity
            db.session.commit()
        else:
            # Create new product
            product = Product(name=name, price=price, quantity=quantity, location=location)
            db.session.add(product)
            db.session.commit()
        
        return redirect(url_for('product.index'))

    return render_template('add_product.html', locations=LOCATIONS)

# ---------------- Shift Product ----------------
@product_bp.route('/product/shift/<int:id>', methods=['GET', 'POST'])
def shift_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        old_location = product.location
        new_location = request.form.get('new_location')

        product.location = new_location
        db.session.commit()

        # Create movement record
        movement = ProductMovement(
            product_id=product.id,
            from_location=old_location,
            to_location=new_location,
            qty=product.quantity
        )
        db.session.add(movement)
        db.session.commit()

        return redirect(url_for('product.index'))

    return render_template('shift_product.html', product=product, locations=LOCATIONS)

# ---------------- Add Product Movement ----------------
@movement_bp.route('/movement/add', methods=['GET', 'POST'])
def add_movement():
    products = Product.query.all()

    if request.method == 'POST':
        product_id = request.form.get('product')
        from_location = request.form.get('from_location') or None
        to_location = request.form.get('to_location') or None
        qty = int(request.form.get('qty'))

        movement = ProductMovement(
            timestamp=datetime.now(),
            product_id=int(product_id),
            from_location=from_location,
            to_location=to_location,
            qty=qty
        )
        db.session.add(movement)
        db.session.commit()
        return redirect(url_for('movement.view_movement'))

    return render_template('add_movement.html', products=products, locations=LOCATIONS)

# ---------------- View Product Movements ----------------
@movement_bp.route('/movement/view', methods=['GET'])
def view_movement():
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('view_movement.html', movements=movements)

# ---------------- Delete Product ----------------
@product_bp.route('/product/delete/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        # Delete all movements related to this product
        ProductMovement.query.filter_by(product_id=product.id).delete()
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('product.index'))
    except Exception as e:
        db.session.rollback()
        return f"Error deleting product: {str(e)}"



# ---------------- Product Report ----------------
@product_bp.route('/product/report', methods=['GET'])
def product_report():
    product_balances = {}
    products = Product.query.all()
    for product in products:
        location_name = product.location
        product_info = {
            'name': product.name,
            'quantity': product.quantity,
            'price': product.price
        }
        if location_name not in product_balances:
            product_balances[location_name] = []
        product_balances[location_name].append(product_info)

    return render_template('report.html', product_balances=product_balances)
