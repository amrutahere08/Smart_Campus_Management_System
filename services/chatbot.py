import google.generativeai as genai
from flask import current_app
from models import db, Event, Department, User, ChatHistory
from models.student_tracking import StudentTracking
from datetime import datetime, timedelta
import pytz


# Faculty and Staff Location Database
FACULTY_LOCATIONS = {
    # Academic Block 1 - 4th Floor
    'shrinivas s. balli': {'name': 'Prof. Shrinivas S. Balli', 'role': 'Dean Student Affairs', 'cabin': '425', 'floor': '4th Floor', 'building': 'Academic Block 1'},
    'shrinivas balli': {'name': 'Prof. Shrinivas S. Balli', 'role': 'Dean Student Affairs', 'cabin': '425', 'floor': '4th Floor', 'building': 'Academic Block 1'},
    'balli': {'name': 'Prof. Shrinivas S. Balli', 'role': 'Dean Student Affairs', 'cabin': '425', 'floor': '4th Floor', 'building': 'Academic Block 1'},
    
    'chetan basavaraj singai': {'name': 'Prof. Chetan Basavaraj Singai', 'role': 'Dean School of Law, Governance and Public Policy', 'cabin': '426', 'floor': '4th Floor', 'building': 'Academic Block 1'},
    'chetan singai': {'name': 'Prof. Chetan Basavaraj Singai', 'role': 'Dean School of Law, Governance and Public Policy', 'cabin': '426', 'floor': '4th Floor', 'building': 'Academic Block 1'},
    'singai': {'name': 'Prof. Chetan Basavaraj Singai', 'role': 'Dean School of Law, Governance and Public Policy', 'cabin': '426', 'floor': '4th Floor', 'building': 'Academic Block 1'},
    
    'dinesh shenoy': {'name': 'Dr. Dinesh Shenoy', 'role': 'Dean School of Management Science', 'cabin': '427', 'floor': '4th Floor', 'building': 'Academic Block 1'},
    'shenoy': {'name': 'Dr. Dinesh Shenoy', 'role': 'Dean School of Management Science', 'cabin': '427', 'floor': '4th Floor', 'building': 'Academic Block 1'},
    
    'sandeep nair': {'name': 'Prof. Sandeep Nair', 'role': 'Dean School of Arts, Humanities and Social Sciences', 'cabin': '428', 'floor': '4th Floor', 'building': 'Academic Block 1'},
    'nair': {'name': 'Prof. Sandeep Nair', 'role': 'Dean School of Arts, Humanities and Social Sciences', 'cabin': '428', 'floor': '4th Floor', 'building': 'Academic Block 1'},
    
    'yashavantha dongre': {'name': 'Prof. Yashavantha Dongre', 'role': 'Vice Chancellor', 'cabin': '464 & 466', 'floor': '4th Floor', 'building': 'Academic Block 1'},
    'dongre': {'name': 'Prof. Yashavantha Dongre', 'role': 'Vice Chancellor', 'cabin': '464 & 466', 'floor': '4th Floor', 'building': 'Academic Block 1'},
    'vice chancellor': {'name': 'Prof. Yashavantha Dongre', 'role': 'Vice Chancellor', 'cabin': '464 & 466', 'floor': '4th Floor', 'building': 'Academic Block 1'},
    'vc': {'name': 'Prof. Yashavantha Dongre', 'role': 'Vice Chancellor', 'cabin': '464 & 466', 'floor': '4th Floor', 'building': 'Academic Block 1'},
    
    's. somanath': {'name': 'Dr. S. Somanath', 'role': 'Chancellor', 'cabin': '465', 'floor': '4th Floor', 'building': 'Academic Block 1'},
    'somanath': {'name': 'Dr. S. Somanath', 'role': 'Chancellor', 'cabin': '465', 'floor': '4th Floor', 'building': 'Academic Block 1'},
    'chancellor': {'name': 'Dr. S. Somanath', 'role': 'Chancellor', 'cabin': '465', 'floor': '4th Floor', 'building': 'Academic Block 1'},
    
    # Academic Block 1 - 3rd Floor
    'bhavani m. r': {'name': 'Dr. Bhavani M. R', 'role': 'Office of Registrar (Evaluation)', 'cabin': '358', 'floor': '3rd Floor', 'building': 'Academic Block 1'},
    'bhavani': {'name': 'Dr. Bhavani M. R', 'role': 'Office of Registrar (Evaluation)', 'cabin': '358', 'floor': '3rd Floor', 'building': 'Academic Block 1'},
    
    'registrar office': {'name': 'Registrar Office', 'role': '', 'cabin': '351', 'floor': '3rd Floor', 'building': 'Academic Block 1'},
    'registrar': {'name': 'Registrar Office', 'role': '', 'cabin': '351', 'floor': '3rd Floor', 'building': 'Academic Block 1'},
    
    'finance office': {'name': 'Finance Office', 'role': '', 'cabin': '377 & 378', 'floor': '3rd Floor', 'building': 'Academic Block 1'},
    'finance': {'name': 'Finance Office', 'role': '', 'cabin': '377 & 378', 'floor': '3rd Floor', 'building': 'Academic Block 1'},
    
    'human resource section': {'name': 'Human Resource Section', 'role': '', 'cabin': '345', 'floor': '3rd Floor', 'building': 'Academic Block 1'},
    'hr section': {'name': 'Human Resource Section', 'role': '', 'cabin': '345', 'floor': '3rd Floor', 'building': 'Academic Block 1'},
    'hr': {'name': 'Human Resource Section', 'role': '', 'cabin': '345', 'floor': '3rd Floor', 'building': 'Academic Block 1'},
    
    # Academic Block 1 - 1st Floor
    'admin front office': {'name': 'Admin Front Office', 'role': '', 'cabin': '139', 'floor': '1st Floor', 'building': 'Academic Block 1'},
    'admin meeting room': {'name': 'Admin Meeting Room', 'role': '', 'cabin': '140', 'floor': '1st Floor', 'building': 'Academic Block 1'},
    'admission hall': {'name': 'Admission Hall', 'role': '', 'cabin': '167', 'floor': '1st Floor', 'building': 'Academic Block 1'},
    'admissions': {'name': 'Admission Hall', 'role': '', 'cabin': '167', 'floor': '1st Floor', 'building': 'Academic Block 1'},
    'hostel warden': {'name': 'Hostel Warden', 'role': '', 'cabin': '136', 'floor': '1st Floor', 'building': 'Academic Block 1'},
    'digi campus verification': {'name': 'Digi Campus Verification', 'role': '', 'cabin': '171', 'floor': '1st Floor', 'building': 'Academic Block 1'},
    
    # Academic Block 1 - Ground Floor
    'library': {'name': 'Library', 'role': '', 'cabin': 'U42', 'floor': 'Ground Floor', 'building': 'Academic Block 1'},
    
    'bharathkumar v': {'name': 'Bharathkumar V', 'role': 'Library Incharge', 'cabin': 'U46', 'floor': 'Ground Floor', 'building': 'Academic Block 1'},
    'bharathkumar': {'name': 'Bharathkumar V', 'role': 'Library Incharge', 'cabin': 'U46', 'floor': 'Ground Floor', 'building': 'Academic Block 1'},
    'library incharge': {'name': 'Bharathkumar V', 'role': 'Library Incharge', 'cabin': 'U46', 'floor': 'Ground Floor', 'building': 'Academic Block 1'},
    
    'library adviser': {'name': 'Library Adviser', 'role': '', 'cabin': 'U45', 'floor': 'Ground Floor', 'building': 'Academic Block 1'},
    'library office': {'name': 'Library Office & Repro', 'role': '', 'cabin': 'U43', 'floor': 'Ground Floor', 'building': 'Academic Block 1'},
    
    # Academic Block 2 - A Wing
    'bharath setturu': {'name': 'Dr. Bharath Setturu', 'role': '', 'cabin': '1', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    'setturu': {'name': 'Dr. Bharath Setturu', 'role': '', 'cabin': '1', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    
    'rajesh kumar prasad': {'name': 'Dr. Rajesh Kumar Prasad', 'role': '', 'cabin': '2', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    'rajesh prasad': {'name': 'Dr. Rajesh Kumar Prasad', 'role': '', 'cabin': '2', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    
    'deepak b': {'name': 'Deepak B', 'role': '', 'cabin': '3', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    'deepak': {'name': 'Deepak B', 'role': '', 'cabin': '3', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    
    'ashith sagar naidu': {'name': 'Ashith Sagar Naidu', 'role': '', 'cabin': '3', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    'ashith': {'name': 'Ashith Sagar Naidu', 'role': '', 'cabin': '3', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    
    'gannavaram sridhar': {'name': 'Gannavaram Sridhar', 'role': '', 'cabin': '3', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    'sridhar': {'name': 'Gannavaram Sridhar', 'role': '', 'cabin': '3', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    
    'bhuvana yv': {'name': 'Bhuvana YV', 'role': '', 'cabin': '3', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    
    'pradeep kumar gopalakrishnan': {'name': 'Sri Pradeep Kumar Gopalakrishnan', 'role': '', 'cabin': '4', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    'pradeep kumar': {'name': 'Sri Pradeep Kumar Gopalakrishnan', 'role': '', 'cabin': '4', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    
    'upkar singh': {'name': 'Dr. Upkar Singh', 'role': '', 'cabin': 'CU7', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    
    'arun kumar': {'name': 'Dr. Arun Kumar', 'role': '', 'cabin': 'CU5', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    
    'chitra gp': {'name': 'Chitra GP', 'role': '', 'cabin': 'CU1', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    'chitra': {'name': 'Chitra GP', 'role': '', 'cabin': 'CU1', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    
    'banu priya m': {'name': 'Banu Priya M', 'role': '', 'cabin': 'CU6', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    'banu priya': {'name': 'Banu Priya M', 'role': '', 'cabin': 'CU6', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    
    'bhagirathi t': {'name': 'Bhagirathi T', 'role': '', 'cabin': 'CU3', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    'bhagirathi': {'name': 'Bhagirathi T', 'role': '', 'cabin': 'CU3', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    
    'bhavana m': {'name': 'Bhavana M', 'role': '', 'cabin': 'CU4', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    
    'mulla arshiya': {'name': 'Mulla Arshiya', 'role': '', 'cabin': 'CU2', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    'arshiya': {'name': 'Mulla Arshiya', 'role': '', 'cabin': 'CU2', 'floor': 'Floor 1', 'building': 'Academic Block 2 A Wing'},
    
    # Academic Block 2 - B Wing
    'shobana': {'name': 'Shobana', 'role': '', 'cabin': '1', 'floor': 'Floor 1', 'building': 'Academic Block 2 B Wing'},
    
    'ashish kumar': {'name': 'Ashish Kumar', 'role': '', 'cabin': '2', 'floor': 'Floor 1', 'building': 'Academic Block 2 B Wing'},
    'ashish': {'name': 'Ashish Kumar', 'role': '', 'cabin': '2', 'floor': 'Floor 1', 'building': 'Academic Block 2 B Wing'},
    
    'vijay': {'name': 'Vijay', 'role': '', 'cabin': '3', 'floor': 'Floor 1', 'building': 'Academic Block 2 B Wing'},
    
    'naresh': {'name': 'Naresh', 'role': '', 'cabin': '4', 'floor': 'Floor 1', 'building': 'Academic Block 2 B Wing'},
    
    'nithesh': {'name': 'Nithesh', 'role': '', 'cabin': 'CU1', 'floor': 'Floor 1', 'building': 'Academic Block 2 B Wing'},
    
    'bhanashankari hosur': {'name': 'Bhanashankari Hosur', 'role': '', 'cabin': 'CU2', 'floor': 'Floor 1', 'building': 'Academic Block 2 B Wing'},
    'bhanashankari': {'name': 'Bhanashankari Hosur', 'role': '', 'cabin': 'CU2', 'floor': 'Floor 1', 'building': 'Academic Block 2 B Wing'},
    
    'nikhil': {'name': 'Nikhil', 'role': '', 'cabin': 'CU3', 'floor': 'Floor 1', 'building': 'Academic Block 2 B Wing'},
    
    'sathyamanikanta': {'name': 'Sathyamanikanta', 'role': '', 'cabin': 'CU4', 'floor': 'Floor 1', 'building': 'Academic Block 2 B Wing'},
    
    'dharaneesh': {'name': 'Dharaneesh', 'role': '', 'cabin': 'CU5', 'floor': 'Floor 1', 'building': 'Academic Block 2 B Wing'},
    
    'amogh': {'name': 'Amogh', 'role': '', 'cabin': 'CU6', 'floor': 'Floor 1', 'building': 'Academic Block 2 B Wing'},
}



class ChatbotService:
    """AI Chatbot service using Google Generative AI"""
    
    def __init__(self):
        self.model = None
        self.last_response_image = None  # Store image URL for person queries
    
    def initialize(self, api_key):
        """Initialize the Gemini model"""
        if api_key:
            genai.configure(api_key=api_key)
            # Use gemini-2.5-flash - latest stable model
            self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        else:
            print("Warning: Google API key not configured. Chatbot will not work.")
    
    def get_context_data(self):
        """Get context data about campus for better responses"""
        context = {
            'events': [],
            'departments': []
        }
        
        # Get upcoming events
        upcoming_events = Event.query.filter(
            Event.event_date >= datetime.utcnow()
        ).order_by(Event.event_date.asc()).limit(10).all()
        
        for event in upcoming_events:
            context['events'].append({
                'title': event.title,
                'description': event.description,
                'date': event.event_date.strftime('%Y-%m-%d %H:%M'),
                'location': event.location
            })
        
        # Get departments
        departments = Department.query.all()
        for dept in departments:
            context['departments'].append({
                'name': dept.name,
                'head': dept.head_of_department,
                'email': dept.contact_email,
                'phone': dept.contact_phone
            })
        
        return context
    
    def get_faculty_info(self, faculty_name):
        """Get detailed faculty information with availability status"""
        # Search for faculty by name (case-insensitive, partial match)
        faculty = User.query.filter(
            User.role == 'Faculty',
            User.full_name.ilike(f'%{faculty_name}%')
        ).first()
        
        if not faculty:
            return None
        
        # Get availability status
        ist = pytz.timezone('Asia/Kolkata')
        today_start = datetime.now(ist).replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        tracking_records = StudentTracking.query.filter(
            StudentTracking.user_id == faculty.id,
            StudentTracking.timestamp >= today_start,
            StudentTracking.timestamp < today_end
        ).order_by(StudentTracking.timestamp.desc()).all()
        
        availability_status = "Not entered today"
        last_entry_time = None
        
        if tracking_records:
            last_record = tracking_records[0]
            last_entry_time = last_record.timestamp.astimezone(ist).strftime('%I:%M %p')
            
            if last_record.entry_type == 'IN':
                availability_status = f"Currently in university (entered at {last_entry_time})"
            else:
                availability_status = f"Left university (last exit at {last_entry_time})"
        
        return {
            'name': faculty.full_name,
            'email': faculty.email,
            'designation': faculty.designation or 'Faculty Member',
            'department': faculty.department.name if faculty.department else 'Not assigned',
            'education': faculty.education or 'Not available',
            'bio': faculty.bio or 'No biography available',
            'research_interests': faculty.research_interests or 'Not specified',
            'profile_image': faculty.profile_image or faculty.profile_picture,
            'availability': availability_status
        }
    
    def build_prompt(self, user_message, user_role=None):
        """Build context-aware prompt"""
        context = self.get_context_data()
        
        system_context = f"""You are a helpful AI assistant for Chanakya University campus. 
You have access to the following information:

FACULTY AND STAFF LOCATIONS:

ACADEMIC BLOCK 1:

4TH FLOOR:
- Prof. Shrinivas S. Balli (Dean Student Affairs) - Cabin 425
- Prof. Chetan Basavaraj Singai (Dean School of Law, Governance and Public Policy) - Cabin 426
- Dr. Dinesh Shenoy (Dean School of Management Science) - Cabin 427
- Prof. Sandeep Nair (Dean School of Arts, Humanities and Social Sciences) - Cabin 428
- Prof. Yashavantha Dongre (Vice Chancellor) - Cabins 464 & 466
- Dr. S. Somanath (Chancellor) - Cabin 465

3RD FLOOR:
- Dr. Bhavani M. R (Office of Registrar - Evaluation) - Cabin 358
- Registrar Office - Cabin 351
- Finance Office - Cabins 377 & 378
- Human Resource Section - Cabin 345

1ST FLOOR:
- Admin Front Office - Cabin 139
- Admin Meeting Room - Cabin 140
- Admission Hall - Cabin 167
- Hostel Warden - Cabin 136
- Digi Campus Verification - Cabin 171

GROUND FLOOR:
- Library - U42
- Bharathkumar V (Library Incharge) - Cabin U46
- Library Adviser - Cabin U45
- Library Office & Repro - Cabin U43
- Library Timings: 9:30 AM to 9:30 PM, Monday to Saturday

LOWER GROUND FLOOR (LG B WING):
- Cafeteria - Admin Block 1, LG B Wing
- Cafeteria Timings: 9:00 AM to 7:30 PM, Monday to Saturday

ACADEMIC BLOCK 2 (SCHOOL OF ENGINEERING):

A WING - FLOOR 1:
- Dr. Bharath Setturu - Cabin 1
- Dr. Rajesh Kumar Prasad - Cabin 2
- Deepak B - Cabin 3
- Ashith Sagar Naidu - Cabin 3
- Gannavaram Sridhar - Cabin 3
- Bhuvana YV - Cabin 3
- Sri Pradeep Kumar Gopalakrishnan - Cabin 4
- Dr. Upkar Singh - CU7
- Dr. Arun Kumar - CU5
- Chitra GP - CU1
- Banu Priya M - CU6
- Bhagirathi T - CU3
- Bhavana M - CU4
- Mulla Arshiya - CU2

B WING - FLOOR 1:
- Shobana - Cabin 1
- Ashish Kumar - Cabin 2
- Vijay - Cabin 3
- Naresh - Cabin 4
- Nithesh - CU1
- Bhanashankari Hosur - CU2
- Nikhil - CU3
- Sathyamanikanta - CU4
- Dharaneesh - CU5
- Amogh - CU6

CHANAKYA UNIVERSITY INFORMATION:

ABOUT THE UNIVERSITY:
Chanakya University is a pioneering exemplar of the vision of a Multidisciplinary University as elucidated in the new National Education Policy (NEP 2020). The university is deeply committed to the creation of a foremost knowledge movement that will harness India's lasting civilizational wisdom to serve society and humanity selflessly. Located in Bangalore, Karnataka, Chanakya University offers a world-class education across multiple disciplines.

SCHOOLS AND DEPARTMENTS:
1. School of Arts, Humanities and Social Sciences (SAHSS)
   - Offers Undergraduate, Postgraduate, and Doctoral Programmes
   - Dean: Prof. Sandeep Nair (Cabin 428, 4th Floor, Academic Block 1)
   - Focuses on humanities, social sciences, and liberal arts education

2. School of Management Sciences (SMS)
   - Offers Undergraduate, Postgraduate, and Doctoral Programmes
   - Dean: Dr. Dinesh Shenoy (Cabin 427, 4th Floor, Academic Block 1)
   - Adopts multidisciplinary approach with in-depth domain knowledge
   - Contact: For specific program details, visit the school office

3. School of Mathematics and Natural Sciences (SMNS)
   - Offers Undergraduate, Postgraduate, and Doctoral Programmes
   - Focuses on mathematics, physics, chemistry, and natural sciences
   - Comprehensive programmes where curiosity meets discovery
   - For dean information, please contact the school office

4. School of Law, Governance and Public Policy (SLGPP)
   - Offers Undergraduate, Postgraduate, and Doctoral Programmes
   - Dean: Prof. Chetan Basavaraj Singai (Cabin 426, 4th Floor, Academic Block 1)
   - Focuses on law, governance, and public policy education

5. School of Biosciences (SB)
   - Committed to providing exceptional educational experience in biosciences
   - Fosters passion for scientific inquiry and discovery
   - Prepares students for careers in biotechnology, life sciences, and research
   - For dean information, please contact the school office

6. School of Engineering (SE)
   - Offers Undergraduate, Postgraduate, and Doctoral Programmes
   - Located in Academic Block 2
   - Covers various engineering disciplines including Computer Science, Mechanical, etc.
   - For dean and faculty information, please visit the school office in Academic Block 2

ADMISSIONS:
- Admissions Office: Cabin 167, 1st Floor, Academic Block 1
- Contact: admissions@chanakyauniversity.edu.in
- Website: https://chanakyauniversity.edu.in/admissions/
- The university offers various programmes at undergraduate, postgraduate, and doctoral levels
- Admission process details and eligibility criteria available on the website

LEADERSHIP:
- Chancellor: Dr. S. Somanath (Cabin 465, 4th Floor, Academic Block 1)
- Vice Chancellor: Prof. Yashavantha Dongre (Cabins 464 & 466, 4th Floor, Academic Block 1)
- Dean Student Affairs: Prof. Shrinivas S. Balli (Cabin 425, 4th Floor, Academic Block 1)

UPCOMING EVENTS:
"""
        
        if context['events']:
            for event in context['events']:
                system_context += f"- {event['title']}: {event['description']} on {event['date']} at {event['location']}\n"
        else:
            system_context += "No upcoming events scheduled.\n"
        
        system_context += "\nDEPARTMENTS:\n"
        if context['departments']:
            for dept in context['departments']:
                system_context += f"- {dept['name']}: Head - {dept['head']}, Contact: {dept['email']}, Phone: {dept['phone']}\n"
        else:
            system_context += "No department information available.\n"
        
        system_context += f"""
Please answer the user's question based on this information. Be helpful, concise, and friendly.

CRITICAL INSTRUCTIONS - READ CAREFULLY:
⚠️ ONLY provide information that is explicitly stated above
⚠️ DO NOT make up or invent faculty names, contact details, or any other information
⚠️ DO NOT hallucinate or fabricate details that are not in the provided context
⚠️ If specific information (like a dean's name or contact) is NOT listed above, say "I don't have that specific information" and suggest visiting the school office or website
⚠️ DO NOT use asterisks (*) or markdown formatting in your responses - use plain text only
⚠️ Write responses in clear, natural language without special formatting characters

GUIDELINES:
- If asked about Chanakya University, schools, programs, or admissions, use ONLY the university information provided above
- If asked about locations, directions, or cabin numbers, use ONLY the faculty locations provided
- If asked about events, schedules, or departments, use ONLY the information provided
- For questions about specific programs or courses, refer to the appropriate school and suggest visiting their website
- For admissions queries, direct to the admissions office (Cabin 167) or email: admissions@chanakyauniversity.edu.in
- If you don't have specific information, say so clearly and suggest: "For detailed information, please visit https://chanakyauniversity.edu.in or contact the relevant school office"
- NEVER invent names, phone numbers, email addresses, or other contact details
- Use plain text without asterisks, bold, or other markdown formatting

User's role: {user_role or 'Guest'}
User's question: {user_message}
"""
        
        return system_context
    
    def get_response(self, user_message, user_id=None, user_role=None):
        """Get chatbot response"""
        # Reset image URL for new query
        self.last_response_image = None
        
        # Try Gemini API first
        if self.model:
            try:
                # Build context-aware prompt
                prompt = self.build_prompt(user_message, user_role)
                
                # Generate response
                response = self.model.generate_content(prompt)
                response_text = response.text
                
                # Store in chat history if user is logged in
                if user_id:
                    chat_record = ChatHistory(
                        user_id=user_id,
                        message=user_message,
                        response=response_text,
                        chat_type='text'
                    )
                    db.session.add(chat_record)
                    db.session.commit()
                
                return {
                    'response': response_text,
                    'image_url': None
                }
            
            except Exception as e:
                print(f"Gemini API error: {str(e)}")
                # Fall through to fallback
        
        # Fallback: Rule-based responses using database
        response_text = self.get_fallback_response(user_message, user_role)
        
        # Store in chat history
        if user_id:
            try:
                chat_record = ChatHistory(
                    user_id=user_id,
                    message=user_message,
                    response=response_text,
                    chat_type='text'
                )
                db.session.add(chat_record)
                db.session.commit()
            except:
                pass
        
        # Return response with image URL if available
        return {
            'response': response_text,
            'image_url': self.last_response_image
        }
    
    def check_person_availability(self, person_name):
        """Check if a specific person is currently in the university"""
        import pytz
        
        # Search for the user by name
        user = User.query.filter(
            db.or_(
                User.full_name.ilike(f'%{person_name}%'),
                User.first_name.ilike(f'%{person_name}%'),
                User.last_name.ilike(f'%{person_name}%')
            )
        ).first()
        
        if not user:
            return None, "Person not found in the system."
        
        # Get today's date in IST
        ist = pytz.timezone('Asia/Kolkata')
        now_ist = datetime.now(ist)
        today_ist = now_ist.date()
        
        # Get all tracking records for this user
        all_tracking_records = StudentTracking.query.filter(
            StudentTracking.user_id == user.id
        ).order_by(StudentTracking.timestamp.desc()).all()
        
        # Filter records for today in IST
        tracking_records = []
        for record in all_tracking_records:
            # Convert UTC timestamp to IST
            utc_time = record.timestamp.replace(tzinfo=pytz.UTC)
            ist_time = utc_time.astimezone(ist)
            if ist_time.date() == today_ist:
                tracking_records.append(record)
        
        # Build detailed user information
        response = f"**{user.full_name}**\n\n"
        
        # Add role
        if user.role:
            response += f"📋 Role: {user.role}\n"
        
        # Add department for students and faculty
        if user.department:
            response += f"🏛️ Department: {user.department.name}\n"
        
        # Add program for students
        if hasattr(user, 'program') and user.program:
            response += f"🎓 Program: {user.program.name}\n"
        
        # Add designation for faculty
        if user.designation:
            response += f"💼 Designation: {user.designation}\n"
        
        # Add email
        response += f"📧 Email: {user.email}\n\n"
        
        # Check presence status
        if not tracking_records:
            response += f"❌ **Status**: Has not entered the university today."
        else:
            # Check the last entry
            last_entry = tracking_records[0]
            
            # Convert entry time to IST for display
            utc_time = last_entry.timestamp.replace(tzinfo=pytz.UTC)
            ist_time = utc_time.astimezone(ist)
            
            if last_entry.entry_type == 'IN':
                # Person is currently in the university
                entry_time = ist_time.strftime('%I:%M %p')
                response += f"✅ **Status**: Currently in the university\n"
                response += f"🕐 Entered at: {entry_time} today"
            else:
                # Person has exited
                exit_time = ist_time.strftime('%I:%M %p')
                response += f"❌ **Status**: Has left the university\n"
                response += f"🕐 Last exit at: {exit_time} today"
        
        # Extract profile image URL
        image_url = None
        if user.profile_image:
            image_url = user.profile_image
        elif user.profile_picture:
            image_url = user.profile_picture
        
        return user, response, image_url
    
    def get_all_present_people(self, role=None):
        """Get all people currently present in the university"""
        import pytz
        
        # Get today's date in IST
        ist = pytz.timezone('Asia/Kolkata')
        now_ist = datetime.now(ist)
        today_ist = now_ist.date()
        
        # Get all tracking records
        query = db.session.query(User, StudentTracking).join(
            StudentTracking, User.id == StudentTracking.user_id
        )
        
        if role:
            query = query.filter(User.role == role)
        
        # Get all tracking records
        all_records = query.all()
        
        # Filter for today in IST and group by user
        user_status = {}
        for user, tracking in all_records:
            # Convert UTC timestamp to IST
            utc_time = tracking.timestamp.replace(tzinfo=pytz.UTC)
            ist_time = utc_time.astimezone(ist)
            
            # Only include records from today (IST)
            if ist_time.date() == today_ist:
                if user.id not in user_status:
                    user_status[user.id] = {'user': user, 'entries': []}
                user_status[user.id]['entries'].append(tracking)
        
        # Determine who is currently present
        present_users = []
        for user_id, data in user_status.items():
            # Sort entries by timestamp descending
            sorted_entries = sorted(data['entries'], key=lambda x: x.timestamp, reverse=True)
            # Check if last entry is IN
            if sorted_entries[0].entry_type == 'IN':
                present_users.append({
                    'user': data['user'],
                    'entry_time': sorted_entries[0].timestamp
                })
        
        return present_users
    
    def get_fallback_response(self, user_message, user_role=None):
        """Fallback rule-based chatbot using database"""
        message_lower = user_message.lower()
        
        # Check for availability queries first
        availability_keywords = [
            'available', 'present', 'in university', 'in campus', 'here today', 
            'came today', 'in college', 'on campus', 'at university', 'at college',
            'entered today', 'came in', 'checked in', 'is here', 'are here',
            'inside', 'inside university', 'inside campus', 'on site'
        ]
        is_availability_query = any(keyword in message_lower for keyword in availability_keywords)
        
        # Also check for student-specific queries
        student_query_patterns = [
            'student', 'students', 'tell me about', 'who is', 'information about',
            'info about', 'details about', 'find student'
        ]
        is_student_query = any(pattern in message_lower for pattern in student_query_patterns)
        
        if is_availability_query or is_student_query or 'is' in message_lower:
            # Check if asking about a specific person
            # Extract potential name from the query
            # Common patterns: "Is [name] available?", "Is [name] in university?", "Is [name] present today?"
            # "Tell me about student [name]", "Is student [name] present?"
            
            potential_name = None
            
            # Try to extract name after "is"
            if 'is ' in message_lower:
                # Get the part after "is"
                after_is = message_lower.split('is ', 1)[1]
                
                # Remove common phrases (order matters - remove longer phrases first)
                removal_phrases = [
                    'student ', 'faculty ', 'professor ', 'prof ', 'dr ',
                    'in the university', 'in university', 'in the campus', 'in campus',
                    'in college', 'in the college', 'on campus', 'on the campus',
                    'at university', 'at the university', 'at college', 'at the college',
                    'available', 'present', 'here today', 'here', 'today',
                    'came today', 'entered today', 'checked in', 'inside', 'the', '?', '.'
                ]
                
                for phrase in removal_phrases:
                    after_is = after_is.replace(phrase, '')
                
                # Clean up extra spaces
                potential_name = ' '.join(after_is.split())
            
            # Try to extract name after "student" or "about"
            elif 'student ' in message_lower or 'about ' in message_lower:
                # Try "student [name]" pattern
                if 'student ' in message_lower:
                    after_student = message_lower.split('student ', 1)[1]
                else:
                    after_student = message_lower.split('about ', 1)[1]
                
                # Remove common phrases
                removal_phrases = [
                    'named ', 'called ', 'is ', 'in the university', 'in university', 
                    'in the campus', 'in campus', 'present', 'available', 
                    'here', 'today', 'the', '?', '.'
                ]
                
                for phrase in removal_phrases:
                    after_student = after_student.replace(phrase, '')
                
                # Clean up extra spaces
                potential_name = ' '.join(after_student.split())
            
            # If we found a potential name, check availability
            if potential_name and len(potential_name) > 2:
                user, message, image_url = self.check_person_availability(potential_name)
                if user:
                    # Store image URL in instance variable for API to access
                    self.last_response_image = image_url
                    return message
            
            # Check for "who is present" or "list present students/faculty"
            if any(phrase in message_lower for phrase in ['who is present', 'who are present', 'list present', 'show present', 'all present']):
                role = None
                if 'student' in message_lower:
                    role = 'Student'
                elif 'faculty' in message_lower or 'teacher' in message_lower or 'professor' in message_lower:
                    role = 'Faculty'
                
                present_people = self.get_all_present_people(role)
                
                if present_people:
                    role_text = f"{role}s" if role else "People"
                    response = f"✅ {role_text} currently present in the university ({len(present_people)}):\n\n"
                    for i, person_data in enumerate(present_people[:20], 1):  # Limit to 20
                        user = person_data['user']
                        entry_time = person_data['entry_time'].strftime('%I:%M %p')
                        response += f"{i}. {user.full_name}"
                        if user.role:
                            response += f" ({user.role})"
                        response += f" - Entered at {entry_time}\n"
                    
                    if len(present_people) > 20:
                        response += f"\n... and {len(present_people) - 20} more"
                    
                    return response.strip()
                else:
                    role_text = f"{role}s" if role else "people"
                    return f"No {role_text} are currently present in the university today."
        
        # Enhanced keyword mapping for schools/departments
        school_keywords = {
            'engineering': ['engineering', 'engineer', 'tech', 'technology', 'cse', 'ece', 'mechanical', 'civil', 'electrical'],
            'management': ['management', 'business', 'mba', 'commerce', 'finance'],
            'law': ['law', 'legal', 'governance', 'policy', 'llb'],
            'biosciences': ['bio', 'bioscience', 'biology', 'life science'],
            'mathematics': ['math', 'mathematics', 'science', 'physics', 'chemistry'],
            'arts': ['arts', 'humanities', 'social', 'literature', 'history']
        }
        
        # Check for "tell me about [school]" or similar queries
        if any(phrase in message_lower for phrase in ['tell me about', 'about', 'what is', 'information about', 'info about']):
            for school_type, keywords in school_keywords.items():
                if any(keyword in message_lower for keyword in keywords):
                    # Find the department
                    dept = Department.query.filter(Department.name.like(f'%{school_type}%')).first()
                    if dept:
                        response = f"📚 {dept.name}\n\n"
                        if dept.head_of_department:
                            response += f"👤 Head: {dept.head_of_department}\n"
                        if dept.contact_email:
                            response += f"📧 Email: {dept.contact_email}\n"
                        if dept.contact_phone:
                            response += f"📞 Phone: {dept.contact_phone}\n"
                        
                        # Get faculty count
                        faculty_count = User.query.join(Department).filter(
                            User.role == 'faculty',
                            Department.id == dept.id
                        ).count()
                        
                        if faculty_count > 0:
                            response += f"\n👨‍🏫 Faculty Members: {faculty_count}\n"
                            response += f"\nWould you like to know more about our faculty? Ask me 'List engineering faculty' or 'Tell me about a specific professor'."
                        
                        return response
                    else:
                        # Generic response about the school
                        school_names = {
                            'engineering': 'School of Engineering',
                            'management': 'School of Management Sciences',
                            'law': 'School of Law, Governance and Public Policy',
                            'biosciences': 'School of Biosciences',
                            'mathematics': 'School of Mathematics and Natural Sciences',
                            'arts': 'School of Arts, Humanities and Social Sciences'
                        }
                        return f"The {school_names.get(school_type, 'school')} is one of our premier academic divisions. For more specific information, please contact the administration office."
        
        # Faculty queries (e.g., "Tell me about Prof. Sandeep Nair", "Who is Prof. Ashok?")
        if any(word in message_lower for word in ['prof', 'professor', 'faculty', 'dr.', 'teacher']):
            # Check if asking about a specific faculty member
            faculty_keywords = ['tell me about', 'who is', 'about', 'information']
            if any(keyword in message_lower for keyword in faculty_keywords):
                # Try to find faculty by name
                users = User.query.filter_by(role='faculty').all()
                
                for user in users:
                    # Check if faculty name is in the message
                    name_parts = user.full_name.lower().split()
                    if any(part in message_lower for part in name_parts if len(part) > 3):
                        response = f"{user.full_name}\n\n"
                        if user.designation:
                            response += f"Designation: {user.designation}\n"
                        if user.department:
                            response += f"Department: {user.department.name}\n"
                        if user.education:
                            response += f"Education: {user.education}\n"
                        if user.bio:
                            response += f"\nAbout: {user.bio}\n"
                        if user.research_interests:
                            response += f"\nResearch Interests: {user.research_interests}\n"
                        response += f"\nEmail: {user.email}"
                        
                        # Add profile image if available
                        if user.profile_image:
                            response += f"\n\nProfile Image: {user.profile_image}"
                        elif user.university_profile_url:
                            response += f"\n\nProfile: {user.university_profile_url}"
                        
                        return response
                
                # If no specific faculty found, ask for clarification
                return "I can help you find information about our faculty. Please provide the faculty member's name. For example: 'Tell me about Prof. Sandeep Nair'"
            
            # List all faculty or faculty by department
            elif 'list' in message_lower or 'all' in message_lower:
                # Check if asking for specific department
                dept_keywords = {
                    'engineering': 'Engineering',
                    'management': 'Management',
                    'law': 'Law',
                    'bioscience': 'Biosciences',
                    'bio': 'Biosciences',
                    'math': 'Mathematics',
                    'science': 'Mathematics',
                    'arts': 'Arts',
                    'humanities': 'Arts'
                }
                
                target_dept = None
                for keyword, dept_name in dept_keywords.items():
                    if keyword in message_lower:
                        target_dept = dept_name
                        break
                
                if target_dept:
                    # List faculty from specific department
                    faculty = User.query.join(Department).filter(
                        User.role == 'faculty',
                        Department.name.like(f'%{target_dept}%')
                    ).all()
                    
                    if faculty:
                        dept_full_name = faculty[0].department.name if faculty[0].department else target_dept
                        response = f"Faculty in {dept_full_name}:\n\n"
                        for i, fac in enumerate(faculty, 1):
                            response += f"{i}. {fac.full_name}\n"
                            response += f"   Email: {fac.email}\n\n"
                        return response.strip()
                    else:
                        return f"No faculty found in {target_dept} department."
                else:
                    # List all faculty (limit to 10)
                    faculty = User.query.filter_by(role='faculty').limit(10).all()
                    if faculty:
                        response = "Faculty at Chanakya University (showing first 10):\n\n"
                        for i, fac in enumerate(faculty, 1):
                            response += f"{i}. {fac.full_name}\n"
                            if fac.department:
                                response += f"   Department: {fac.department.name}\n"
                            response += f"   Email: {fac.email}\n\n"
                        return response.strip()
        
        # Specific department head query (e.g., "Who is the head of Engineering?")
        if 'head' in message_lower and 'of' in message_lower:
            # Extract department name
            dept_keywords = {
                'engineering': 'School of Engineering',
                'management': 'School of Management Sciences',
                'law': 'School of Law, Governance and Public Policy',
                'bioscience': 'School of Biosciences',
                'bio': 'School of Biosciences',
                'math': 'School of Mathematics and Natural Sciences',
                'science': 'School of Mathematics and Natural Sciences',
                'arts': 'School of Arts, Humanities and Social Sciences',
                'humanities': 'School of Arts, Humanities and Social Sciences',
                'social': 'School of Arts, Humanities and Social Sciences'
            }
            
            for keyword, dept_name in dept_keywords.items():
                if keyword in message_lower:
                    dept = Department.query.filter(Department.name.like(f'%{dept_name}%')).first()
                    if dept:
                        response = f"{dept.name}\n\n"
                        if dept.head_of_department:
                            response += f"Head: {dept.head_of_department}\n"
                        if dept.contact_email:
                            response += f"Email: {dept.contact_email}\n"
                        if dept.contact_phone:
                            response += f"Phone: {dept.contact_phone}"
                        return response
            
            # If no specific department found, ask for clarification
            return "I can help you find the head of a department. Which department are you interested in? (Engineering, Management, Law, Biosciences, Mathematics, or Arts)"
        
        # Specific department contact query
        elif 'contact' in message_lower and any(word in message_lower for word in ['engineering', 'management', 'law', 'bio', 'math', 'arts']):
            dept_keywords = {
                'engineering': 'Engineering',
                'management': 'Management',
                'law': 'Law',
                'bio': 'Biosciences',
                'math': 'Mathematics',
                'arts': 'Arts'
            }
            
            for keyword, search_term in dept_keywords.items():
                if keyword in message_lower:
                    dept = Department.query.filter(Department.name.like(f'%{search_term}%')).first()
                    if dept:
                        response = f"Contact Information for {dept.name}:\n\n"
                        if dept.contact_email:
                            response += f"Email: {dept.contact_email}\n"
                        if dept.contact_phone:
                            response += f"Phone: {dept.contact_phone}\n"
                        if dept.head_of_department:
                            response += f"\nHead: {dept.head_of_department}"
                        return response
        
        # Events queries
        elif any(word in message_lower for word in ['event', 'happening', 'schedule', 'upcoming']):
            upcoming_events = Event.query.filter(
                Event.event_date >= datetime.utcnow()
            ).order_by(Event.event_date.asc()).limit(5).all()
            
            if upcoming_events:
                response = "Upcoming Events at Chanakya University:\n\n"
                for i, event in enumerate(upcoming_events, 1):
                    response += f"{i}. {event.title}\n"
                    response += f"   Date: {event.event_date.strftime('%B %d, %Y at %I:%M %p')}\n"
                    response += f"   Location: {event.location}\n"
                    if event.description:
                        # Truncate long descriptions
                        desc = event.description[:150] + "..." if len(event.description) > 150 else event.description
                        response += f"   Info: {desc}\n"
                    response += "\n"
                return response.strip()
            else:
                return "There are no upcoming events scheduled at the moment. Please check back later!"
        
        # General department list query
        elif 'department' in message_lower or 'school' in message_lower:
            # Check if asking about all departments
            if any(word in message_lower for word in ['all', 'list', 'what', 'tell me about']):
                departments = Department.query.all()
                
                if departments:
                    response = "Schools at Chanakya University:\n\n"
                    for i, dept in enumerate(departments, 1):
                        response += f"{i}. {dept.name}\n"
                        if dept.head_of_department:
                            response += f"   Head: {dept.head_of_department}\n"
                        if dept.contact_email:
                            response += f"   Email: {dept.contact_email}\n"
                        response += "\n"
                    return response.strip()
                else:
                    return "Department information is not available at the moment."
            else:
                # Asking about departments in general
                return "We have 6 schools at Chanakya University:\n\n1. School of Engineering\n2. School of Management Sciences\n3. School of Law, Governance and Public Policy\n4. School of Biosciences\n5. School of Mathematics and Natural Sciences\n6. School of Arts, Humanities and Social Sciences\n\nAsk me about a specific school to learn more!"
        
        # Location queries - Check faculty/staff locations first
        elif any(word in message_lower for word in ['where', 'location', 'find', 'located', 'cabin', 'office']):
            # Search for faculty/staff in the message
            found_location = None
            
            # Normalize the message by removing common titles and punctuation
            normalized_message = message_lower.replace('dr.', '').replace('prof.', '').replace('professor', '').replace('.', '').replace(',', '').strip()
            
            # Try to find exact matches or partial matches
            for key, location_data in FACULTY_LOCATIONS.items():
                if key in normalized_message:
                    found_location = location_data
                    break
            
            if found_location:
                # Format the response
                response = f"{found_location['name']}"
                if found_location['role']:
                    response += f" ({found_location['role']})"
                response += f" is located in:\n"
                response += f"  Cabin: {found_location['cabin']}\n"
                response += f"  Floor: {found_location['floor']}\n"
                response += f"  Building: {found_location['building']}"
                return response
            
            # If no specific faculty found, fallback to old location mapping
            locations = {
                'library': 'Upper Ground Floor, Administrative Block "A" Wing',
                'auditorium': 'Upper Ground Floor, Administrative Block "A" Wing',
                'incubation': 'Upper Ground Floor, Administrative Block "A" Wing',
                'incubation centre': 'Upper Ground Floor, Administrative Block "A" Wing',
                'vice chancellor': '4th Floor, Administrative Block "A" Wing',
                'vc': '4th Floor, Administrative Block "A" Wing',
                'dean': '4th Floor, Administrative Block "A" Wing',
                'registrar': '3rd Floor, Administrative Block "A" Wing',
                'finance': '3rd Floor, Administrative Block "A" Wing',
                'communication': '3rd Floor, Administrative Block "A" Wing',
                'procurement': '3rd Floor, Administrative Block "A" Wing',
                'store': '2nd Floor, Administrative Block "A" Wing',
                'classroom': '2nd Floor, Administrative Block "A" Wing',
                'ug classroom': '2nd Floor, Administrative Block "A" Wing',
                'coo': '1st Floor, Administrative Block "A" Wing',
                'admission': '1st Floor, Administrative Block "A" Wing',
                'administrative': '1st Floor, Administrative Block "A" Wing',
                'data centre': 'Lower Ground Floor, Administrative Block "A" Wing',
                'bms': 'Lower Ground Floor, Administrative Block "A" Wing',
                'cafeteria': 'Admin Block 1, LG B Wing',
                'canteen': 'Admin Block 1, LG B Wing'
            }
            
            # Find matching location
            for keyword, location in locations.items():
                if keyword in message_lower:
                    response = f"The {keyword.title()} is located at {location}."
                    # Add timings if available
                    if keyword == 'library':
                        response += "\n\nLibrary Timings:\n9:30 AM to 9:30 PM, Monday to Saturday"
                    elif keyword in ['cafeteria', 'canteen']:
                        response += "\n\nCafeteria Timings:\n9:00 AM to 7:30 PM, Monday to Saturday"
                    return response
            
            # If no specific location found, provide general info
            return """I can help you find faculty and staff locations on campus!

Try asking:
- "Where is Prof. Shrinivas S. Balli?"
- "Where is the library?"
- "What time does the cafeteria open?"
- "Library timings?"
- "What is Naresh's cabin number?"
- "Where is the finance office?"

Or ask me about specific faculty members, offices, or campus locations!"""
        
        # Timing queries for library and cafeteria
        elif any(word in message_lower for word in ['timing', 'timings', 'time', 'hours', 'open', 'close', 'schedule']):
            if 'library' in message_lower:
                return """Library Timings:
📚 9:30 AM to 9:30 PM
📅 Monday to Saturday
📍 Location: Upper Ground Floor, Administrative Block "A" Wing (Cabin U42)

For more information, contact:
Bharathkumar V (Library Incharge) - Cabin U46"""
            elif any(word in message_lower for word in ['cafeteria', 'canteen', 'food', 'dining']):
                return """Cafeteria Timings:
🍽️ 9:00 AM to 7:30 PM
📅 Monday to Saturday
📍 Location: Admin Block 1, LG B Wing

Enjoy your meals!"""
            else:
                return """I can help you with timings for:

📚 Library: 9:30 AM to 9:30 PM (Monday to Saturday)
🍽️ Cafeteria: 9:00 AM to 7:30 PM (Monday to Saturday)

What would you like to know more about?"""
        
        # Help/greeting
        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'help', 'what can you']):
            return """Hello! I'm your Chanakya University AI assistant. I can help you with:

- Student/Faculty Info - "Who is Deepak B?" or "Is Faizan Ansari present?"
- Presence Status - "Is [student name] in the university today?"
- Locations - "Where is the Library?"
- Events - "What events are coming up?"
- Departments - "Tell me about the schools"
- Contact - "Who is the head of Engineering?"

What would you like to know?"""
        
        # Thanks
        elif any(word in message_lower for word in ['thank', 'thanks']):
            return "You're welcome! Feel free to ask if you need anything else."
        
        # Default response - ask for clarification
        else:
            return """I didn't quite understand that. Could you please rephrase your question?

I can help you with:

- Student/Faculty Info - "Who is [name]?" or "Is [name] present?"
- Campus locations - "Where is the Library?"
- Upcoming events - "What events are happening?"
- Department information - "Tell me about Engineering"
- Faculty information - "List engineering faculty"
- Contact details - "Who is the head of Management?"

What would you like to know?"""


# Global chatbot instance
chatbot = ChatbotService()
