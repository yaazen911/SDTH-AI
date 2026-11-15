from app import app
from models import db, User, Truck

with app.app_context():
    # إضافة سائق تجريبي
    driver = User(username="ahmed", password="1234", role="driver")
    
    # إضافة إدمن تجريبي
    admin = User(username="admin", password="admin123", role="admin")
    
    # إضافة شاحنة تجريبية
    truck = Truck(plate_number="ABC-123", qr_code="TRUCK001")

    db.session.add(driver)
    db.session.add(admin)
    db.session.add(truck)
    db.session.commit()

    print("تمت إضافة البيانات التجريبية بنجاح!")