#!/usr/bin/env python3

try:
    from app import create_app
    print("✓ Import successful")

    app = create_app()
    print("✓ App created successfully")

    with app.app_context():
        from app.models import User
        print("✓ Models imported successfully")

        # Test database
        app.db.create_all()
        print("✓ Database tables created")

    print("🎉 All tests passed! The app should work.")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()