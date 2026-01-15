"""
Update department names and add all Chanakya programs
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, Program, Department

app = create_app('development')

def update_departments_and_programs():
    """Update department names and add all programs"""
    with app.app_context():
        print("Updating departments and adding programs...")
        
        # First, let's see what departments exist
        existing_depts = Department.query.all()
        print("\nExisting departments:")
        for dept in existing_depts:
            print(f"  - {dept.name}")
        
        # Update department names to match Chanakya University
        dept_updates = {
            'School of Engineering': 'School of Engineering',
            'School of Management Sciences': 'School of Management Sciences',
            'School of Mathematics and Natural Sciences': 'School of Mathematics and Natural Sciences',
            'School of Arts, Humanities and Social Sciences': 'School of Arts, Humanities and Social Sciences',
        }
        
        # Create missing departments
        required_depts = [
            'School of Engineering',
            'School of Management Sciences',
            'School of Mathematics and Natural Sciences',
            'School of Arts, Humanities and Social Sciences',
            'School of Public Policy and Legal Studies',
            'School of Bioscience',
        ]
        
        for dept_name in required_depts:
            if not Department.query.filter_by(name=dept_name).first():
                dept = Department(
                    name=dept_name,
                    head_of_department='TBD',
                    contact_email=f"{dept_name.lower().replace(' ', '').replace(',', '')}@chanakyauniversity.edu.in"
                )
                db.session.add(dept)
                print(f"  ✓ Created: {dept_name}")
        
        db.session.commit()
        
        # Now add all programs
        programs_data = {
            'School of Engineering': [
                # UG Programs
                {'name': 'B.Tech Computer Science and Engineering', 'code': 'BTECH-CSE', 'duration': 4},
                {'name': 'B.Tech Electronics and Communication Engineering', 'code': 'BTECH-ECE', 'duration': 4},
                {'name': 'B.Tech Mechanical Engineering', 'code': 'BTECH-MECH', 'duration': 4},
                {'name': 'B.Tech Civil Engineering', 'code': 'BTECH-CIVIL', 'duration': 4},
                {'name': 'B.Tech Electrical and Electronics Engineering', 'code': 'BTECH-EEE', 'duration': 4},
                {'name': 'B.Tech Artificial Intelligence and Machine Learning', 'code': 'BTECH-AIML', 'duration': 4},
                {'name': 'B.Tech Data Science', 'code': 'BTECH-DS', 'duration': 4},
                # PG Programs
                {'name': 'M.Tech Computer Science and Engineering', 'code': 'MTECH-CSE', 'duration': 2},
                {'name': 'M.Tech VLSI Design', 'code': 'MTECH-VLSI', 'duration': 2},
                {'name': 'M.Tech Structural Engineering', 'code': 'MTECH-SE', 'duration': 2},
                # Doctoral
                {'name': 'Ph.D. Engineering', 'code': 'PHD-ENG', 'duration': 4},
            ],
            'School of Management Sciences': [
                # UG Programs
                {'name': 'BBA General Management', 'code': 'BBA-GM', 'duration': 3},
                {'name': 'BBA Finance', 'code': 'BBA-FIN', 'duration': 3},
                {'name': 'BBA Marketing', 'code': 'BBA-MKT', 'duration': 3},
                # PG Programs
                {'name': 'MBA General Management', 'code': 'MBA-GM', 'duration': 2},
                {'name': 'MBA Finance', 'code': 'MBA-FIN', 'duration': 2},
                {'name': 'MBA Marketing', 'code': 'MBA-MKT', 'duration': 2},
                {'name': 'MBA Human Resources', 'code': 'MBA-HR', 'duration': 2},
                {'name': 'MBA Business Analytics', 'code': 'MBA-BA', 'duration': 2},
                {'name': 'MBA International Business', 'code': 'MBA-IB', 'duration': 2},
                # Doctoral
                {'name': 'Ph.D. Management', 'code': 'PHD-MGT', 'duration': 4},
            ],
            'School of Mathematics and Natural Sciences': [
                # UG Programs
                {'name': 'B.Sc Physics', 'code': 'BSC-PHY', 'duration': 3},
                {'name': 'B.Sc Chemistry', 'code': 'BSC-CHEM', 'duration': 3},
                {'name': 'B.Sc Mathematics', 'code': 'BSC-MATH', 'duration': 3},
                {'name': 'B.Sc Statistics', 'code': 'BSC-STAT', 'duration': 3},
                {'name': 'B.Sc Environmental Science', 'code': 'BSC-ENV', 'duration': 3},
                # PG Programs
                {'name': 'M.Sc Physics', 'code': 'MSC-PHY', 'duration': 2},
                {'name': 'M.Sc Chemistry', 'code': 'MSC-CHEM', 'duration': 2},
                {'name': 'M.Sc Mathematics', 'code': 'MSC-MATH', 'duration': 2},
                {'name': 'M.Sc Data Science', 'code': 'MSC-DS', 'duration': 2},
                # Doctoral
                {'name': 'Ph.D. Sciences', 'code': 'PHD-SCI', 'duration': 4},
            ],
            'School of Arts, Humanities and Social Sciences': [
                # UG Programs
                {'name': 'BA English Literature', 'code': 'BA-ENG', 'duration': 3},
                {'name': 'BA History', 'code': 'BA-HIST', 'duration': 3},
                {'name': 'BA Political Science', 'code': 'BA-POL', 'duration': 3},
                {'name': 'BA Psychology', 'code': 'BA-PSY', 'duration': 3},
                {'name': 'BA Sociology', 'code': 'BA-SOC', 'duration': 3},
                {'name': 'BA Economics', 'code': 'BA-ECO', 'duration': 3},
                # PG Programs
                {'name': 'MA English Literature', 'code': 'MA-ENG', 'duration': 2},
                {'name': 'MA History', 'code': 'MA-HIST', 'duration': 2},
                {'name': 'MA Political Science', 'code': 'MA-POL', 'duration': 2},
                {'name': 'MA Psychology', 'code': 'MA-PSY', 'duration': 2},
                # Doctoral
                {'name': 'Ph.D. Arts and Humanities', 'code': 'PHD-ARTS', 'duration': 4},
            ],
            'School of Public Policy and Legal Studies': [
                # UG Programs
                {'name': 'BA Public Policy', 'code': 'BA-PP', 'duration': 3},
                {'name': 'BA Legal Studies', 'code': 'BA-LAW', 'duration': 3},
                # PG Programs
                {'name': 'MA Public Policy', 'code': 'MA-PP', 'duration': 2},
                {'name': 'MA International Relations', 'code': 'MA-IR', 'duration': 2},
                {'name': 'Master of Public Administration', 'code': 'MPA', 'duration': 2},
                # Doctoral
                {'name': 'Ph.D. Public Policy', 'code': 'PHD-PP', 'duration': 4},
            ],
            'School of Bioscience': [
                # UG Programs
                {'name': 'B.Sc Biotechnology', 'code': 'BSC-BIOTECH', 'duration': 3},
                {'name': 'B.Sc Microbiology', 'code': 'BSC-MICRO', 'duration': 3},
                {'name': 'B.Sc Biochemistry', 'code': 'BSC-BIOCHEM', 'duration': 3},
                # PG Programs
                {'name': 'M.Sc Biotechnology', 'code': 'MSC-BIOTECH', 'duration': 2},
                {'name': 'M.Sc Microbiology', 'code': 'MSC-MICRO', 'duration': 2},
                {'name': 'M.Sc Molecular Biology', 'code': 'MSC-MOLBIO', 'duration': 2},
                # Doctoral
                {'name': 'Ph.D. Bioscience', 'code': 'PHD-BIO', 'duration': 4},
            ],
        }
        
        added_count = 0
        skipped_count = 0
        
        print("\nAdding programs:")
        for dept_name, programs in programs_data.items():
            dept = Department.query.filter_by(name=dept_name).first()
            if not dept:
                print(f"Warning: Department '{dept_name}' not found, skipping...")
                continue
            
            print(f"\n{dept_name}:")
            for prog_data in programs:
                existing = Program.query.filter_by(code=prog_data['code']).first()
                if not existing:
                    program = Program(
                        name=prog_data['name'],
                        code=prog_data['code'],
                        department_id=dept.id,
                        duration_years=prog_data['duration']
                    )
                    db.session.add(program)
                    print(f"  ✓ Added: {prog_data['name']}")
                    added_count += 1
                else:
                    print(f"  - Skipped: {prog_data['name']}")
                    skipped_count += 1
        
        db.session.commit()
        
        print(f"\n{'='*60}")
        print(f"✓ Migration completed!")
        print(f"  Programs added: {added_count}")
        print(f"  Programs skipped: {skipped_count}")
        print(f"  Total programs in database: {Program.query.count()}")
        print(f"  Total departments: {Department.query.count()}")
        print(f"{'='*60}")


if __name__ == "__main__":
    update_departments_and_programs()
