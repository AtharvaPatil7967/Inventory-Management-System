# Quick Start Guide 🚀

## Installation (3 Simple Steps)

### 1️⃣ Navigate to Project Directory
```powershell
cd C:\Users\Atharva\Documents\inventory_system
```

### 2️⃣ Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3️⃣ Run the Application
```powershell
python app.py
```

## Access the Application

Open your web browser and go to:
```
http://localhost:5000
```

## First-Time Setup

The application will automatically:
- ✅ Create the database (inventory.db)
- ✅ Set up all tables
- ✅ Load sample data (8 products, 3 suppliers, sales history)
- ✅ Start the Flask server

## Navigation Guide

| Page | URL | Description |
|------|-----|-------------|
| **Dashboard** | http://localhost:5000/ | Overview with summary cards |
| **Products** | http://localhost:5000/products | Manage products |
| **Suppliers** | http://localhost:5000/suppliers | Manage suppliers |
| **Inventory** | http://localhost:5000/inventory | View/update stock |
| **Sales** | http://localhost:5000/sales | Record sales |
| **AI Insights** | http://localhost:5000/ai-insights | Predictions & charts |

## Try These Features

### 1. Add a New Product
1. Go to Products page
2. Click "Add New Product"
3. Fill in details
4. Save

### 2. Record a Sale
1. Go to Sales page
2. Click "Record New Sale"
3. Select product and quantity
4. Watch inventory auto-update!

### 3. Run AI Prediction
1. Go to AI Insights page
2. Click "Run AI Prediction"
3. View which products will run out soon
4. Check sales trends and category charts

## Common Commands

```powershell
# Stop the server
Ctrl + C

# Restart the server
python app.py

# Reset database (delete and restart)
del inventory.db
python app.py

# Check if running
# Open browser to http://localhost:5000
```

## Project Structure at a Glance

```
inventory_system/
├── app.py                 ← Main Flask app (START HERE)
├── requirements.txt       ← Dependencies
├── README.md             ← Full documentation
├── models/database.py    ← Database models
├── ai/predictor.py       ← AI prediction logic
├── templates/            ← HTML pages
└── static/               ← CSS & JavaScript
```

## Sample Data Included

- **8 Products**: Laptops, Mice, Keyboards, Monitors, Chairs, Notebooks, Pens, Cables
- **3 Suppliers**: TechSupply Co., Office Depot, FurniturePro
- **10+ Sales**: Historical data for AI training
- **Inventory**: Pre-filled stock levels

## Troubleshooting

**Error: Module not found**
```powershell
pip install -r requirements.txt
```

**Port 5000 already in use**
- Edit app.py, change port to 8080:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

**Database issues**
```powershell
del inventory.db
python app.py
```

## What to Explore

1. ✅ Dashboard - See live statistics
2. ✅ Add/Edit products and suppliers
3. ✅ Record sales and watch inventory decrease
4. ✅ Update stock levels manually
5. ✅ Run AI predictions to see stock forecasts
6. ✅ View beautiful charts and analytics

## Next Steps

- Read full documentation in README.md
- Explore API endpoints for integration
- Customize colors in static/css/style.css
- Add more products and suppliers
- Test the AI prediction with more sales data

---

**Need Help?** Check README.md for detailed documentation.

**Enjoy your Inventory Management System! 📦✨**
