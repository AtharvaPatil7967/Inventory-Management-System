# 🎯 Inventory Management System - Complete Setup Guide

## 📋 Overview

A full-stack **AI-powered Inventory Management System** with:
- ✅ User Authentication & Authorization
- ✅ Activity Tracking & Logging
- ✅ Personalized Dashboard
- ✅ AI-Powered Insights
- ✅ Modern UI with Bootstrap 5 & Animations
- ✅ SQLite Database
- ✅ Flask Backend

---

## 🚀 Features Implemented

### 1. **Authentication System**
- 🏠 **Landing Page**: Beautiful home page with animations and project description
- 🔐 **Login System**: Secure login with username/password
- 📝 **Registration**: New user registration with email validation
- 🔒 **Password Security**: Werkzeug password hashing
- 👤 **User Sessions**: Flask-Login for session management
- 🚪 **Logout**: Clean logout with activity logging

### 2. **User Management**
- 👥 **User Model**: user_id, username, email, password_hash, join_date, is_admin
- 🗄️ **Database Storage**: SQLite with SQLAlchemy ORM
- 🛡️ **Protected Routes**: Login required for all CRUD operations
- 👑 **Admin Support**: Admin flag for elevated privileges

### 3. **Activity Tracking**
- 📊 **ActivityLog Table**: Tracks all user actions
  - log_id, user_id, action_type, affected_table, affected_id, description, timestamp
- 🔍 **Tracked Actions**:
  - ➕ Add Product/Supplier
  - ✏️ Edit Product/Supplier/Inventory
  - 🗑️ Delete Product/Supplier/Sale
  - 💰 Record Sale/Purchase
  - 🔐 Login/Logout
- 📈 **Dashboard Integration**: Recent activities shown on user dashboard
- 👀 **Admin View**: Admins can view all user activities

### 4. **Personalized Dashboard**
- 👋 **Welcome Banner**: Personalized greeting with user stats
- 📊 **Summary Cards**: Total products, sales, low stock alerts, suppliers
- 🕐 **Recent Activity**: User's last 10 actions with icons
- 📉 **Recent Sales**: Last 5 sales transactions
- ⚠️ **Low Stock Alerts**: Products with quantity < 20
- ⚡ **Quick Actions**: Fast navigation to key features
- 📱 **Responsive Design**: Mobile-friendly layout

### 5. **Beautiful Frontend**
- 🎨 **Landing Page**: Gradient backgrounds, floating animations, feature cards
- 💅 **Login/Register**: Modern card design with animations
- 🌈 **Dashboard**: Animated stat cards with gradients
- 🎯 **Navigation**: Conditional navbar (logged in vs logged out)
- 🎭 **User Dropdown**: Shows username and admin badge
- ✨ **Animations**: Fade-in, slide-in, hover effects

### 6. **AI Features** (Already Implemented)
- 🤖 **Low Stock Prediction**: Machine learning predictions
- 📈 **Sales Trends**: Historical analysis
- 📊 **Category Analysis**: Sales by category
- 🔮 **Insights Dashboard**: Visual AI predictions

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip

### Step 1: Clone/Navigate to Project
```bash
cd C:\Users\Atharva\Documents\inventory_system
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

The app will start on `http://localhost:5000` or `http://0.0.0.0:5000`

---

## 🔑 Default Credentials

**Admin Account** (created automatically):
- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Important**: Change the default password after first login in production!

---

## 🗂️ Project Structure

```
inventory_system/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── SETUP_GUIDE.md             # This file
├── README.md                   # Original README
├── QUICKSTART.md              # Quick start guide
│
├── models/
│   ├── database.py            # All database models
│   ├── user.py                # User model (imported in database.py)
│   ├── activity_log.py        # ActivityLog model (imported in database.py)
│   └── __init__.py
│
├── ai/
│   ├── predictor.py           # AI/ML prediction functions
│   └── __init__.py
│
├── templates/
│   ├── home.html              # Landing page (NEW!)
│   ├── login.html             # Login page (NEW!)
│   ├── register.html          # Registration page (NEW!)
│   ├── dashboard.html         # User dashboard (NEW!)
│   ├── base.html              # Base template (UPDATED!)
│   ├── products.html          # Products management
│   ├── suppliers.html         # Suppliers management
│   ├── inventory.html         # Inventory management
│   ├── sales.html             # Sales tracking
│   └── ai_insights.html       # AI insights
│
├── static/
│   ├── css/
│   │   └── style.css          # Custom CSS with animations (NEW!)
│   └── js/
│       └── main.js            # Custom JavaScript
│
└── instance/
    └── inventory.db           # SQLite database
```

---

## 🎮 How to Use

### First Time Setup
1. Start the application: `python app.py`
2. Visit `http://localhost:5000`
3. You'll see the beautiful landing page
4. Click **"Get Started"** or **"Sign Up"**

### Creating a New Account
1. Click **"Register"** or **"Sign Up"**
2. Fill in:
   - Username (min 3 characters)
   - Email
   - Password (min 6 characters)
   - Confirm Password
3. Click **"Create Account"**
4. You'll be redirected to login

### Logging In
1. Enter your username and password
2. Click **"Login"**
3. You'll be redirected to your personalized dashboard

### Using the Dashboard
- View summary statistics at the top
- Check your recent activities
- Monitor low stock alerts
- Use quick action buttons to navigate
- View your profile in the top-right dropdown

### Managing Inventory
1. **Products**: Add/edit/delete products
2. **Suppliers**: Manage supplier information
3. **Inventory**: Update stock quantities
4. **Sales**: Record sales (auto-updates inventory)
5. **AI Insights**: View predictions and trends

### Activity Tracking
- Every action you take is logged
- View your recent activities on the dashboard
- Admins can view all user activities via API:
  - `/api/activity-log` - Your activities
  - `/api/activity-log/all` - All activities (admin only)

---

## 🔐 Security Features

1. **Password Hashing**: Werkzeug PBKDF2 SHA256
2. **Session Management**: Flask-Login with secure cookies
3. **Protected Routes**: `@login_required` decorator
4. **CSRF Protection**: Built into Flask forms
5. **Admin Privileges**: Role-based access control

---

## 🎨 UI/UX Features

### Animations
- ✨ Fade-in on page load
- 📤 Slide-in for cards
- 🎭 Hover effects on buttons and cards
- 💫 Floating icons on landing page
- 🔄 Smooth transitions

### Color Scheme
- **Primary**: Purple gradient (#667eea → #764ba2)
- **Success**: Green gradient (#11998e → #38ef7d)
- **Warning**: Pink gradient (#f093fb → #f5576c)
- **Info**: Blue gradient (#4facfe → #00f2fe)

### Responsive Design
- 📱 Mobile-friendly
- 💻 Tablet optimized
- 🖥️ Desktop enhanced

---

## 📊 Database Schema

### Users Table
```sql
- user_id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- join_date (DateTime)
- is_admin (Boolean)
```

### ActivityLog Table
```sql
- log_id (Primary Key)
- user_id (Foreign Key → Users)
- action_type (String)
- affected_table (String)
- affected_id (Integer, nullable)
- description (String, nullable)
- timestamp (DateTime)
```

### Other Tables
- Products
- Suppliers
- Inventory
- Sales
- Purchases

---

## 🔌 API Endpoints

### Authentication
- `GET /` - Landing page
- `GET/POST /login` - Login page
- `GET/POST /register` - Registration page
- `GET /logout` - Logout
- `GET /dashboard` - User dashboard (protected)

### Activity Logs
- `GET /api/activity-log` - Current user's activities (protected)
- `GET /api/activity-log/all` - All activities (admin only)

### Products
- `GET /api/products` - List all products
- `GET /api/products/<id>` - Get single product
- `POST /api/products` - Create product (protected)
- `PUT /api/products/<id>` - Update product (protected)
- `DELETE /api/products/<id>` - Delete product (protected)

### Suppliers
- `GET /api/suppliers` - List all suppliers
- `POST /api/suppliers` - Create supplier (protected)
- `PUT /api/suppliers/<id>` - Update supplier (protected)
- `DELETE /api/suppliers/<id>` - Delete supplier (protected)

### Inventory
- `GET /api/inventory` - List inventory
- `PUT /api/inventory/<id>` - Update stock (protected)

### Sales
- `GET /api/sales` - List sales
- `POST /api/sales` - Record sale (protected)
- `DELETE /api/sales/<id>` - Delete sale (protected)

### Purchases
- `GET /api/purchases` - List purchases
- `POST /api/purchases` - Record purchase (protected)

### AI Features
- `GET /api/predict` - Low stock predictions
- `GET /api/sales-trend` - Sales trend data
- `GET /api/category-sales` - Category sales data

---

## 🐛 Troubleshooting

### Database Issues
```bash
# Delete the database and restart (WARNING: loses all data)
rm instance/inventory.db
python app.py
```

### Port Already in Use
```python
# Edit app.py, change port at the bottom:
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Missing Dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

---

## 🎯 Next Steps / Optional Enhancements

1. **Email Verification**: Add email confirmation on registration
2. **Password Reset**: Forgot password functionality
3. **Two-Factor Authentication**: Extra security layer
4. **User Profiles**: Edit profile, change password
5. **Advanced Analytics**: More AI insights
6. **Export Features**: PDF reports, CSV exports
7. **Real-time Notifications**: WebSocket alerts
8. **Dark Mode**: Theme toggle
9. **Multi-language**: i18n support
10. **Audit Trail**: Detailed change history

---

## 📝 Notes

- The application creates sample data on first run
- Default admin user is created automatically
- All passwords are hashed (never stored in plain text)
- Activity logging is automatic for all CRUD operations
- Sessions are managed by Flask-Login

---

## 🆘 Support

For issues or questions:
1. Check the console output for error messages
2. Review the QUICKSTART.md for basic setup
3. Check requirements.txt for correct package versions

---

## 📄 License

This project is for educational/personal use.

---

**Enjoy your Inventory Management System! 🚀**
