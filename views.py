from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from models import db, Product, ProductMovement, Location, init_default_locations
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
            'location': product.location.name if product.location else "N/A"
        })
    return render_template('index.html', products=enumerated_products)

# ---------------- Add Product ----------------
@product_bp.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        location_id = int(request.form['location'])

        # Check if a product with same name, price, and location already exists
        existing_product = Product.query.filter_by(
            name=name, 
            price=price, 
            location_id=location_id
        ).first()

        if existing_product:
            # Update quantity of existing product
            existing_product.quantity += quantity
            db.session.commit()
            flash('Product quantity updated successfully!', 'success')
        else:
            # Create new product
            product = Product(name=name, price=price, quantity=quantity, location_id=location_id)
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully!', 'success')
        
        return redirect(url_for('product.index'))

    locations = Location.query.all()
    return render_template('add_product.html', locations=locations)

# ---------------- Shift Product ----------------
@product_bp.route('/product/shift/<int:id>', methods=['GET', 'POST'])
def shift_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        old_location_id = product.location_id
        new_location_id = request.form.get('new_location')

        product.location_id = new_location_id
        db.session.commit()

        # Create movement record
        movement = ProductMovement(
            product_id=product.id,
            from_location_id=old_location_id,
            to_location_id=new_location_id,
            qty=product.quantity
        )
        db.session.add(movement)
        db.session.commit()
        flash('Product location updated successfully!', 'success')

        return redirect(url_for('product.index'))

    locations = Location.query.all()
    return render_template('shift_product.html', product=product, locations=locations)

# ---------------- Add Product Movement ----------------
@movement_bp.route('/movement/add', methods=['GET', 'POST'])
def add_movement():
    products = Product.query.all()

    if request.method == 'POST':
        product_id = request.form.get('product')
        from_location_id = request.form.get('from_location') or None
        to_location_id = request.form.get('to_location') or None
        qty = int(request.form.get('qty'))

        movement = ProductMovement(
            timestamp=datetime.now(),
            product_id=int(product_id),
            from_location_id=from_location_id,
            to_location_id=to_location_id,
            qty=qty
        )
        db.session.add(movement)
        db.session.commit()
        flash('Movement recorded successfully!', 'success')
        return redirect(url_for('movement.view_movement'))

    locations = Location.query.all()
    return render_template('add_movement.html', products=products, locations=locations)

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
    products = Product.query.join(Location).all()
    for product in products:
        location_name = product.location.name
        product_info = {
            'name': product.name,
            'quantity': product.quantity,
            'price': product.price
        }
        if location_name not in product_balances:
            product_balances[location_name] = []
        product_balances[location_name].append(product_info)

    return render_template('report.html', product_balances=product_balances)

# ---------------- Location Management ----------------
@location_bp.route('/location/manage', methods=['GET'])
def manage_locations():
    locations = Location.query.all()
    return render_template('manage_locations.html', locations=locations)

@location_bp.route('/location/add', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        name = request.form['name']
        
        # Check if location already exists
        if Location.query.filter_by(name=name).first():
            flash('Location already exists!', 'error')
            return redirect(url_for('location.add_location'))
        
        location = Location(name=name)
        db.session.add(location)
        db.session.commit()
        flash('Location added successfully!', 'success')
        return redirect(url_for('location.manage_locations'))
    
    return render_template('add_location.html')

@location_bp.route('/location/edit/<int:id>', methods=['GET', 'POST'])
def edit_location(id):
    location = Location.query.get_or_404(id)
    
    if request.method == 'POST':
        new_name = request.form['name']
        
        # Check if another location with same name exists
        existing = Location.query.filter_by(name=new_name).first()
        if existing and existing.id != id:
            flash('Location name already exists!', 'error')
            return redirect(url_for('location.edit_location', id=id))
        
        location.name = new_name
        db.session.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('location.manage_locations'))
    
    return render_template('edit_location.html', location=location)

@location_bp.route('/location/delete/<int:id>', methods=['POST'])
def delete_location(id):
    location = Location.query.get_or_404(id)
    
    # Check if location has products
    if location.products:
        flash('Cannot delete location that has products! Move or delete products first.', 'error')
        return redirect(url_for('location.manage_locations'))
    
    try:
        db.session.delete(location)
        db.session.commit()
        flash('Location deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting location: {str(e)}', 'error')
    
    return redirect(url_for('location.manage_locations'))
