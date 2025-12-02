import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class InventoryAI:
    """AI models for inventory prediction and forecasting"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.demand_model = LinearRegression()
        
    def predict_demand(self, product_id, days_ahead=7):
        """Predict future demand for a product"""
        try:
            cursor = self.db.cursor(dictionary=True)
            
            # Get historical sales data
            query = """
                SELECT sale_date, SUM(quantity_sold) as daily_quantity
                FROM sales
                WHERE product_id = %s
                GROUP BY sale_date
                ORDER BY sale_date
            """
            cursor.execute(query, (product_id,))
            sales_data = cursor.fetchall()
            cursor.close()
            
            if len(sales_data) < 7:
                return {"error": "Insufficient historical data (need at least 7 days)"}
            
            # Prepare data
            df = pd.DataFrame(sales_data)
            df['sale_date'] = pd.to_datetime(df['sale_date'])
            df['day_number'] = (df['sale_date'] - df['sale_date'].min()).dt.days
            
            # Train model
            X = df[['day_number']].values
            y = df['daily_quantity'].values
            
            self.demand_model.fit(X, y)
            
            # Predict future demand
            last_day = df['day_number'].max()
            future_days = np.array([[last_day + i] for i in range(1, days_ahead + 1)])
            predictions = self.demand_model.predict(future_days)
            predictions = np.maximum(predictions, 0)  # No negative predictions
            
            # Prepare results
            forecast = []
            for i, pred in enumerate(predictions):
                forecast_date = df['sale_date'].max() + timedelta(days=i+1)
                forecast.append({
                    "date": forecast_date.strftime('%Y-%m-%d'),
                    "predicted_quantity": round(float(pred), 2)
                })
            
            total_predicted = sum([f['predicted_quantity'] for f in forecast])
            
            return {
                "product_id": product_id,
                "forecast_period": f"{days_ahead} days",
                "total_predicted_demand": round(total_predicted, 2),
                "daily_forecast": forecast,
                "model_score": round(self.demand_model.score(X, y), 2)
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def detect_low_stock_alerts(self, threshold_days=7):
        """Detect products that may run out of stock"""
        try:
            cursor = self.db.cursor(dictionary=True)
            
            # Get current inventory
            cursor.execute("""
                SELECT i.product_id, p.product_name, i.stock_quantity
                FROM inventory i
                JOIN products p ON i.product_id = p.product_id
            """)
            inventory = cursor.fetchall()
            
            alerts = []
            for item in inventory:
                # Predict demand for next 7 days
                prediction = self.predict_demand(item['product_id'], threshold_days)
                
                if 'error' not in prediction:
                    predicted_demand = prediction['total_predicted_demand']
                    current_stock = item['stock_quantity']
                    
                    if current_stock < predicted_demand:
                        shortage = predicted_demand - current_stock
                        alerts.append({
                            "product_id": item['product_id'],
                            "product_name": item['product_name'],
                            "current_stock": current_stock,
                            "predicted_demand": round(predicted_demand, 2),
                            "shortage": round(shortage, 2),
                            "recommended_reorder": round(shortage * 1.2, 2),  # 20% buffer
                            "alert_level": "CRITICAL" if shortage > current_stock else "WARNING"
                        })
            
            cursor.close()
            return alerts
            
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_sales_trends(self, product_id=None):
        """Analyze sales trends and patterns"""
        try:
            cursor = self.db.cursor(dictionary=True)
            
            if product_id:
                query = """
                    SELECT DATE_FORMAT(sale_date, '%Y-%m') as month,
                           SUM(quantity_sold) as total_quantity,
                           SUM(sale_price * quantity_sold) as total_revenue,
                           COUNT(*) as num_transactions
                    FROM sales
                    WHERE product_id = %s
                    GROUP BY month
                    ORDER BY month DESC
                    LIMIT 12
                """
                cursor.execute(query, (product_id,))
            else:
                query = """
                    SELECT DATE_FORMAT(sale_date, '%Y-%m') as month,
                           SUM(quantity_sold) as total_quantity,
                           SUM(sale_price * quantity_sold) as total_revenue,
                           COUNT(*) as num_transactions
                    FROM sales
                    GROUP BY month
                    ORDER BY month DESC
                    LIMIT 12
                """
                cursor.execute(query)
            
            trends = cursor.fetchall()
            cursor.close()
            
            return {
                "product_id": product_id if product_id else "all_products",
                "period": "last_12_months",
                "trends": trends
            }
            
        except Exception as e:
            return {"error": str(e)}
