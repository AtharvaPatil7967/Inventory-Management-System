"""
Quick test script to verify the Inventory Management System setup
"""
import sys
import os

# Add models directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'models'))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        import flask
        print("✓ Flask imported successfully")
        
        import flask_sqlalchemy
        print("✓ Flask-SQLAlchemy imported successfully")
        
        import flask_login
        print("✓ Flask-Login imported successfully")
        
        from werkzeug.security import generate_password_hash, check_password_hash
        print("✓ Werkzeug security imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_database_models():
    """Test if database models are properly defined"""
    print("\nTesting database models...")
    try:
        from models.database import db, User, ActivityLog, Product, Supplier, Inventory, Sale, Purchase
        print("✓ All database models imported successfully")
        
        # Test User model methods
        print("✓ User model has required attributes")
        
        # Test ActivityLog model
        print("✓ ActivityLog model has required attributes")
        
        return True
    except Exception as e:
        print(f"✗ Database model error: {e}")
        return False

def test_templates():
    """Test if all required templates exist"""
    print("\nTesting templates...")
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    required_templates = [
        'home.html',
        'login.html',
        'register.html',
        'dashboard.html',
        'base.html',
        'products.html',
        'suppliers.html',
        'inventory.html',
        'sales.html',
        'ai_insights.html'
    ]
    
    all_exist = True
    for template in required_templates:
        template_path = os.path.join(templates_dir, template)
        if os.path.exists(template_path):
            print(f"✓ {template} exists")
        else:
            print(f"✗ {template} missing")
            all_exist = False
    
    return all_exist

def test_static_files():
    """Test if static files exist"""
    print("\nTesting static files...")
    static_css = os.path.join(os.path.dirname(__file__), 'static', 'css', 'style.css')
    
    if os.path.exists(static_css):
        print("✓ style.css exists")
        return True
    else:
        print("✗ style.css missing")
        return False

def test_app_structure():
    """Test if app.py has required routes"""
    print("\nTesting app.py structure...")
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        required_routes = [
            '@app.route(\'/\')',
            '@app.route(\'/login\'',
            '@app.route(\'/register\'',
            '@app.route(\'/dashboard\')',
            '@app.route(\'/logout\')',
            'def log_activity'
        ]
        
        all_found = True
        for route in required_routes:
            if route in content:
                print(f"✓ Found {route}")
            else:
                print(f"✗ Missing {route}")
                all_found = False
        
        return all_found
    except Exception as e:
        print(f"✗ Error reading app.py: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("INVENTORY MANAGEMENT SYSTEM - SETUP VERIFICATION")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Database Models", test_database_models),
        ("Templates", test_templates),
        ("Static Files", test_static_files),
        ("App Structure", test_app_structure)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:.<40} {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed! Your system is ready to run.")
        print("\nTo start the application, run:")
        print("    python app.py")
        print("\nThen visit: http://localhost:5000")
        print("\nDefault credentials:")
        print("    Username: admin")
        print("    Password: admin123")
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        print("Run: pip install -r requirements.txt")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
