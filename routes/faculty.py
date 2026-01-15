from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import db, Event, ChatHistory, Attendance, User
from utils.decorators import faculty_required
from datetime import datetime

faculty_bp = Blueprint('faculty', __name__)


@faculty_bp.route('/dashboard')
@login_required
@faculty_required
def dashboard():
    """Faculty dashboard"""
    from models import Attendance
    from datetime import datetime, date
    
    # Get upcoming events
    upcoming_events = Event.query.filter(
        Event.event_date >= datetime.utcnow()
    ).order_by(Event.event_date.asc()).limit(5).all()
    
    # Get statistics
    total_students = User.query.filter_by(role='Student', is_active=True).count()
    total_classes = 0  # Can be enhanced later with actual class data
    
    # Get today's attendance count
    today = date.today()
    attendance_today = Attendance.query.filter(
        db.func.date(Attendance.timestamp) == today
    ).count()
    
    return render_template('faculty/dashboard.html',
                         faculty_name=current_user.full_name,
                         upcoming_events=upcoming_events,
                         total_students=total_students,
                         total_classes=total_classes,
                         attendance_today=attendance_today)


@faculty_bp.route('/events')
@login_required
@faculty_required
def events():
    """View all upcoming events"""
    upcoming_events = Event.query.filter(
        Event.event_date >= datetime.utcnow()
    ).order_by(Event.event_date.asc()).all()
    
    return render_template('faculty/events.html', events=upcoming_events)


@faculty_bp.route('/profile')
@login_required
@faculty_required
def profile():
    """Faculty profile page"""
    # Get events created by this faculty
    events_created = Event.query.filter_by(created_by=current_user.id).count()
    
    # Get students in same department
    students_count = User.query.filter_by(
        role='student',
        department_id=current_user.department_id
    ).count() if current_user.department_id else 0
    
    # Get chat interactions
    chat_count = ChatHistory.query.filter_by(user_id=current_user.id).count()
    
    return render_template('faculty/profile.html',
                         events_created=events_created,
                         students_count=students_count,
                         chat_count=chat_count)


@faculty_bp.route('/chat')
@login_required
@faculty_required
def chat():
    """Chatbot interface"""
    return render_template('faculty/chat.html')


@faculty_bp.route('/chat/history')
@login_required
@faculty_required
def chat_history():
    """View chat history"""
    history = ChatHistory.query.filter_by(
        user_id=current_user.id
    ).order_by(ChatHistory.timestamp.desc()).all()
    
    return render_template('faculty/chat_history.html', history=history)


@faculty_bp.route('/attendance')
@login_required
@faculty_required
def attendance():
    """View attendance records"""
    # Get students in the same department
    if current_user.department_id:
        students = db.session.query(User).filter_by(
            department_id=current_user.department_id,
            role='Student'
        ).all()
        
        attendance_records = Attendance.query.filter(
            Attendance.user_id.in_([s.id for s in students])
        ).order_by(Attendance.timestamp.desc()).limit(50).all()
    else:
        students = []
        attendance_records = []
    
    return render_template('faculty/attendance.html',
                         students=students,
                         attendance_records=attendance_records)


@faculty_bp.route('/anonymous-messages')
@login_required
@faculty_required
def anonymous_messages():
    """View anonymous messages from students"""
    return render_template('faculty/anonymous_message.html')


@faculty_bp.route('/api/monitor-attention', methods=['POST'])
@login_required
@faculty_required
def monitor_attention():
    """
    API endpoint for real-time attention monitoring
    Accepts video frame and returns attention analysis
    """
    from services.attention_monitoring import attention_service
    from models.attention_log import AttentionLog
    import cv2
    import numpy as np
    import uuid
    
    try:
        # Get image from request
        if 'image' not in request.files:
            return {'error': 'No image provided', 'success': False}, 400
        
        image_file = request.files['image']
        image_data = image_file.read()
        
        # Convert to numpy array
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return {'error': 'Invalid image data', 'success': False}, 400
        
        # Analyze attention
        result = attention_service.analyze_attention(image)
        
        if not result['success']:
            return {'error': result.get('error', 'Analysis failed'), 'success': False}, 500
        
        # Get or create session ID from request
        session_id = request.form.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Log to database (sample every 5 seconds to avoid spam)
        # Frontend should send session_id and only log periodically
        should_log = request.form.get('log', 'false').lower() == 'true'
        
        if should_log:
            attention_log = AttentionLog(
                faculty_id=current_user.id,
                session_id=session_id,
                total_students=result['total_faces'],
                focused_count=result['focused_count'],
                distracted_count=result['distracted_count'],
                alert_triggered=result['alert']
            )
            db.session.add(attention_log)
            db.session.commit()
        
        # Return analysis results
        return {
            'success': True,
            'session_id': session_id,
            'total_faces': result['total_faces'],
            'focused_count': result['focused_count'],
            'distracted_count': result['distracted_count'],
            'alert': result['alert'],
            'faces': result['faces']
        }
        
    except Exception as e:
        print(f"Error in monitor_attention: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'error': str(e), 'success': False}, 500

