#!/bin/bash
# Smart Campus - One Command Run Script

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           🚀 SMART CAMPUS - QUICK START                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Navigate to project directory
cd "/Users/abhi/Documents/Smart Campus"

# Check if virtual environment exists
if [ ! -d "myenv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv myenv
    source myenv/bin/activate
    echo "📦 Installing dependencies..."
    pip install -r requirement.txt
else
    source myenv/bin/activate
fi

# Check if database exists
if [ ! -f "instance/smart_campus.db" ]; then
    echo "📊 Database not found. Initializing..."
    python3 init_db.py
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your GOOGLE_API_KEY"
fi

echo ""
echo "✅ Environment: Activated"
echo "✅ Database: Ready"
echo "✅ Dependencies: Installed"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 Starting Smart Campus on http://localhost:5001"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Default Login Credentials:"
echo "   👨‍💼 Admin:    admin / Admin@123"
echo "   👨‍🎓 Student:  student1 / Student@123"
echo "   👨‍🏫 Faculty:  faculty1 / Faculty@123"
echo "   👮 Security: security / Security@123"
echo ""
echo "🎯 Quick Links:"
echo "   🏠 Home:     http://localhost:5001"
echo "   👤 Login:    http://localhost:5001/auth/login"
echo "   🚪 Visitor:  http://localhost:5001/visitor"
echo ""
echo "Press CTRL+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run the application
python3 app.py
