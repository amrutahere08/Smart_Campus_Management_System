# 🎓 AI-Powered University Assistant & Smart Campus Monitoring System

## Overview

The Smart Campus Monitoring System is a web-based application designed to streamline university operations through automation and artificial intelligence. This platform addresses common challenges in campus management by providing automated attendance tracking, intelligent query resolution, and comprehensive visitor management.

Built as a final year project, this system demonstrates the practical application of machine learning and web development technologies to solve real-world problems in educational institutions.

## Problem Statement

Traditional campus management systems face several challenges:
- Manual attendance tracking is time-consuming and prone to errors
- Students struggle to find accurate information about campus activities and schedules
- Visitor management requires significant administrative overhead
- Security personnel lack real-time monitoring tools
- Emotional well-being of students often goes unnoticed

This project aims to address these issues through an integrated platform that leverages modern AI technologies.

## Core Features

### Automated Attendance System
The system uses face recognition technology to automatically mark attendance when students enter campus premises. This eliminates the need for manual roll calls and reduces proxy attendance. The face recognition module is built using the dlib library, which provides 128-dimensional face encodings for accurate identification.

### AI-Powered University Assistant
An intelligent chatbot powered by Google's Gemini AI helps students and faculty find information quickly. The assistant can answer queries about campus events, course schedules, faculty information, and general university policies. The chatbot maintains conversation context to provide more relevant responses.

### Visitor Management
A digital system for managing campus visitors that includes:
- Self-service kiosk for visitor registration
- Automated entry and exit logging
- Real-time tracking of visitor locations
- Historical records for security audits

### Emotion Detection
The system analyzes facial expressions to detect emotions during campus entry. This data helps counselors identify students who may need support, enabling proactive mental health interventions.

### Role-Based Access Control
Different user types have access to specific features:
- Administrators can manage users, courses, events, and system settings
- Faculty members can view attendance records and manage their classes
- Students can check their attendance history and interact with the chatbot
- Security personnel can monitor entries and exits in real-time
- Counselors can access emotion tracking data for student welfare

## Technical Architecture

### Backend Framework
The application is built using Flask, a lightweight Python web framework. Flask was chosen for its simplicity and flexibility, making it ideal for rapid development and easy integration with machine learning libraries.

### Database Design
SQLite serves as the database management system, with SQLAlchemy as the ORM layer. The database schema includes tables for users, attendance records, visitor logs, emotion tracking, chat history, and system events. The normalized design ensures data integrity and efficient querying.

### Machine Learning Components

**Face Recognition**: The system uses the face_recognition library, which is built on top of dlib's state-of-the-art face recognition algorithms. Each registered user's face is encoded into a 128-dimensional vector, which is then compared against detected faces for identification.

**Emotion Detection**: DeepFace library with TensorFlow backend analyzes facial expressions to classify emotions into seven categories: happy, sad, angry, fear, surprise, disgust, and neutral. The model provides confidence scores for each prediction.

**Natural Language Processing**: Google's Gemini AI model processes natural language queries and generates contextually appropriate responses. The system includes custom prompts to ensure responses are relevant to the university context.

### Frontend Technologies
The user interface is built with HTML5, CSS3, and vanilla JavaScript. The design prioritizes usability and responsiveness, ensuring the application works across different devices and screen sizes.

## System Requirements

### Software Dependencies
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Hardware Requirements
- Minimum 4GB RAM
- Webcam for face recognition features
- Stable internet connection for AI chatbot functionality

### API Keys
- Google API key for Gemini AI integration (required for chatbot features)

## Installation Guide

### Step 1: Clone the Repository
```bash
git clone https://github.com/Abhilashg23/AI-Powered-University-Assistant-Smart-Campus-Monitoring-System.git
cd AI-Powered-University-Assistant-Smart-Campus-Monitoring-System
```

### Step 2: Set Up Virtual Environment
Creating a virtual environment isolates project dependencies from your system Python installation.

For Linux/Mac:
```bash
python3 -m venv myenv
source myenv/bin/activate
```

For Windows:
```bash
python -m venv myenv
myenv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirement.txt
```

This will install all necessary packages including Flask, SQLAlchemy, OpenCV, face_recognition, DeepFace, and TensorFlow.

### Step 4: Configure Environment Variables
Copy the example environment file and add your API keys:
```bash
cp .env.example .env
```

Edit the `.env` file and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

### Step 5: Initialize Database
Run the database initialization script to create all necessary tables:
```bash
python init_db.py
```

This script creates the database schema and populates it with sample data for testing.

## Running the Application

### Quick Start Method
Use the provided shell script that handles environment activation and server startup:
```bash
bash run.sh
```

### Manual Start Method
```bash
python app.py
```

The application will start on `http://localhost:5001`. Open this URL in your web browser to access the system.

## Default Login Credentials

For testing purposes, the following default accounts are available:

| Role | Username | Password |
|------|----------|----------|
| Administrator | admin | Admin@123 |
| Faculty | faculty1 | Faculty@123 |
| Student | student1 | Student@123 |
| Security | security | Security@123 |

Note: Change these credentials in a production environment.

## Project Structure

```
SmartCampusFinal/
├── app.py                  # Application entry point
├── config.py              # Configuration settings
├── models/                # Database models
│   ├── __init__.py
│   └── user.py
├── routes/                # Application routes
│   ├── auth.py           # Authentication routes
│   ├── admin.py          # Admin dashboard
│   ├── student.py        # Student dashboard
│   ├── faculty.py        # Faculty dashboard
│   ├── security.py       # Security dashboard
│   └── api/              # API endpoints
│       ├── face.py       # Face recognition API
│       ├── chat.py       # Chatbot API
│       └── emotion.py    # Emotion detection API
├── services/              # Business logic
│   ├── face_recognition.py
│   ├── emotion_detection.py
│   └── chatbot.py
├── templates/             # HTML templates
├── static/               # CSS, JavaScript, images
├── data/                 # Face encodings and training data
└── instance/             # Database files

```

## API Documentation

### Face Recognition API

**Endpoint**: `/api/face/verify`  
**Method**: POST  
**Content-Type**: multipart/form-data

Request:
```
image: [binary image file]
```

Response:
```json
{
  "success": true,
  "message": "IN: John Doe",
  "user": {
    "full_name": "John Doe",
    "registration_id": "STU001",
    "role": "Student"
  },
  "entry_type": "IN",
  "emotion": {
    "dominant_emotion": "happy",
    "confidence": 0.89
  }
}
```

### Chatbot API

**Endpoint**: `/api/chat/message`  
**Method**: POST  
**Content-Type**: application/json

Request:
```json
{
  "message": "What time does the library close?",
  "user_id": 1
}
```

Response:
```json
{
  "success": true,
  "response": "The library is open from 8:00 AM to 10:00 PM on weekdays..."
}
```

## Database Schema

### Users Table
Stores information about all system users including students, faculty, and staff.

Fields: id, username, password_hash, full_name, email, role, department_id, is_active, is_approved, created_at

### Student Tracking Table
Records entry and exit events for attendance tracking.

Fields: id, user_id, entry_type, timestamp, location

### Emotion Tracking Table
Stores emotion detection results for student welfare monitoring.

Fields: id, user_id, emotion, confidence, timestamp

### Face Data Table
Contains face encodings for registered users.

Fields: id, user_id, face_encoding, created_at, updated_at

## Security Considerations

### Password Security
User passwords are hashed using Werkzeug's security functions before storage. The system never stores plain text passwords.

### Session Management
Flask-Login handles user sessions with secure cookies. Sessions expire after a period of inactivity.

### API Security
API endpoints validate user authentication and authorization before processing requests. Rate limiting can be implemented to prevent abuse.

### Data Privacy
Face encodings are stored as binary data and cannot be reverse-engineered to recreate the original image. Emotion tracking data is accessible only to authorized counselors and administrators.

## Testing

### Unit Tests
Run the test suite to verify core functionality:
```bash
python -m pytest tests/
```

### Manual Testing
1. Test user registration and login with different roles
2. Verify face recognition accuracy with multiple users
3. Check chatbot responses for various queries
4. Validate visitor entry and exit logging
5. Confirm emotion detection accuracy

## Troubleshooting

### Common Issues

**Issue**: Face recognition not working  
**Solution**: Ensure webcam permissions are granted and lighting conditions are adequate. The face should be clearly visible and facing the camera.

**Issue**: Chatbot not responding  
**Solution**: Verify that the Google API key is correctly set in the `.env` file and that you have an active internet connection.

**Issue**: Database errors on startup  
**Solution**: Delete the existing database file and run `python init_db.py` again to recreate the schema.

**Issue**: Import errors for face_recognition  
**Solution**: The face_recognition library requires dlib, which may need additional system dependencies. On Windows, install Visual C++ build tools. On Linux, install cmake and build-essential.

## Future Enhancements

Potential improvements for future versions:
- Mobile application for iOS and Android
- Integration with existing university management systems
- Advanced analytics dashboard with data visualization
- Multi-language support for international students
- Biometric authentication options beyond face recognition
- Integration with campus IoT devices for smart classroom management

## Contributing

Contributions to improve the system are welcome. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Test thoroughly before submitting
5. Create a pull request with a detailed description

## Acknowledgments

This project was developed as part of the MCA curriculum by a team of 2 members.We would like to express our gratitude to:
- Our faculty advisors for their continuous guidance and support throughout the development process
- The open source communities for providing excellent libraries and frameworks
- Our college for providing the necessary infrastructure and resources

## License

This project is released under the MIT License. You are free to use, modify, and distribute this software for educational and commercial purposes.

## Contact

For questions, suggestions, or bug reports, please open an issue on the GitHub repository or contact the development team.

---

Developed as a academic project to demonstrate practical applications of artificial intelligence in educational technology.

## Project Information

> This is a group academic project developed by 2 members.   
> Original development was done collaboratively as part of academic project.
