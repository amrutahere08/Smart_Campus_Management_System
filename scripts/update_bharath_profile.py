"""
Update Dr. Bharath Setturu's complete faculty profile
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, Department
from werkzeug.security import generate_password_hash
import shutil

def update_bharath_profile():
    """Update Dr. Bharath Setturu's complete profile"""
    app = create_app()
    
    with app.app_context():
        print("Updating Dr. Bharath Setturu's profile...")
        
        # Find the user
        user = User.query.filter_by(username='bharath_setturu').first()
        
        if not user:
            print("❌ User 'bharath_setturu' not found")
            # Try to find by email
            user = User.query.filter_by(email='bharaths@chanakyauniversity.edu.in').first()
            if not user:
                print("❌ User not found by email either")
                return
        
        print(f"✓ Found user: {user.full_name}")
        
        # Get Engineering department
        engineering_dept = Department.query.filter_by(name='School of Engineering').first()
        if not engineering_dept:
            print("Creating School of Engineering department...")
            engineering_dept = Department(name='School of Engineering')
            db.session.add(engineering_dept)
            db.session.flush()
        
        # Update user details
        user.full_name = 'Dr. Bharath Setturu'
        user.email = 'bharaths@chanakyauniversity.edu.in'
        user.role = 'Faculty'
        user.department_id = engineering_dept.id
        user.designation = 'Associate Professor, School of Engineering'
        user.education = 'Ph.D., IIIT Hyderabad; Post-doctoral Fellow, IISc Bangalore'
        
        # Update bio with comprehensive information
        user.bio = """Dr. Bharath Setturu is an Associate Professor of Computer Science at the School of Engineering, Chanakya University, Bengaluru, leading BCA and MCA programs since August 2023. He was a post-doctoral fellow at IISc Bangalore and serves as guest faculty at IIT Jodhpur. He has authored 2 books, 48 international journal papers, and 75+ technical reports, contributing to 15+ research projects in GIS, Remote Sensing, and ecological studies. His work, recognized with multiple awards, supports evidence-based environmental decision-making and employs advanced geospatial and data-driven techniques."""
        
        # Update research interests
        user.research_interests = 'GIS, Remote Sensing, Geospatial Science, Ecological Studies, Environmental Decision-Making, Data-Driven Techniques'
        
        # Copy profile image
        source_image = '/Users/abhi/.gemini/antigravity/brain/80556d4d-5d86-446d-b60b-ccbb99a00388/uploaded_image_1766566598764.jpg'
        if os.path.exists(source_image):
            # Create faculty images directory
            faculty_dir = 'static/images/faculty'
            os.makedirs(faculty_dir, exist_ok=True)
            
            # Copy image
            dest_image = os.path.join(faculty_dir, 'bharath_setturu.jpg')
            shutil.copy(source_image, dest_image)
            user.profile_image = f'/static/images/faculty/bharath_setturu.jpg'
            user.profile_picture = f'/static/images/faculty/bharath_setturu.jpg'
            print(f"✓ Profile image copied to {dest_image}")
        else:
            print(f"⚠ Source image not found: {source_image}")
        
        # Commit changes
        db.session.commit()
        
        print("\n✅ Profile updated successfully!")
        print(f"Name: {user.full_name}")
        print(f"Email: {user.email}")
        print(f"Department: {user.department.name}")
        print(f"Designation: {user.designation}")
        print(f"Education: {user.education}")
        print(f"Profile Image: {user.profile_image}")
        print(f"\nBio: {user.bio[:100]}...")
        print(f"Research: {user.research_interests}")

if __name__ == '__main__':
    update_bharath_profile()
