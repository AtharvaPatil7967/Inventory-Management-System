import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from models.database import Product, Sale, Inventory, db

def predict_low_stock():
    """
    Predicts which products will run out of stock soon based on historical sales data.
    Uses Linear Regression to forecast next day sales.
    """
    try:
        predictions = []
        
        # Get all products
        products = Product.query.all()
        
        for product in products:
            # Get sales history for this product
            sales = Sale.query.filter_by(product_id=product.product_id).order_by(Sale.sale_date).all()
            
            if not sales or len(sales) < 2:
                # Not enough data for prediction
                inventory = Inventory.query.filter_by(product_id=product.product_id).first()
                current_stock = inventory.stock_quantity if inventory else 0
                
                predictions.append({
                    'product_id': product.product_id,
                    'product_name': product.product_name,
                    'category': product.category,
                    'current_stock': current_stock,
                    'predicted_sales': 0,
                    'days_until_stockout': 'N/A',
                    'status': 'Insufficient Data',
                    'confidence': 'Low'
                })
                continue
            
            # Prepare data for regression
            # Convert dates to numerical values (days since first sale)
            first_sale_date = sales[0].sale_date
            X = []
            y = []
            
            for sale in sales:
                days_diff = (sale.sale_date - first_sale_date).days
                X.append([days_diff])
                y.append(sale.quantity_sold)
            
            X = np.array(X)
            y = np.array(y)
            
            # Train linear regression model
            model = LinearRegression()
            model.fit(X, y)
            
            # Predict sales for next day
            last_sale_date = sales[-1].sale_date
            days_since_first = (datetime.now().date() - first_sale_date).days
            predicted_sales = model.predict([[days_since_first]])[0]
            
            # Ensure prediction is not negative
            predicted_sales = max(0, predicted_sales)
            
            # Get current stock
            inventory = Inventory.query.filter_by(product_id=product.product_id).first()
            current_stock = inventory.stock_quantity if inventory else 0
            
            # Calculate days until stockout
            if predicted_sales > 0:
                days_until_stockout = int(current_stock / predicted_sales)
            else:
                days_until_stockout = 999  # Essentially infinite
            
            # Determine status
            if days_until_stockout <= 3 and predicted_sales > 0:
                status = '⚠️ Critical - Low Stock'
            elif days_until_stockout <= 7 and predicted_sales > 0:
                status = '⚠️ Warning - Stock Running Low'
            elif current_stock < 10:
                status = '⚠️ Low Stock'
            else:
                status = '✅ Healthy Stock'
            
            # Calculate confidence based on number of data points
            if len(sales) >= 5:
                confidence = 'High'
            elif len(sales) >= 3:
                confidence = 'Medium'
            else:
                confidence = 'Low'
            
            predictions.append({
                'product_id': product.product_id,
                'product_name': product.product_name,
                'category': product.category,
                'current_stock': current_stock,
                'predicted_sales': round(predicted_sales, 2),
                'days_until_stockout': days_until_stockout if days_until_stockout < 999 else 'N/A',
                'status': status,
                'confidence': confidence,
                'model_score': round(model.score(X, y), 2) if len(X) > 1 else 0
            })
        
        # Sort by days until stockout (critical items first)
        predictions.sort(key=lambda x: x['days_until_stockout'] if isinstance(x['days_until_stockout'], int) else 999)
        
        return {
            'success': True,
            'predictions': predictions,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'predictions': []
        }

def get_sales_trend_data():
    """
    Get sales trend data for visualization
    """
    try:
        # Get sales for last 30 days
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        sales = Sale.query.filter(Sale.sale_date >= thirty_days_ago).order_by(Sale.sale_date).all()
        
        # Aggregate by date
        sales_by_date = {}
        for sale in sales:
            date_str = sale.sale_date.strftime('%Y-%m-%d')
            if date_str not in sales_by_date:
                sales_by_date[date_str] = 0
            sales_by_date[date_str] += sale.quantity_sold
        
        # Convert to lists for Chart.js
        dates = sorted(sales_by_date.keys())
        quantities = [sales_by_date[date] for date in dates]
        
        return {
            'success': True,
            'dates': dates,
            'quantities': quantities
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def get_category_sales():
    """
    Get sales distribution by category
    """
    try:
        products = Product.query.all()
        category_sales = {}
        
        for product in products:
            sales = Sale.query.filter_by(product_id=product.product_id).all()
            total_sold = sum(sale.quantity_sold for sale in sales)
            
            if product.category not in category_sales:
                category_sales[product.category] = 0
            category_sales[product.category] += total_sold
        
        return {
            'success': True,
            'categories': list(category_sales.keys()),
            'sales': list(category_sales.values())
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
