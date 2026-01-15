"""
Faculty Data Scraper for School of Engineering
Scrapes faculty profiles from Chanakya University website and populates database
"""

import requests
from bs4 import BeautifulSoup
import os
import sys
from urllib.parse import urljoin
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, Department

app = create_app('development')

# Base URL
BASE_URL = "https://chanakyauniversity.edu.in"

# Faculty list from main page
FACULTY_LIST = [
    {"name": "Dr. Rajesh Kumar Prasad", "id": "9478", "designation": "Associate Professor"},
    {"name": "Dr. Bharath Setturu", "id": "3498", "designation": "Associate Professor of Computer Science"},
    {"name": "Sri Naresh Dixit P. S.", "id": "3501", "designation": "Assistant Professor"},
    {"name": "Dr. Vijay V.", "id": "5234", "designation": "Assistant Professor"},
    {"name": "Dr. Ashish Kumar Shukla", "id": "5277", "designation": "Assistant Professor"},
    {"name": "Sri Shreehari H. S.", "id": "6524", "designation": "Assistant Professor"},
    {"name": "Banashankari Hosur", "id": "7714", "designation": "Assistant Professor"},
    {"name": "Banu Priya M.", "id": "8989", "designation": "Assistant Professor of Computer Science"},
    {"name": "Bhagirathi T", "id": "9245", "designation": "Assistant Professor"},
    {"name": "Dr. Abhishek Patel", "id": "11647", "designation": "Assistant Professor"},
    {"name": "Mulla Arshiya", "id": "11645", "designation": "Assistant Professor"},
    {"name": "Dr. Upkar Singh", "id": "11956", "designation": "Assistant Professor"},
    {"name": "Amogh S Raj", "id": "12471", "designation": "Assistant Professor"},
    {"name": "Anupam Sharma", "id": "14683", "designation": "Assistant Professor"},
    {"name": "Rachana K", "id": "14703", "designation": "Assistant professor"},
    {"name": "Sri Pradeep Kumar Gopalakrishnan", "id": "9231", "designation": "Professor of Practice"},
    {"name": "Prof. P. V. Venkitakrishnan", "id": "4154", "designation": "Visiting Faculty"},
    {"name": "Dr. Kowshik Thopalli", "id": "4218", "designation": "Visiting Faculty"},
    {"name": "Dr. Ritesh Jain", "id": "4222", "designation": "Visiting Faculty"},
    {"name": "Sri Shishir Shukla", "id": "4221", "designation": "Visiting Faculty"},
    {"name": "Dr. Siddhartha Visveswara Jayanti", "id": "4219", "designation": "Visiting Faculty"},
    {"name": "Dr. Tanujay Saha", "id": "4220", "designation": "Visiting Faculty"},
    {"name": "Prof. Y. N. Srikant", "id": "5553", "designation": "Visiting Faculty"},
    {"name": "Dr. Sandoche Balakrichenan", "id": "12560", "designation": "Visiting Faculty"},
    {"name": "Dr. Siddarth Rai Mahendra", "id": "12562", "designation": "Visiting Faculty"},
]


def scrape_faculty_profile(faculty_id, faculty_name):
    """Scrape individual faculty profile page"""
    profile_url = f"{BASE_URL}/schools/school-of-engineering/about?id={faculty_id}"
    
    try:
        print(f"Scraping profile: {faculty_name} ({profile_url})")
        response = requests.get(profile_url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract profile data
        profile_data = {
            'name': faculty_name,
            'profile_url': profile_url,
            'image_url': None,
            'education': None,
            'bio': None,
            'research_interests': None
        }
        
        # Try to find profile image
        img_tag = soup.find('img', class_='faculty-image') or soup.find('img', alt=lambda x: x and faculty_name in x)
        if img_tag and img_tag.get('src'):
            profile_data['image_url'] = urljoin(BASE_URL, img_tag['src'])
        
        # Extract education/qualifications
        edu_section = soup.find(text=lambda x: x and ('Education' in x or 'Qualification' in x))
        if edu_section:
            edu_parent = edu_section.find_parent()
            if edu_parent:
                profile_data['education'] = edu_parent.get_text(strip=True)
        
        # Extract bio/about
        bio_section = soup.find(text=lambda x: x and ('About' in x or 'Biography' in x))
        if bio_section:
            bio_parent = bio_section.find_parent()
            if bio_parent:
                profile_data['bio'] = bio_parent.get_text(strip=True)
        
        # Extract research interests
        research_section = soup.find(text=lambda x: x and 'Research' in x)
        if research_section:
            research_parent = research_section.find_parent()
            if research_parent:
                profile_data['research_interests'] = research_parent.get_text(strip=True)
        
        return profile_data
        
    except Exception as e:
        print(f"Error scraping {faculty_name}: {str(e)}")
        return None


def download_faculty_image(image_url, faculty_name):
    """Download and save faculty profile image"""
    if not image_url:
        return None
    
    try:
        # Create safe filename
        safe_name = faculty_name.lower().replace(' ', '_').replace('.', '')
        safe_name = ''.join(c for c in safe_name if c.isalnum() or c == '_')
        filename = f"{safe_name}.jpg"
        filepath = os.path.join('static', 'images', 'faculty', 'engineering', filename)
        
        # Download image
        print(f"Downloading image for {faculty_name}...")
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Save image
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        # Return relative path for database
        return f"/static/images/faculty/engineering/{filename}"
        
    except Exception as e:
        print(f"Error downloading image for {faculty_name}: {str(e)}")
        return None


def create_faculty_user(faculty_data, designation, department):
    """Create or update faculty user in database"""
    try:
        # Generate email and username
        name_parts = faculty_data['name'].replace('Dr. ', '').replace('Sri ', '').replace('Prof. ', '').strip().split()
        username = '_'.join(name_parts).lower()
        email = f"{username}@chanakyauniversity.edu.in"
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Create new user
            user = User(
                username=username,
                email=email,
                full_name=faculty_data['name'],
                role='Faculty',
                department_id=department.id if department else None,
                is_approved=True,
                is_active=True
            )
            # Set a default password
            user.set_password('faculty123')  # Should be changed on first login
            db.session.add(user)
            print(f"Created new user: {faculty_data['name']}")
        else:
            print(f"Updating existing user: {faculty_data['name']}")
        
        # Update faculty-specific fields
        user.designation = designation
        user.education = faculty_data.get('education')
        user.bio = faculty_data.get('bio')
        user.research_interests = faculty_data.get('research_interests')
        user.university_profile_url = faculty_data.get('profile_url')
        
        # Download and set profile image
        if faculty_data.get('image_url'):
            image_path = download_faculty_image(faculty_data['image_url'], faculty_data['name'])
            if image_path:
                user.profile_image = image_path
        
        db.session.commit()
        print(f"✓ Successfully saved: {faculty_data['name']}")
        return user
        
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error creating user {faculty_data['name']}: {str(e)}")
        return None


def populate_engineering_faculty():
    """Main function to populate all engineering faculty"""
    with app.app_context():
        print("=" * 60)
        print("Starting Faculty Data Scraping for School of Engineering")
        print("=" * 60)
        
        # Get or create Engineering department
        department = Department.query.filter(Department.name.like('%Engineering%')).first()
        if not department:
            department = Department(
                name="School of Engineering",
                contact_email="engineering@chanakyauniversity.edu.in"
            )
            db.session.add(department)
            db.session.commit()
            print(f"Created department: {department.name}")
        else:
            print(f"Using existing department: {department.name}")
        
        print(f"\nProcessing {len(FACULTY_LIST)} faculty members...")
        print("-" * 60)
        
        success_count = 0
        failed_count = 0
        
        for faculty in FACULTY_LIST:
            print(f"\n[{success_count + failed_count + 1}/{len(FACULTY_LIST)}] Processing: {faculty['name']}")
            
            # Scrape profile
            profile_data = scrape_faculty_profile(faculty['id'], faculty['name'])
            
            if profile_data:
                # Create/update user
                user = create_faculty_user(profile_data, faculty['designation'], department)
                if user:
                    success_count += 1
                else:
                    failed_count += 1
            else:
                failed_count += 1
            
            # Be nice to the server
            time.sleep(1)
        
        print("\n" + "=" * 60)
        print("Faculty Data Scraping Complete!")
        print("=" * 60)
        print(f"✓ Successfully processed: {success_count}")
        print(f"✗ Failed: {failed_count}")
        print(f"Total: {len(FACULTY_LIST)}")
        print("=" * 60)


if __name__ == "__main__":
    populate_engineering_faculty()
