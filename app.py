from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
import os
import sys

# Add models directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'models'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ai'))

from models.database import db, Product, Supplier, Inventory, Sale, Purchase, User, ActivityLog, init_db
from ai.predictor import predict_low_stock, get_sales_trend_data, get_category_sales

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize database
init_db(app)

# Helper function to log activities
def log_activity(action_type, affected_table, affected_id=None, description=None):
    """Log user activity"""
    if current_user.is_authenticated:
        activity = ActivityLog(
            user_id=current_user.user_id,
            action_type=action_type,
            affected_table=affected_table,
            affected_id=affected_id,
            description=description
        )
        db.session.add(activity)
        db.session.commit()

# ============= AUTHENTICATION ROUTES =============
@app.route('/')
def home():
    """Landing page with login/register options"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            log_activity('login', 'users', user.user_id, f'User {username} logged in')
            flash(f'Welcome back, {username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return render_template('register.html')
        
        # Create new user
        new_user = User(
            username=username,
            email=email
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    log_activity('logout', 'users', current_user.user_id, f'User {current_user.username} logged out')
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))

# ============= DASHBOARD (LOGGED IN HOME) =============
@app.route('/dashboard')
@login_required
def dashboard():
    """Personalized dashboard for logged-in users"""
    try:
        total_products = Product.query.count()
        total_sales = db.session.query(db.func.sum(Sale.quantity_sold)).scalar() or 0
        low_stock_count = Inventory.query.filter(Inventory.stock_quantity < 20).count()
        total_suppliers = Supplier.query.count()
        
        # Get recent sales
        recent_sales = Sale.query.order_by(Sale.sale_date.desc()).limit(5).all()
        
        # Get low stock items
        low_stock_items = db.session.query(Inventory, Product).join(
            Product, Inventory.product_id == Product.product_id
        ).filter(Inventory.stock_quantity < 20).limit(5).all()
        
        # Get user's recent activity
        recent_activities = ActivityLog.query.filter_by(
            user_id=current_user.user_id
        ).order_by(ActivityLog.timestamp.desc()).limit(10).all()
        
        # Get user stats
        user_actions_count = ActivityLog.query.filter_by(user_id=current_user.user_id).count()
        
        return render_template('dashboard.html',
                             total_products=total_products,
                             total_sales=total_sales,
                             low_stock_count=low_stock_count,
                             total_suppliers=total_suppliers,
                             recent_sales=recent_sales,
                             low_stock_items=low_stock_items,
                             recent_activities=recent_activities,
                             user_actions_count=user_actions_count)
    except Exception as e:
        return render_template('dashboard.html', error=str(e))

# ============= ACTIVITY LOG API =============
@app.route('/api/activity-log')
@login_required
def get_activity_log():
    """Get current user's activity log"""
    activities = ActivityLog.query.filter_by(
        user_id=current_user.user_id
    ).order_by(ActivityLog.timestamp.desc()).limit(50).all()
    return jsonify([a.to_dict() for a in activities])

@app.route('/api/activity-log/all')
@login_required
def get_all_activity_logs():
    """Get all users' activity logs (admin only)"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Admin access required'}), 403
    
    activities = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(100).all()
    return jsonify([a.to_dict() for a in activities])

# ============= PRODUCTS ROUTES =============
@app.route('/products')
@login_required
def products():
    """Products management page"""
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products (API)"""
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product (API)"""
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@app.route('/api/products', methods=['POST'])
@login_required
def create_product():
    """Create new product (API)"""
    try:
        data = request.get_json()
        product = Product(
            product_name=data['product_name'],
            category=data['category'],
            price=float(data['price'])
        )
        db.session.add(product)
        db.session.commit()
        
        # Also create inventory entry for new product
        inventory = Inventory(
            product_id=product.product_id,
            stock_quantity=data.get('initial_stock', 0),
            restock_date=datetime.now()
        )
        db.session.add(inventory)
        db.session.commit()
        
        # Log activity
        log_activity('add_product', 'products', product.product_id, f"Added product '{product.product_name}'")
        
        return jsonify({'success': True, 'product': product.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/products/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    """Update product (API)"""
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        
        product.product_name = data.get('product_name', product.product_name)
        product.category = data.get('category', product.category)
        product.price = float(data.get('price', product.price))
        
        db.session.commit()
        
        # Log activity
        log_activity('edit_product', 'products', product_id, f"Updated product '{product.product_name}'")
        
        return jsonify({'success': True, 'product': product.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    """Delete product (API)"""
    try:
        product = Product.query.get_or_404(product_id)
        product_name = product.product_name
        db.session.delete(product)
        db.session.commit()
        
        # Log activity
        log_activity('delete_product', 'products', product_id, f"Deleted product '{product_name}'")
        
        return jsonify({'success': True, 'message': 'Product deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# ============= SUPPLIERS ROUTES =============
@app.route('/suppliers')
@login_required
def suppliers():
    """Suppliers management page"""
    suppliers = Supplier.query.all()
    return render_template('suppliers.html', suppliers=suppliers)

@app.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    """Get all suppliers (API)"""
    suppliers = Supplier.query.all()
    return jsonify([s.to_dict() for s in suppliers])

@app.route('/api/suppliers/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    """Get single supplier (API)"""
    supplier = Supplier.query.get_or_404(supplier_id)
    return jsonify(supplier.to_dict())

@app.route('/api/suppliers', methods=['POST'])
@login_required
def create_supplier():
    """Create new supplier (API)"""
    try:
        data = request.get_json()
        supplier = Supplier(
            supplier_name=data['supplier_name'],
            contact_info=data['contact_info']
        )
        db.session.add(supplier)
        db.session.commit()
        log_activity('add_supplier', 'suppliers', supplier.supplier_id, f"Added supplier '{supplier.supplier_name}'")
        return jsonify({'success': True, 'supplier': supplier.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/suppliers/<int:supplier_id>', methods=['PUT'])
@login_required
def update_supplier(supplier_id):
    """Update supplier (API)"""
    try:
        supplier = Supplier.query.get_or_404(supplier_id)
        data = request.get_json()
        
        supplier.supplier_name = data.get('supplier_name', supplier.supplier_name)
        supplier.contact_info = data.get('contact_info', supplier.contact_info)
        
        db.session.commit()
        log_activity('edit_supplier', 'suppliers', supplier_id, f"Updated supplier '{supplier.supplier_name}'")
        return jsonify({'success': True, 'supplier': supplier.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/suppliers/<int:supplier_id>', methods=['DELETE'])
@login_required
def delete_supplier(supplier_id):
    """Delete supplier (API)"""
    try:
        supplier = Supplier.query.get_or_404(supplier_id)
        supplier_name = supplier.supplier_name
        db.session.delete(supplier)
        db.session.commit()
        log_activity('delete_supplier', 'suppliers', supplier_id, f"Deleted supplier '{supplier_name}'")
        return jsonify({'success': True, 'message': 'Supplier deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# ============= INVENTORY ROUTES =============
@app.route('/inventory')
@login_required
def inventory():
    """Inventory management page"""
    inventory_items = db.session.query(Inventory, Product).join(
        Product, Inventory.product_id == Product.product_id
    ).all()
    products = Product.query.all()
    return render_template('inventory.html', inventory_items=inventory_items, products=products)

@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    """Get all inventory items (API)"""
    inventory_items = Inventory.query.all()
    return jsonify([i.to_dict() for i in inventory_items])

@app.route('/api/inventory/<int:inventory_id>', methods=['PUT'])
@login_required
def update_inventory(inventory_id):
    """Update inventory (API)"""
    try:
        inventory = Inventory.query.get_or_404(inventory_id)
        data = request.get_json()
        
        old_quantity = inventory.stock_quantity
        inventory.stock_quantity = int(data.get('stock_quantity', inventory.stock_quantity))
        if 'restock_date' in data and data['restock_date']:
            inventory.restock_date = datetime.strptime(data['restock_date'], '%Y-%m-%d')
        
        db.session.commit()
        log_activity('edit_inventory', 'inventory', inventory_id, 
                    f"Updated stock for '{inventory.product.product_name}' from {old_quantity} to {inventory.stock_quantity}")
        return jsonify({'success': True, 'inventory': inventory.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# ============= SALES ROUTES =============
@app.route('/sales')
@login_required
def sales():
    """Sales management page"""
    sales_records = Sale.query.order_by(Sale.sale_date.desc()).all()
    products = Product.query.all()
    return render_template('sales.html', sales=sales_records, products=products)

@app.route('/api/sales', methods=['GET'])
def get_sales():
    """Get all sales (API)"""
    sales = Sale.query.all()
    return jsonify([s.to_dict() for s in sales])

@app.route('/api/sales', methods=['POST'])
@login_required
def create_sale():
    """Create new sale and update inventory (API)"""
    try:
        data = request.get_json()
        product_id = int(data['product_id'])
        quantity_sold = int(data['quantity_sold'])
        
        # Check inventory
        inventory = Inventory.query.filter_by(product_id=product_id).first()
        if not inventory:
            return jsonify({'success': False, 'error': 'Product not found in inventory'}), 400
        
        if inventory.stock_quantity < quantity_sold:
            return jsonify({'success': False, 'error': f'Insufficient stock. Available: {inventory.stock_quantity}'}), 400
        
        # Create sale record
        sale_date = datetime.strptime(data['sale_date'], '%Y-%m-%d') if 'sale_date' in data else datetime.now()
        sale = Sale(
            product_id=product_id,
            quantity_sold=quantity_sold,
            sale_date=sale_date
        )
        db.session.add(sale)
        
        # Update inventory
        inventory.stock_quantity -= quantity_sold
        
        db.session.commit()
        log_activity('sale_recorded', 'sales', sale.sale_id, 
                    f"Recorded sale of {quantity_sold} units of '{inventory.product.product_name}'")
        return jsonify({'success': True, 'sale': sale.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/sales/<int:sale_id>', methods=['DELETE'])
@login_required
def delete_sale(sale_id):
    """Delete sale (API)"""
    try:
        sale = Sale.query.get_or_404(sale_id)
        product_name = sale.product.product_name
        quantity = sale.quantity_sold
        
        # Restore inventory
        inventory = Inventory.query.filter_by(product_id=sale.product_id).first()
        if inventory:
            inventory.stock_quantity += sale.quantity_sold
        
        db.session.delete(sale)
        db.session.commit()
        log_activity('delete_sale', 'sales', sale_id, f"Deleted sale of {quantity} units of '{product_name}'")
        return jsonify({'success': True, 'message': 'Sale deleted and inventory restored'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# ============= PURCHASES ROUTES =============
@app.route('/api/purchases', methods=['GET'])
def get_purchases():
    """Get all purchases (API)"""
    purchases = Purchase.query.all()
    return jsonify([p.to_dict() for p in purchases])

@app.route('/api/purchases', methods=['POST'])
@login_required
def create_purchase():
    """Create new purchase and update inventory (API)"""
    try:
        data = request.get_json()
        product_id = int(data['product_id'])
        quantity_purchased = int(data['quantity_purchased'])
        
        # Create purchase record
        purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d') if 'purchase_date' in data else datetime.now()
        purchase = Purchase(
            product_id=product_id,
            supplier_id=int(data['supplier_id']),
            quantity_purchased=quantity_purchased,
            purchase_date=purchase_date
        )
        db.session.add(purchase)
        
        # Update inventory
        inventory = Inventory.query.filter_by(product_id=product_id).first()
        if inventory:
            inventory.stock_quantity += quantity_purchased
            inventory.restock_date = purchase_date
        
        db.session.commit()
        log_activity('purchase_recorded', 'purchases', purchase.purchase_id, 
                    f"Recorded purchase of {quantity_purchased} units of '{purchase.product.product_name}'")
        return jsonify({'success': True, 'purchase': purchase.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# ============= AI INSIGHTS ROUTES =============
@app.route('/ai-insights')
@login_required
def ai_insights():
    """AI insights and predictions page"""
    return render_template('ai_insights.html')

@app.route('/api/predict', methods=['GET'])
def predict():
    """AI prediction endpoint"""
    result = predict_low_stock()
    return jsonify(result)

@app.route('/api/sales-trend', methods=['GET'])
def sales_trend():
    """Sales trend data for charts"""
    result = get_sales_trend_data()
    return jsonify(result)

@app.route('/api/category-sales', methods=['GET'])
def category_sales():
    """Category sales data for charts"""
    result = get_category_sales()
    return jsonify(result)

# ============= ERROR HANDLERS =============
@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'error': 'Resource not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
