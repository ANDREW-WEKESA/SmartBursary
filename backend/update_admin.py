"""Update admin user with default values for new columns"""
from app.database import SessionLocal
from app.models import User

db = SessionLocal()
try:
    admin = db.query(User).filter_by(email='admin@smartbursary.com').first()
    if admin:
        admin.ward = None
        admin.last_login = None
        admin.login_count = 0
        db.commit()
        print('✅ Admin user updated with default values for new columns')
        print(f'   Email: {admin.email}')
        print(f'   Role: {admin.role}')
        print(f'   Ward: {admin.ward}')
        print(f'   Login count: {admin.login_count}')
    else:
        print('❌ Admin user not found')
finally:
    db.close()
