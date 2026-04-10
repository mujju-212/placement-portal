from app import app
from models import db, User

with app.app_context():
    db.create_all()

    # Check if admin already exists
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin_user = User(
            username='admin',
            email='admin@placement.com',
            password='admin123',  
            role='admin',
            is_active=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin created successfully!")
        print("Username: admin")
        print("Password: admin123")
    else:
        print("Admin already exists!")

    print("Database tables created successfully!")
