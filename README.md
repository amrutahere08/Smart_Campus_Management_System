# 🎓 AI-Powered University Assistant & Smart Campus Monitoring System

A comprehensive Smart Campus solution integrating AI-driven features for enhanced security, efficient management, and improved student experience.

## 🚀 Overview

This project is a web-based application built with **Flask** that serves as a central hub for university operations. It leverages Artificial Intelligence for key functionalities like face recognition-based attendance, an intelligent chatbot for query resolution, and a robust visitor management system.

## ✨ Key Features

### 🤖 AI University Assistant (Chatbot)
-   Intelligent chatbot powered by **Gemini AI** (or configured model).
-   Answers student and faculty queries regarding campus activities, schedules, and more.
-   Voice-enabled interaction capabilities.

### 📸 Smart Attendance System
-   **Face Recognition**: Automated attendance marking using computer vision.
-   Real-time detection and verification of registered students and faculty.
-   Secure and tamper-proof attendance logging.

### 👥 Visitor Management System
-   Digital entry/exit logging for visitors.
-   Kiosk mode for self-registration.
-   Admin dashboard to track visitor history and current campus occupancy.

### 🛡️ Security & Monitoring
-   Dedicated Security Panel for gatekeepers.
-   Real-time monitoring of campus entries and exits.
-   Alerts and tracking for unauthorized access attempts.

### 📊 Role-Based Dashboards
-   **Admin**: Full control over users, courses, events, and system settings.
-   **Faculty**: Manage classes, view attendance, and interact with students.
-   **Student**: View attendance, schedules, and access the chatbot.
-   **Security**: Monitor gate entries and visitor logs.

## 🛠️ Tech Stack

-   **Backend**: Python (Flask)
-   **Frontend**: HTML5, CSS3, JavaScript
-   **Database**: SQLite
-   **AI/ML**: TensorFlow/Keras (Face Recognition), Gemini API (Chatbot)
-   **Tools**: OpenCV, MediaPipe

## 📦 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Abhilashg23/AI-Powered-University-Assistant-Smart-Campus-Monitoring-System.git
    cd AI-Powered-University-Assistant-Smart-Campus-Monitoring-System
    ```

2.  **Set Up Environment**
    It is recommended to use a virtual environment.
    ```bash
    python3 -m venv myenv
    source myenv/bin/activate  # On Windows use: myenv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirement.txt
    ```

4.  **Environment Variables**
    -   Copy `.env.example` to `.env`.
    -   Add your API keys (e.g., `GOOGLE_API_KEY` for the chatbot) in the `.env` file.

5.  **Initialize Database**
    ```bash
    python3 init_db.py
    ```

## 🚀 Running the Application

### Option 1: Quick Start (Recommended)
We provide a helper script to handle everything for you.
```bash
bash run.sh
```

### Option 2: Manual Start
```bash
python3 app.py
```
The application will start at `http://localhost:5001`.

## 🔐 Default Login Credentials

| Role | Username | Password |
| :--- | :--- | :--- |
| **Admin** | `admin` | `Admin@123` |
| **Faculty** | `faculty1` | `Faculty@123` |
| **Student** | `student1` | `Student@123` |
| **Security** | `security` | `Security@123` |

## 🤝 Contributing

Contributions are welcome! Please feel free to verify functionality, submit issues, or create pull requests.

## 📄 License

This project is licensed under the MIT License.
