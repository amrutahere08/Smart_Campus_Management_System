"""
Database initialization script for Smart Campus System
Creates all tables and seeds initial data
"""

from app import create_app
from models import db, User, Department
from services.chatbot import chatbot
import os

def init_database():
 """Initialize database with tables and seed data"""
 app = create_app('development')
 
 with app.app_context():
 # Drop all tables and recreate (for fresh start)
 print("Creating database tables...")
 db.drop_all()
 db.create_all()
 print(" Tables created successfully!")
 
 # Create departments
 print("\nCreating departments...")
 departments = [
 Department(
 name="Computer Science",
 head_of_department="Dr. John Smith",
 contact_email="cs@smartcampus.edu",
 contact_phone="+1-555-0101"
 ),
 Department(
 name="Electrical Engineering",
 head_of_department="Dr. Sarah Johnson",
 contact_email="ee@smartcampus.edu",
 contact_phone="+1-555-0102"
 ),
 Department(
 name="Business Administration",
 head_of_department="Dr. Michael Brown",
 contact_email="ba@smartcampus.edu",
 contact_phone="+1-555-0103"
 ),
 Department(
 name="Mathematics",
 head_of_department="Dr. Emily Davis",
 contact_email="math@smartcampus.edu",
 contact_phone="+1-555-0104"
 )
 ]
 
 for dept in departments:
 db.session.add(dept)
 
 db.session.commit()
 print(f" Created {len(departments)} departments")
 
 # Create admin user
 print("\nCreating admin user...")
 admin = User(
 username="admin",
 email="chanakyasmartcampus@gmail.com",
 full_name="System Administrator",
 role="Admin",
 is_approved=True,
 is_active=True
 )
 admin.set_password("Admin@Chanakya25")
 
 db.session.add(admin)
 db.session.commit()
 print(" Admin user created")
 print(" Username: admin")
 print(" Email: chanakyasmartcampus@gmail.com")
 print(" Password: Admin@Chanakya25")
 
 # Create sample student
 print("\nCreating sample student...")
 cs_dept = Department.query.filter_by(name="Computer Science").first()
 student = User(
 username="student1",
 email="student1@smartcampus.edu",
 full_name="John Doe",
 role="Student",
 department_id=cs_dept.id,
 is_approved=True,
 is_active=True
 )
 student.set_password("Student@123")
 
 db.session.add(student)
 db.session.commit()
 print(" Sample student created")
 print(" Username: student1")
 print(" Password: Student@123")
 
 # Create sample faculty
 print("\nCreating sample faculty...")
 faculty = User(
 username="faculty1",
 email="faculty1@smartcampus.edu",
 full_name="Dr. Jane Smith",
 role="Faculty",
 department_id=cs_dept.id,
 is_approved=True,
 is_active=True
 )
 faculty.set_password("Faculty@123")
 
 db.session.add(faculty)
 db.session.commit()
 print(" Sample faculty created")
 print(" Username: faculty1")
 print(" Password: Faculty@123")
 
 # Create security user
 print("\nCreating security user...")
 security = User(
 username="security",
 email="security@smartcampus.edu",
 full_name="Security Admin",
 role="Security",
 is_approved=True,
 is_active=True
 )
 security.set_password("Admin2")
 
 db.session.add(security)
 db.session.commit()
 print(" Security user created")
 print(" Username: security")
 print(" Password: Admin2")
 
 # Initialize chatbot
 print("\nInitializing AI chatbot...")
 api_key = os.environ.get('GOOGLE_API_KEY')
 if api_key:
 chatbot.initialize(api_key)
 print(" Chatbot initialized with Google API key")
 else:
 print(" Warning: GOOGLE_API_KEY not found in environment variables")
 print(" Chatbot will not work until you set the API key in .env file")
 
 print("\n" + "="*60)
 print(" Database initialization complete!")
 print("="*60)
 print("\nYou can now run the application with: python app.py")
  print("\nDefault login credentials:")
  print(" Admin - username: admin, email: chanakyasmartcampus@gmail.com, password: Admin@Chanakya25")
  print(" Student - username: student1, password: Student@123")
  print(" Faculty - username: faculty1, password: Faculty@123")
  print(" Security - username: security, password: Admin2")
 print("\nDon't forget to:")
 print(" 1. Copy .env.example to .env")
 print(" 2. Add your GOOGLE_API_KEY to .env")
 print(" 3. Update SECRET_KEY in .env for production")
 print("="*60)


if __name__ == '__main__':
 init_database()
