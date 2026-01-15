from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import db, Event, ChatHistory, Attendance
from utils.decorators import student_required
from datetime import datetime

student_bp = Blueprint('student', __name__)


@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    """Student dashboard"""
    # Get upcoming events
    upcoming_events = Event.query.filter(
        Event.event_date >= datetime.utcnow()
    ).order_by(Event.event_date.asc()).limit(5).all()
    
    return render_template('student/dashboard.html',
                         student_name=current_user.full_name,
                         upcoming_events=upcoming_events)


@student_bp.route('/events')
@login_required
@student_required
def events():
    """View all upcoming events"""
    upcoming_events = Event.query.filter(
        Event.event_date >= datetime.utcnow()
    ).order_by(Event.event_date.asc()).all()
    
    return render_template('student/events.html', events=upcoming_events)


@student_bp.route('/profile')
@login_required
@student_required
def profile():
    """Student profile page"""
    # Get attendance count
    attendance_count = Attendance.query.filter_by(user_id=current_user.id).count()
    
    # Get events count (could be registrations or attended events)
    event_count = Event.query.filter(Event.event_date >= datetime.utcnow()).count()
    
    return render_template('student/profile.html',
                         attendance_count=attendance_count,
                         event_count=event_count)


@student_bp.route('/chat')
@login_required
@student_required
def chat():
    """Chatbot interface"""
    return render_template('student/chat.html')


@student_bp.route('/chat/history')
@login_required
@student_required
def chat_history():
    """View chat history"""
    history = ChatHistory.query.filter_by(
        user_id=current_user.id
    ).order_by(ChatHistory.timestamp.desc()).all()
    
    return render_template('student/chat_history.html', history=history)
