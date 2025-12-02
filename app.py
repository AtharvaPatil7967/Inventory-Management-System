from flask import Flask, request, jsonify
from flask_cors import CORS
from database import Database
from datetime import datetime
import traceback

app = Flask(__name__)
CORS(app)

# Initialize database
db = Database()
db.connect()

# ==================== PRODUCTS ENDPOINTS ====================

@app.route('/products', methods=['GET'])
def get_products():
    """Get all products"""
    try:
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        return jsonify({"success": True, "data": products}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product by ID"""
    try:
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        cursor.close()
        
        if product:
            return jsonify({"success": True, "data": product}), 200
        return jsonify({"success": False, "error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/products', methods=['POST'])
def create_product():
    """Create new product"""
    try:
        data = request.get_json()
        cursor = db.get_cursor()
        
        sql = "INSERT INTO products (product_name, category, price) VALUES (%s, %s, %s)"
        values = (data['product_name'], data['category'], data['price'])
        
        cursor.execute(sql, values)
        db.connection.commit()
        product_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({
            "success": True, 
            "message": "Product created successfully",
            "product_id": product_id
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update existing product"""
    try:
        data = request.get_json()
        cursor = db.get_cursor()
        
        sql = "UPDATE products SET product_name=%s, category=%s, price=%s WHERE product_id=%s"
        values = (data['product_name'], data['category'], data['price'], product_id)
        
        cursor.execute(sql, values)
        db.connection.commit()
        cursor.close()
        
        return jsonify({"success": True, "message": "Product updated successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete product"""
    try:
        cursor = db.get_cursor()
        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        db.connection.commit()
        cursor.close()
        
        return jsonify({"success": True, "message": "Product deleted successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ==================== INVENTORY ENDPOINTS ====================

@app.route('/inventory', methods=['GET'])
def get_inventory():
    """Get all inventory with product details"""
    try:
        cursor = db.get_cursor()
        query = """
            SELECT i.*, p.product_name, p.category, p.price 
            FROM inventory i
            JOIN products p ON i.product_id = p.product_id
        """
        cursor.execute(query)
        inventory = cursor.fetchall()
        cursor.close()
        return jsonify({"success": True, "data": inventory}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/inventory', methods=['POST'])
def add_inventory():
    """Add inventory for a product"""
    try:
        data = request.get_json()
        cursor = db.get_cursor()
        
        sql = """INSERT INTO inventory (product_id, stock_quantity, restock_date, location) 
                 VALUES (%s, %s, %s, %s)"""
        values = (data['product_id'], data['stock_quantity'], 
                  data.get('restock_date'), data.get('location'))
        
        cursor.execute(sql, values)
        db.connection.commit()
        cursor.close()
        
        return jsonify({"success": True, "message": "Inventory added successfully"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/inventory/<int:inventory_id>', methods=['PUT'])
def update_inventory(inventory_id):
    """Update inventory stock levels"""
    try:
        data = request.get_json()
        cursor = db.get_cursor()
        
        sql = """UPDATE inventory SET stock_quantity=%s, restock_date=%s, location=%s 
                 WHERE inventory_id=%s"""
        values = (data['stock_quantity'], data.get('restock_date'), 
                  data.get('location'), inventory_id)
        
        cursor.execute(sql, values)
        db.connection.commit()
        cursor.close()
        
        return jsonify({"success": True, "message": "Inventory updated successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ==================== SUPPLIERS ENDPOINTS ====================

@app.route('/suppliers', methods=['GET'])
def get_suppliers():
    """Get all suppliers"""
    try:
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM suppliers")
        suppliers = cursor.fetchall()
        cursor.close()
        return jsonify({"success": True, "data": suppliers}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/suppliers', methods=['POST'])
def create_supplier():
    """Create new supplier"""
    try:
        data = request.get_json()
        cursor = db.get_cursor()
        
        sql = "INSERT INTO suppliers (supplier_name, contact_info, email) VALUES (%s, %s, %s)"
        values = (data['supplier_name'], data['contact_info'], data['email'])
        
        cursor.execute(sql, values)
        db.connection.commit()
        cursor.close()
        
        return jsonify({"success": True, "message": "Supplier created successfully"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ==================== PURCHASES ENDPOINTS ====================

@app.route('/purchases', methods=['GET'])
def get_purchases():
    """Get all purchases"""
    try:
        cursor = db.get_cursor()
        query = """
            SELECT p.*, s.supplier_name, pr.product_name
            FROM purchases p
            JOIN suppliers s ON p.supplier_id = s.supplier_id
            JOIN products pr ON p.product_id = pr.product_id
            ORDER BY p.purchase_date DESC
        """
        cursor.execute(query)
        purchases = cursor.fetchall()
        cursor.close()
        return jsonify({"success": True, "data": purchases}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/purchases', methods=['POST'])
def create_purchase():
    """Record a new purchase"""
    try:
        data = request.get_json()
        cursor = db.get_cursor()
        
        # Insert purchase record
        sql = """INSERT INTO purchases (supplier_id, product_id, quantity_purchased, 
                 purchase_date, purchase_price) VALUES (%s, %s, %s, %s, %s)"""
        values = (data['supplier_id'], data['product_id'], data['quantity_purchased'],
                  data['purchase_date'], data['purchase_price'])
        
        cursor.execute(sql, values)
        
        # Update inventory stock
        update_sql = """UPDATE inventory SET stock_quantity = stock_quantity + %s 
                        WHERE product_id = %s"""
        cursor.execute(update_sql, (data['quantity_purchased'], data['product_id']))
        
        db.connection.commit()
        cursor.close()
        
        return jsonify({"success": True, "message": "Purchase recorded successfully"}), 201
    except Exception as e:
        db.connection.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

# ==================== SALES ENDPOINTS ====================

@app.route('/sales', methods=['GET'])
def get_sales():
    """Get all sales"""
    try:
        cursor = db.get_cursor()
        query = """
            SELECT s.*, p.product_name, p.category
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            ORDER BY s.sale_date DESC
        """
        cursor.execute(query)
        sales = cursor.fetchall()
        cursor.close()
        return jsonify({"success": True, "data": sales}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/sales', methods=['POST'])
def create_sale():
    """Record a new sale"""
    try:
        data = request.get_json()
        cursor = db.get_cursor()
        
        # Check if sufficient stock available
        cursor.execute("SELECT stock_quantity FROM inventory WHERE product_id = %s", 
                      (data['product_id'],))
        result = cursor.fetchone()
        
        if not result or result['stock_quantity'] < data['quantity_sold']:
            return jsonify({"success": False, "error": "Insufficient stock"}), 400
        
        # Insert sale record
        sql = """INSERT INTO sales (product_id, quantity_sold, sale_date, 
                 sale_price, customer_name) VALUES (%s, %s, %s, %s, %s)"""
        values = (data['product_id'], data['quantity_sold'], data['sale_date'],
                  data['sale_price'], data.get('customer_name'))
        
        cursor.execute(sql, values)
        
        # Reduce inventory stock
        update_sql = """UPDATE inventory SET stock_quantity = stock_quantity - %s 
                        WHERE product_id = %s"""
        cursor.execute(update_sql, (data['quantity_sold'], data['product_id']))
        
        db.connection.commit()
        cursor.close()
        
        return jsonify({"success": True, "message": "Sale recorded successfully"}), 201
    except Exception as e:
        db.connection.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

# ==================== ANALYTICS ENDPOINTS ====================

@app.route('/analytics/low-stock', methods=['GET'])
def get_low_stock():
    """Get products with low stock (below threshold)"""
    try:
        threshold = request.args.get('threshold', 50, type=int)
        cursor = db.get_cursor()
        
        query = """
            SELECT i.*, p.product_name, p.category, p.price
            FROM inventory i
            JOIN products p ON i.product_id = p.product_id
            WHERE i.stock_quantity < %s
            ORDER BY i.stock_quantity ASC
        """
        cursor.execute(query, (threshold,))
        low_stock = cursor.fetchall()
        cursor.close()
        
        return jsonify({"success": True, "data": low_stock}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/analytics/sales-summary', methods=['GET'])
def get_sales_summary():
    """Get sales summary and revenue"""
    try:
        cursor = db.get_cursor()
        
        query = """
            SELECT 
                COUNT(*) as total_sales,
                SUM(quantity_sold) as total_quantity,
                SUM(sale_price * quantity_sold) as total_revenue,
                AVG(sale_price * quantity_sold) as avg_sale_value
            FROM sales
        """
        cursor.execute(query)
        summary = cursor.fetchone()
        cursor.close()
        
        return jsonify({"success": True, "data": summary}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/analytics/top-products', methods=['GET'])
def get_top_products():
    """Get top selling products"""
    try:
        limit = request.args.get('limit', 10, type=int)
        cursor = db.get_cursor()
        
        query = """
            SELECT p.product_name, p.category, 
                   SUM(s.quantity_sold) as total_sold,
                   SUM(s.sale_price * s.quantity_sold) as total_revenue
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            GROUP BY s.product_id
            ORDER BY total_sold DESC
            LIMIT %s
        """
        cursor.execute(query, (limit,))
        top_products = cursor.fetchall()
        cursor.close()
        
        return jsonify({"success": True, "data": top_products}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ==================== MAIN ====================
from models import InventoryAI

# Initialize AI model
ai_model = InventoryAI(db.connection)

# ==================== AI ENDPOINTS ====================

@app.route('/ai/predict-demand/<int:product_id>', methods=['GET'])
def predict_demand(product_id):
    """Predict future demand for a product"""
    try:
        days = request.args.get('days', 7, type=int)
        prediction = ai_model.predict_demand(product_id, days)
        
        if 'error' in prediction:
            return jsonify({"success": False, "error": prediction['error']}), 400
        
        return jsonify({"success": True, "data": prediction}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/ai/stock-alerts', methods=['GET'])
def stock_alerts():
    """Get low stock alerts with AI predictions"""
    try:
        days = request.args.get('days', 7, type=int)
        alerts = ai_model.detect_low_stock_alerts(days)
        
        if isinstance(alerts, dict) and 'error' in alerts:
            return jsonify({"success": False, "error": alerts['error']}), 400
        
        return jsonify({"success": True, "data": alerts, "count": len(alerts)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/ai/sales-trends', methods=['GET'])
def sales_trends():
    """Analyze sales trends"""
    try:
        product_id = request.args.get('product_id', type=int)
        trends = ai_model.analyze_sales_trends(product_id)
        
        if 'error' in trends:
            return jsonify({"success": False, "error": trends['error']}), 400
        
        return jsonify({"success": True, "data": trends}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Inventory Management System...")
    print("API will run on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
