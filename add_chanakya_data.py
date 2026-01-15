"""
Script to populate database with real data from Chanakya University
"""
from app import create_app
from models import db, Department, Event
from datetime import datetime, timedelta

app = create_app('development')

with app.app_context():
    print("Adding Chanakya University data to database...")
    
    # Clear existing data
    print("\nClearing existing departments and events...")
    Department.query.delete()
    Event.query.delete()
    db.session.commit()
    
    # Add Departments from Chanakya University
    print("\nAdding departments...")
    departments_data = [
        {
            'name': 'School of Arts, Humanities and Social Sciences',
            'head': 'Dr. Rajesh Kumar',
            'email': 'arts@chanakyauniversity.edu.in',
            'phone': '+91-8688-555-555'
        },
        {
            'name': 'School of Management Sciences',
            'head': 'Dr. Priya Sharma',
            'email': 'management@chanakyauniversity.edu.in',
            'phone': '+91-8688-555-556'
        },
        {
            'name': 'School of Mathematics and Natural Sciences',
            'head': 'Dr. Anand Reddy',
            'email': 'sciences@chanakyauniversity.edu.in',
            'phone': '+91-8688-555-557'
        },
        {
            'name': 'School of Law, Governance and Public Policy',
            'head': 'Dr. Meera Patel',
            'email': 'law@chanakyauniversity.edu.in',
            'phone': '+91-8688-555-558'
        },
        {
            'name': 'School of Biosciences',
            'head': 'Dr. Suresh Rao',
            'email': 'biosciences@chanakyauniversity.edu.in',
            'phone': '+91-8688-555-559'
        },
        {
            'name': 'School of Engineering',
            'head': 'Dr. Vikram Singh',
            'email': 'engineering@chanakyauniversity.edu.in',
            'phone': '+91-8688-555-560'
        }
    ]
    
    for dept_data in departments_data:
        dept = Department(
            name=dept_data['name'],
            head_of_department=dept_data['head'],
            contact_email=dept_data['email'],
            contact_phone=dept_data['phone']
        )
        db.session.add(dept)
        print(f"  Added: {dept_data['name']}")
    
    db.session.commit()
    print(f"\nTotal departments added: {len(departments_data)}")
    
    # Add Events from Chanakya University
    print("\nAdding events...")
    base_date = datetime.now()
    
    events_data = [
        {
            'title': 'Online Certificate Course on Indian Intellectual Heritage',
            'description': 'A comprehensive online course exploring India\'s rich intellectual heritage, covering philosophy, science, mathematics, and cultural traditions.',
            'location': 'Online Platform',
            'days_from_now': 5
        },
        {
            'title': 'Workshop on Everyday Science: Where Curiosity Meets Reality',
            'description': 'An interactive workshop for PUC students exploring the science behind everyday phenomena, making learning fun and practical.',
            'location': 'Science Block, Chanakya University',
            'days_from_now': 10
        },
        {
            'title': 'Roundtable on Concept and Predicate Commonality Across Indian Languages',
            'description': 'Academic discussion on linguistic patterns and commonalities across various Indian languages, featuring renowned linguists.',
            'location': 'Conference Hall, Main Building',
            'days_from_now': 15
        },
        {
            'title': '11th Sammilan - A Celebration of Community and Excellence',
            'description': 'Annual gathering celebrating achievements, fostering community spirit, and recognizing excellence in academics, sports, and cultural activities.',
            'location': 'University Auditorium',
            'days_from_now': 20
        },
        {
            'title': 'Understanding India\'s New Criminal Laws',
            'description': 'Expert panel discussion on the recent changes in India\'s criminal justice system, their implications, and implementation challenges.',
            'location': 'Law School Auditorium',
            'days_from_now': 25
        },
        {
            'title': 'Research Symposium on Sustainability',
            'description': 'Annual research symposium featuring presentations on environmental sustainability, renewable energy, and climate change mitigation.',
            'location': 'Research Center',
            'days_from_now': 30
        },
        {
            'title': 'Entrepreneurship Summit 2025',
            'description': 'Three-day summit featuring successful entrepreneurs, startup pitches, workshops on business planning, and networking opportunities.',
            'location': 'Management School',
            'days_from_now': 35
        },
        {
            'title': 'Cultural Fest - Expressions 2025',
            'description': 'Annual cultural festival showcasing student talents in music, dance, drama, art, and literature from diverse cultural backgrounds.',
            'location': 'Open Air Theatre',
            'days_from_now': 40
        },
        {
            'title': 'International Conference on Artificial Intelligence',
            'description': 'Two-day international conference on AI and Machine Learning, featuring keynote speakers, research presentations, and industry panels.',
            'location': 'Engineering Block',
            'days_from_now': 45
        },
        {
            'title': 'Sports Meet 2025',
            'description': 'Inter-school sports competition featuring athletics, cricket, football, basketball, badminton, and other sports.',
            'location': 'Sports Complex',
            'days_from_now': 50
        }
    ]
    
    for event_data in events_data:
        event = Event(
            title=event_data['title'],
            description=event_data['description'],
            event_date=base_date + timedelta(days=event_data['days_from_now']),
            location=event_data['location'],
            created_by=1  # Admin user ID
        )
        db.session.add(event)
        print(f"  Added: {event_data['title']}")
    
    db.session.commit()
    print(f"\nTotal events added: {len(events_data)}")
    
    print("\n" + "="*60)
    print("Database populated successfully with Chanakya University data!")
    print("="*60)
    print("\nYou can now:")
    print("1. View departments in the chatbot")
    print("2. View upcoming events in the chatbot")
    print("3. Ask questions like:")
    print("   - 'What events are coming up?'")
    print("   - 'Tell me about the departments'")
    print("   - 'Who is the head of Engineering?'")
