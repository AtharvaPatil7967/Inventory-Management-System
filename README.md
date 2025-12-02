# Inventory Management System 📦

A complete web-based inventory management system built with Flask, Bootstrap 5, and Machine Learning for stock prediction.

## 🌟 Features

### Core Functionality
- **Product Management**: Add, edit, delete, and view products with categories and pricing
- **Supplier Management**: Maintain supplier information and contacts
- **Inventory Tracking**: Real-time stock level monitoring with low stock alerts
- **Sales Recording**: Record sales transactions with automatic inventory updates
- **Purchase Management**: Track purchases from suppliers

### AI-Powered Insights 🧠
- **Stock Prediction**: Uses Linear Regression to predict which products will run out of stock
- **Sales Forecasting**: Predicts expected daily sales for each product
- **Visual Analytics**: Interactive charts showing:
  - Sales trends over the last 30 days
  - Sales distribution by category
  - Stock status predictions

### User Interface
- **Responsive Design**: Built with Bootstrap 5 for mobile and desktop
- **Dashboard**: Overview cards showing key metrics
- **Clean Navigation**: Easy-to-use navbar with icon indicators
- **Real-time Updates**: AJAX-based interactions for smooth user experience

## 🗃️ Database Schema

### Tables

**Products**
- product_id (Primary Key)
- product_name
- category
- price

**Suppliers**
- supplier_id (Primary Key)
- supplier_name
- contact_info

**Inventory**
- inventory_id (Primary Key)
- product_id (Foreign Key)
- stock_quantity
- restock_date

**Sales**
- sale_id (Primary Key)
- product_id (Foreign Key)
- quantity_sold
- sale_date

**Purchases**
- purchase_id (Primary Key)
- product_id (Foreign Key)
- supplier_id (Foreign Key)
- quantity_purchased
- purchase_date

## 📦 Tech Stack

- **Backend**: Python 3.9+ with Flask
- **Database**: SQLite (can be easily changed to MySQL)
- **ORM**: SQLAlchemy
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **AI/ML**: scikit-learn (Linear Regression), pandas, numpy
- **Charts**: Chart.js

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Step 1: Clone or Download
```bash
cd C:\Users\Atharva\Documents
# (Project is already in inventory_system folder)
```

### Step 2: Install Dependencies
```bash
cd inventory_system
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

The application will automatically:
- Create the SQLite database (`inventory.db`)
- Initialize tables with sample data
- Start the Flask development server

## 📁 Project Structure

```
inventory_system/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── inventory.db               # SQLite database (auto-generated)
├── models/
│   └── database.py            # Database models and initialization
├── ai/
│   └── predictor.py           # AI prediction module
├── templates/
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Dashboard home page
│   ├── products.html          # Products management
│   ├── suppliers.html         # Suppliers management
│   ├── inventory.html         # Inventory tracking
│   ├── sales.html             # Sales recording
│   └── ai_insights.html       # AI predictions and charts
└── static/
    ├── css/
    │   └── style.css          # Custom styling
    └── js/
        └── main.js            # JavaScript utilities
```

## 🎯 Usage Guide

### Dashboard (Home)
- View summary cards: Total Products, Total Sales, Low Stock Count, Suppliers
- See recent sales and low stock alerts

### Products Page
- Click "Add New Product" to create a product
- Edit or delete existing products
- Products automatically get inventory entries

### Suppliers Page
- Manage supplier information
- Add, edit, or delete suppliers

### Inventory Page
- View current stock levels with color-coded status:
  - 🔴 Red: Critical (< 10 units)
  - 🟡 Yellow: Low (< 20 units)
  - 🟢 Green: Healthy (≥ 20 units)
- Update stock quantities and restock dates

### Sales Page
- Record new sales transactions
- Inventory automatically decrements
- Delete sales to restore inventory

### AI Insights Page
- Click "Run AI Prediction" to analyze stock levels
- View predictions table showing:
  - Current stock
  - Predicted daily sales
  - Days until stockout
  - Confidence level
- Interactive charts:
  - Sales trend over time
  - Category sales distribution

## 🤖 AI Prediction Model

The system uses **Linear Regression** from scikit-learn to:

1. **Analyze Historical Data**: Reviews past sales for each product
2. **Predict Future Sales**: Forecasts expected daily sales
3. **Calculate Days to Stockout**: Determines when products will run out
4. **Prioritize Alerts**: Highlights critical and warning items

### Prediction Status
- ⚠️ **Critical**: Stock will run out in ≤ 3 days
- ⚠️ **Warning**: Stock will run out in ≤ 7 days
- ⚠️ **Low Stock**: Current stock < 10 units
- ✅ **Healthy**: Sufficient stock available

### Confidence Levels
- **High**: Based on 5+ sales records
- **Medium**: Based on 3-4 sales records
- **Low**: Based on < 3 sales records

## 🔧 Configuration

### Change Database (Optional)
To use MySQL instead of SQLite, update `app.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/inventory_db'
```

### Adjust Port
Change the port in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Sample Data
The system initializes with sample data on first run. To reset:
1. Delete `inventory.db`
2. Restart the application

## 🛠️ API Endpoints

### Products
- `GET /api/products` - Get all products
- `POST /api/products` - Create product
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product

### Suppliers
- `GET /api/suppliers` - Get all suppliers
- `POST /api/suppliers` - Create supplier
- `PUT /api/suppliers/<id>` - Update supplier
- `DELETE /api/suppliers/<id>` - Delete supplier

### Inventory
- `GET /api/inventory` - Get all inventory
- `PUT /api/inventory/<id>` - Update inventory

### Sales
- `GET /api/sales` - Get all sales
- `POST /api/sales` - Create sale (auto-updates inventory)
- `DELETE /api/sales/<id>` - Delete sale (restores inventory)

### AI & Analytics
- `GET /api/predict` - Run AI stock prediction
- `GET /api/sales-trend` - Get sales trend data
- `GET /api/category-sales` - Get category distribution

## 📊 Sample Data Included

The system comes with pre-loaded sample data:
- 8 Products (Electronics, Furniture, Stationery)
- 3 Suppliers
- Inventory records for all products
- Historical sales data for AI training
- Sample purchase records

## 🐛 Troubleshooting

### Issue: Module not found
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Database locked
**Solution**: Close any other applications accessing `inventory.db` and restart

### Issue: Port already in use
**Solution**: Change the port in `app.py` or kill the process using port 5000

### Issue: AI predictions not showing
**Solution**: Ensure you have enough sales data (at least 2 sales per product)

## 🎨 Customization

### Colors and Styling
Edit `static/css/style.css` to customize:
- Color schemes
- Card styles
- Typography
- Animations

### Add More Features
The codebase is modular and easy to extend:
- Add new database models in `models/database.py`
- Create new routes in `app.py`
- Add pages by creating templates
- Enhance AI models in `ai/predictor.py`

## 📝 License

This project is created for educational purposes. Feel free to use and modify as needed.

## 👨‍💻 Developer Notes

- The application uses Flask's development server - not suitable for production
- For production deployment, use Gunicorn or similar WSGI server
- Consider implementing user authentication for multi-user environments
- Add input validation and sanitization for production use
- Implement proper error logging and monitoring

## 🎓 Learning Resources

This project demonstrates:
- Flask web framework
- SQLAlchemy ORM
- RESTful API design
- Bootstrap frontend framework
- Machine Learning integration
- Data visualization with Chart.js

## 📧 Support

For issues or questions, check the code comments or review the Flask and scikit-learn documentation.

---

**Happy Inventory Managing! 🚀**
