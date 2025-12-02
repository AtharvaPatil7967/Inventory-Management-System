from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    activity_logs = db.relationship('ActivityLog', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def get_id(self):
        return str(self.user_id)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'join_date': self.join_date.strftime('%Y-%m-%d %H:%M:%S') if self.join_date else None,
            'is_admin': self.is_admin
        }

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    action_type = db.Column(db.String(100), nullable=False)
    affected_table = db.Column(db.String(100), nullable=False)
    affected_id = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'log_id': self.log_id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'action_type': self.action_type,
            'affected_table': self.affected_table,
            'affected_id': self.affected_id,
            'description': self.description,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else None
        }

class Product(db.Model):
    __tablename__ = 'products'
    
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    # Relationships
    inventory = db.relationship('Inventory', backref='product', lazy=True, cascade='all, delete-orphan')
    sales = db.relationship('Sale', backref='product', lazy=True, cascade='all, delete-orphan')
    purchases = db.relationship('Purchase', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'category': self.category,
            'price': self.price
        }

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    supplier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_name = db.Column(db.String(200), nullable=False)
    contact_info = db.Column(db.String(200), nullable=False)
    
    # Relationships
    purchases = db.relationship('Purchase', backref='supplier', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'supplier_id': self.supplier_id,
            'supplier_name': self.supplier_name,
            'contact_info': self.contact_info
        }

class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    inventory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    restock_date = db.Column(db.Date, nullable=True)
    
    def to_dict(self):
        return {
            'inventory_id': self.inventory_id,
            'product_id': self.product_id,
            'product_name': self.product.product_name if self.product else None,
            'stock_quantity': self.stock_quantity,
            'restock_date': self.restock_date.strftime('%Y-%m-%d') if self.restock_date else None
        }

class Sale(db.Model):
    __tablename__ = 'sales'
    
    sale_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity_sold = db.Column(db.Integer, nullable=False)
    sale_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'sale_id': self.sale_id,
            'product_id': self.product_id,
            'product_name': self.product.product_name if self.product else None,
            'quantity_sold': self.quantity_sold,
            'sale_date': self.sale_date.strftime('%Y-%m-%d') if self.sale_date else None
        }

class Purchase(db.Model):
    __tablename__ = 'purchases'
    
    purchase_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)
    quantity_purchased = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'purchase_id': self.purchase_id,
            'product_id': self.product_id,
            'product_name': self.product.product_name if self.product else None,
            'supplier_id': self.supplier_id,
            'supplier_name': self.supplier.supplier_name if self.supplier else None,
            'quantity_purchased': self.quantity_purchased,
            'purchase_date': self.purchase_date.strftime('%Y-%m-%d') if self.purchase_date else None
        }

def init_db(app):
    """Initialize the database with sample data"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
        # Create default admin user if none exists
        if User.query.count() == 0:
            admin_user = User(
                username='admin',
                email='admin@inventory.com',
                is_admin=True
            )
            admin_user.set_password('admin123')  # Default password
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user created (username: admin, password: admin123)")
        
        # Check if database is empty
        if Product.query.count() == 0:
            # Add sample products
            products = [
                Product(product_name='Laptop', category='Electronics', price=899.99),
                Product(product_name='Mouse', category='Electronics', price=25.99),
                Product(product_name='Keyboard', category='Electronics', price=49.99),
                Product(product_name='Monitor', category='Electronics', price=199.99),
                Product(product_name='Desk Chair', category='Furniture', price=149.99),
                Product(product_name='Notebook', category='Stationery', price=3.99),
                Product(product_name='Pen Set', category='Stationery', price=12.99),
                Product(product_name='USB Cable', category='Electronics', price=8.99),
            ]
            db.session.add_all(products)
            db.session.commit()
            
            # Add sample suppliers
            suppliers = [
                Supplier(supplier_name='TechSupply Co.', contact_info='tech@supply.com'),
                Supplier(supplier_name='Office Depot', contact_info='sales@officedepot.com'),
                Supplier(supplier_name='FurniturePro', contact_info='info@furniturepro.com'),
            ]
            db.session.add_all(suppliers)
            db.session.commit()
            
            # Add sample inventory
            inventory_items = [
                Inventory(product_id=1, stock_quantity=50, restock_date=datetime(2025, 11, 15)),
                Inventory(product_id=2, stock_quantity=120, restock_date=datetime(2025, 11, 10)),
                Inventory(product_id=3, stock_quantity=80, restock_date=datetime(2025, 11, 12)),
                Inventory(product_id=4, stock_quantity=35, restock_date=datetime(2025, 11, 20)),
                Inventory(product_id=5, stock_quantity=25, restock_date=datetime(2025, 11, 18)),
                Inventory(product_id=6, stock_quantity=200, restock_date=datetime(2025, 11, 8)),
                Inventory(product_id=7, stock_quantity=150, restock_date=datetime(2025, 11, 9)),
                Inventory(product_id=8, stock_quantity=90, restock_date=datetime(2025, 11, 11)),
            ]
            db.session.add_all(inventory_items)
            db.session.commit()
            
            # Add sample sales
            sales = [
                Sale(product_id=1, quantity_sold=5, sale_date=datetime(2025, 10, 25)),
                Sale(product_id=2, quantity_sold=15, sale_date=datetime(2025, 10, 26)),
                Sale(product_id=1, quantity_sold=3, sale_date=datetime(2025, 10, 27)),
                Sale(product_id=3, quantity_sold=8, sale_date=datetime(2025, 10, 28)),
                Sale(product_id=4, quantity_sold=4, sale_date=datetime(2025, 10, 29)),
                Sale(product_id=2, quantity_sold=12, sale_date=datetime(2025, 10, 30)),
                Sale(product_id=6, quantity_sold=25, sale_date=datetime(2025, 10, 31)),
                Sale(product_id=7, quantity_sold=18, sale_date=datetime(2025, 11, 1)),
                Sale(product_id=1, quantity_sold=2, sale_date=datetime(2025, 11, 1)),
                Sale(product_id=5, quantity_sold=3, sale_date=datetime(2025, 11, 2)),
            ]
            db.session.add_all(sales)
            db.session.commit()
            
            # Add sample purchases
            purchases = [
                Purchase(product_id=1, supplier_id=1, quantity_purchased=30, purchase_date=datetime(2025, 10, 20)),
                Purchase(product_id=2, supplier_id=1, quantity_purchased=100, purchase_date=datetime(2025, 10, 21)),
                Purchase(product_id=5, supplier_id=3, quantity_purchased=20, purchase_date=datetime(2025, 10, 22)),
                Purchase(product_id=6, supplier_id=2, quantity_purchased=150, purchase_date=datetime(2025, 10, 23)),
            ]
            db.session.add_all(purchases)
            db.session.commit()
            
            print("Database initialized with sample data!")
