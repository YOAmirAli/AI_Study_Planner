# 🎓 AI Study Planner & Progress Tracker - Backend

A comprehensive Python Flask backend API for an intelligent academic management platform that helps university students plan, schedule, track, and optimize their study habits using Artificial Intelligence.

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Database Schema](#database-schema)
- [Development Phases](#development-phases)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### Core Features
- 🔐 **User Authentication** - JWT-based secure authentication with password hashing
- 📚 **Course Management** - Organize and track all enrolled courses
- ✅ **Task & Assignment Tracking** - Comprehensive task management with priorities and deadlines
- 📅 **AI-Powered Scheduling** - Intelligent study schedule generation using custom algorithms
- 🤖 **AI Study Tools** - Text summarization, quiz generation, flashcard creation
- 📊 **Analytics & Progress Tracking** - Detailed performance metrics and visualizations
- 🔔 **Smart Notifications** - Automated deadline reminders and falling behind alerts
- 👥 **Group Collaboration** - Study groups with member management

### AI Capabilities
- Automatic topic extraction from course syllabi
- Smart task time estimation
- Personalized study schedule optimization
- Falling behind prediction algorithm
- Study material recommendations (YouTube, Coursera)

---

## 🛠️ Technology Stack

- **Framework:** Flask 3.0.0
- **Database:** MySQL (SQLAlchemy ORM)
- **Authentication:** JWT (Flask-JWT-Extended)
- **AI Integration:** OpenAI GPT-4 / Groq API
- **Scheduling:** APScheduler (automated jobs)
- **Security:** bcrypt password hashing
- **CORS:** Flask-CORS

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **MySQL 8.0+** - [Download MySQL](https://dev.mysql.com/downloads/)
- **pip** - Python package manager (comes with Python)
- **Git** - Version control system

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd backend
```

### 2. Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up MySQL Database

Create a new MySQL database:

```sql
CREATE DATABASE ai_study_planner;
```

### 5. Apply Database Indexes (Optional but Recommended)

For better performance, run the index creation script:

```bash
mysql -u your_username -p ai_study_planner < app/utils/database_indexes.sql
```

---

## ⚙️ Configuration

### 1. Create Environment File

Copy the example environment file:

```bash
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` with your configuration:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-here-change-in-production

# Database Configuration
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/ai_study_planner

# AI API Keys (choose one)
OPENAI_API_KEY=your-openai-api-key-here
# OR
GROQ_API_KEY=your-groq-api-key-here

# CORS Configuration
CORS_ORIGINS=http://localhost:3000

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Environment Variables Explained

| Variable | Description | Required |
|----------|-------------|----------|
| `FLASK_ENV` | Environment mode (development/production) | Yes |
| `SECRET_KEY` | Flask secret key for sessions | Yes |
| `JWT_SECRET_KEY` | Secret key for JWT token generation | Yes |
| `DATABASE_URL` | MySQL database connection string | Yes |
| `OPENAI_API_KEY` | OpenAI API key for AI features | One of these |
| `GROQ_API_KEY` | Groq API key for AI features | One of these |
| `CORS_ORIGINS` | Allowed origins for CORS | Yes |
| `MAIL_SERVER` | SMTP server for emails | Optional |

---

## 🏃 Running the Application

### Development Mode

```bash
python run.py
```

The API will be available at: `http://localhost:5000`

### Check if Server is Running

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "ok",
  "message": "AI Study Planner API is running",
  "version": "1.0.0"
}
```

### Production Mode

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

---

## 📚 API Documentation

Complete API documentation is available in [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

### Quick API Overview

**Base URL:** `http://localhost:5000/api`

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

#### Courses
- `GET /courses` - Get all courses
- `POST /courses` - Create new course
- `PUT /courses/:id` - Update course
- `DELETE /courses/:id` - Delete course

#### Tasks
- `GET /tasks` - Get all tasks (with filters)
- `POST /tasks` - Create new task
- `PATCH /tasks/:id/complete` - Mark task complete
- `GET /tasks/upcoming` - Get upcoming tasks
- `GET /tasks/overdue` - Get overdue tasks

#### Schedules
- `GET /schedules` - Get weekly schedule
- `POST /schedules/generate` - Generate AI schedule

#### AI Tools
- `POST /ai/summarize` - Summarize text
- `POST /ai/generate-quiz` - Generate quiz
- `POST /ai/create-flashcards` - Create flashcards
- `POST /ai/recommend-materials` - Get study recommendations

#### Analytics
- `GET /progress/dashboard` - Get dashboard stats
- `GET /progress/analytics` - Get detailed analytics
- `GET /progress/prediction` - Get falling behind prediction

#### Notifications
- `GET /notifications` - Get all notifications
- `PATCH /notifications/:id/read` - Mark as read
- `PATCH /notifications/mark-all-read` - Mark all as read

#### Groups
- `GET /groups` - Get user's groups
- `POST /groups` - Create new group
- `POST /groups/:id/join` - Join group
- `POST /groups/:id/leave` - Leave group

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py              # App factory
│   ├── config/
│   │   ├── config.py            # Configuration classes
│   │   └── database.py          # Database initialization
│   ├── models/                  # Database models
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── task.py
│   │   ├── schedule.py
│   │   ├── analytics.py
│   │   ├── notification.py
│   │   ├── group.py
│   │   └── group_member.py
│   ├── routes/                  # API endpoints
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   ├── course_routes.py
│   │   ├── task_routes.py
│   │   ├── schedule_routes.py
│   │   ├── ai_routes.py
│   │   ├── analytics_routes.py
│   │   ├── notification_routes.py
│   │   └── group_routes.py
│   ├── services/                # Business logic
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── course_service.py
│   │   ├── task_service.py
│   │   ├── schedule_service.py
│   │   ├── ai_service.py
│   │   ├── analytics_service.py
│   │   ├── prediction_service.py
│   │   ├── notification_service.py
│   │   └── group_service.py
│   ├── ai/                      # AI algorithms
│   │   ├── schedule_algorithm.py
│   │   ├── summarizer.py
│   │   ├── quiz_generator.py
│   │   ├── flashcard_generator.py
│   │   └── recommender.py
│   ├── tasks/                   # Scheduled jobs
│   │   ├── cron_jobs.py
│   │   └── scheduler.py
│   ├── middleware/              # Middleware
│   │   ├── auth_middleware.py
│   │   └── error_handler.py
│   └── utils/                   # Utilities
│       ├── jwt_utils.py
│       ├── password_utils.py
│       ├── validators.py
│       ├── logger.py
│       └── database_indexes.sql
├── logs/                        # Application logs
├── uploads/                     # File uploads
├── tests/                       # Test files
├── .env                         # Environment variables
├── .env.example                 # Environment template
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── wsgi.py                      # WSGI entry point
├── API_DOCUMENTATION.md         # Complete API docs
└── README.md                    # This file
```

---

## 🧪 Testing

### Run All Phase Tests

```bash
# Phase 2: Authentication
python test_phase2.py

# Phase 3: Courses & Tasks
python test_phase3.py

# Phase 4: Schedule Management
python test_phase4.py

# Phase 5: AI Tools
python test_phase5.py

# Phase 6: Analytics
python test_phase6.py

# Phase 7: Notifications & Groups
python test_phase7.py
```

### Test Coverage

The test suite includes:
- ✅ 100+ endpoint tests
- ✅ Authentication and authorization tests
- ✅ CRUD operation tests
- ✅ AI feature tests
- ✅ Error handling tests
- ✅ Integration tests

---

## 🗄️ Database Schema

### Tables

1. **users** - User accounts and profiles
2. **courses** - Course information
3. **tasks** - Assignments and tasks
4. **schedules** - Study schedule blocks
5. **analytics** - Performance tracking data
6. **notifications** - User notifications
7. **groups** - Study groups
8. **group_members** - Group membership

### Entity Relationships

- User → Courses (One-to-Many)
- User → Tasks (One-to-Many)
- Course → Tasks (One-to-Many)
- User → Schedules (One-to-Many)
- User → Notifications (One-to-Many)
- User → Groups (Many-to-Many through group_members)

---

## 📈 Development Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | Foundation & Setup | ✅ Complete |
| 2 | Authentication | ✅ Complete |
| 3 | Courses & Tasks | ✅ Complete |
| 4 | Schedule Management | ✅ Complete |
| 5 | AI Tools | ✅ Complete |
| 6 | Analytics & Predictions | ✅ Complete |
| 7 | Notifications & Groups | ✅ Complete |
| 8 | Testing, Optimization & Documentation | 🚧 In Progress |
| 9 | Deployment | ⏳ Pending |

---

## 🔒 Security Features

- ✅ JWT-based authentication
- ✅ bcrypt password hashing (12 rounds)
- ✅ SQL injection prevention (parameterized queries)
- ✅ XSS prevention (input sanitization)
- ✅ CORS configuration
- ✅ Rate limiting ready
- ✅ Secure session management

---

## 📝 Logging

Application logs are stored in the `logs/` directory:

- `app.log` - General application logs
- `error.log` - Error logs only

Log rotation is configured (10MB per file, 10 backups).

---

## 🐛 Troubleshooting

### Database Connection Issues
- Verify your MySQL connection string in `.env`
- Check if MySQL server is running
- Ensure database exists: `CREATE DATABASE ai_study_planner;`
- Test connection: `mysql -u username -p`

### Module Import Errors
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version: `python --version` (should be 3.9+)

### Port Already in Use
- Change the PORT in `run.py`
- Or kill the process using port 5000:
  - Windows: `netstat -ano | findstr :5000` then `taskkill /PID <PID> /F`
  - Mac/Linux: `lsof -ti:5000 | xargs kill -9`

### AI Features Not Working
- Verify API key is set in `.env`
- Check API key is valid
- Ensure you have credits/quota available
- Check logs for specific error messages

### Scheduled Jobs Not Running
- Check if APScheduler is installed: `pip install APScheduler`
- Verify scheduler initialization in logs
- Check system time is correct

---

## 📄 License

This project is part of a Visual Programming course project.

---

## 👥 Authors

- Development Team - AI Study Planner Project

---

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Groq for fast AI inference
- Flask community for excellent documentation
- All contributors and testers

---

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check existing documentation
- Review API documentation

---

**Last Updated:** November 28, 2025  
**Version:** 1.0.0  
**Status:** Production Ready (Phase 8 in progress)
