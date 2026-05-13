# 📚 AI Study Planner - Complete API Documentation

**Base URL:** `http://localhost:5000/api` (Development)  
**Authentication:** JWT Bearer Token (except public endpoints)  
**Content-Type:** `application/json`

---

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [User Management](#user-management)
3. [Course Management](#course-management)
4. [Task Management](#task-management)
5. [Schedule Management](#schedule-management)
6. [AI Tools](#ai-tools)
7. [Analytics & Progress](#analytics--progress)
8. [Notifications](#notifications)
9. [Group Collaboration](#group-collaboration)
10. [Error Codes](#error-codes)

---

## 🔐 Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

### Register User
**POST** `/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "name": "John Doe",
  "university": "MIT",
  "program": "Computer Science"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "user_id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "university": "MIT",
    "program": "Computer Science"
  }
}
```

---

### Login
**POST** `/auth/login`

Authenticate and receive JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "user_id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

---

### Get Current User
**GET** `/auth/me` 🔒

Get authenticated user's information.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "user": {
    "user_id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "university": "MIT",
    "program": "Computer Science",
    "created_at": "2025-11-20T10:00:00"
  }
}
```

---

## 👤 User Management

### Get User Profile
**GET** `/users/profile` 🔒

**Response (200):**
```json
{
  "user": {
    "user_id": 1,
    "name": "John Doe",
    "email": "user@example.com",
    "university": "MIT",
    "program": "Computer Science",
    "profile_picture": null
  }
}
```

---

### Update Profile
**PUT** `/users/profile` 🔒

**Request Body:**
```json
{
  "name": "John Smith",
  "university": "Stanford",
  "program": "Data Science"
}
```

**Response (200):**
```json
{
  "message": "Profile updated successfully",
  "user": {
    "user_id": 1,
    "name": "John Smith",
    "university": "Stanford",
    "program": "Data Science"
  }
}
```

---

## 📚 Course Management

### Get All Courses
**GET** `/courses` 🔒

**Response (200):**
```json
{
  "courses": [
    {
      "course_id": 1,
      "course_name": "Data Structures",
      "course_code": "CS201",
      "credit_hours": 3,
      "instructor": "Dr. Smith",
      "color": "#3B82F6",
      "created_at": "2025-11-20T10:00:00"
    }
  ],
  "count": 1
}
```

---

### Create Course
**POST** `/courses` 🔒

**Request Body:**
```json
{
  "course_name": "Data Structures",
  "course_code": "CS201",
  "credit_hours": 3,
  "instructor": "Dr. Smith",
  "color": "#3B82F6",
  "schedule": {
    "monday": ["10:00-11:30"],
    "wednesday": ["10:00-11:30"]
  }
}
```

**Response (201):**
```json
{
  "message": "Course created successfully",
  "course": {
    "course_id": 1,
    "course_name": "Data Structures",
    "course_code": "CS201",
    "credit_hours": 3,
    "instructor": "Dr. Smith"
  }
}
```

---

### Get Single Course
**GET** `/courses/:id` 🔒

**Response (200):**
```json
{
  "course": {
    "course_id": 1,
    "course_name": "Data Structures",
    "course_code": "CS201",
    "credit_hours": 3,
    "instructor": "Dr. Smith",
    "topics": "Arrays, Linked Lists, Trees, Graphs",
    "color": "#3B82F6",
    "schedule": {
      "monday": ["10:00-11:30"],
      "wednesday": ["10:00-11:30"]
    }
  }
}
```

---

### Update Course
**PUT** `/courses/:id` 🔒

**Request Body:**
```json
{
  "course_name": "Advanced Data Structures",
  "instructor": "Dr. Johnson"
}
```

**Response (200):**
```json
{
  "message": "Course updated successfully",
  "course": {
    "course_id": 1,
    "course_name": "Advanced Data Structures",
    "instructor": "Dr. Johnson"
  }
}
```

---

### Delete Course
**DELETE** `/courses/:id` 🔒

**Response (200):**
```json
{
  "message": "Course deleted successfully"
}
```

---

## ✅ Task Management

### Get All Tasks
**GET** `/tasks` 🔒

**Query Parameters:**
- `status` - Filter by status (pending, in_progress, completed)
- `priority` - Filter by priority (high, medium, low)
- `course_id` - Filter by course ID

**Example:** `/tasks?status=pending&priority=high`

**Response (200):**
```json
{
  "tasks": [
    {
      "task_id": 1,
      "title": "Assignment 1",
      "description": "Complete data structures assignment",
      "deadline": "2025-12-01T23:59:00",
      "priority": "high",
      "status": "pending",
      "course_id": 1,
      "estimated_time": 120,
      "created_at": "2025-11-20T10:00:00"
    }
  ],
  "count": 1
}
```

---

### Create Task
**POST** `/tasks` 🔒

**Request Body:**
```json
{
  "title": "Assignment 1",
  "description": "Complete data structures assignment",
  "deadline": "2025-12-01T23:59:00",
  "priority": "high",
  "course_id": 1,
  "estimated_time": 120
}
```

**Response (201):**
```json
{
  "message": "Task created successfully",
  "task": {
    "task_id": 1,
    "title": "Assignment 1",
    "deadline": "2025-12-01T23:59:00",
    "priority": "high",
    "status": "pending"
  }
}
```

---

### Mark Task Complete
**PATCH** `/tasks/:id/complete` 🔒

**Response (200):**
```json
{
  "message": "Task marked as completed",
  "task": {
    "task_id": 1,
    "status": "completed",
    "completed_at": "2025-11-28T15:30:00"
  }
}
```

---

### Get Upcoming Tasks
**GET** `/tasks/upcoming` 🔒

Get tasks due in the next 7 days.

**Response (200):**
```json
{
  "tasks": [
    {
      "task_id": 1,
      "title": "Assignment 1",
      "deadline": "2025-12-01T23:59:00",
      "days_until": 3
    }
  ],
  "count": 1
}
```

---

### Get Overdue Tasks
**GET** `/tasks/overdue` 🔒

**Response (200):**
```json
{
  "tasks": [
    {
      "task_id": 2,
      "title": "Quiz 1",
      "deadline": "2025-11-25T23:59:00",
      "days_overdue": 3
    }
  ],
  "count": 1
}
```

---

## 📅 Schedule Management

### Get Weekly Schedule
**GET** `/schedules` 🔒

**Query Parameters:**
- `week_start` - Start date (YYYY-MM-DD)

**Response (200):**
```json
{
  "schedules": [
    {
      "schedule_id": 1,
      "date": "2025-11-28",
      "start_time": "10:00:00",
      "end_time": "12:00:00",
      "block_type": "study",
      "title": "Study Data Structures",
      "task_id": 1
    }
  ],
  "count": 1
}
```

---

### Generate AI Schedule
**POST** `/schedules/generate` 🔒

**Request Body:**
```json
{
  "week_start_date": "2025-11-28",
  "preferences": {
    "study_hours_per_day": 4,
    "preferred_times": ["morning", "afternoon"]
  }
}
```

**Response (201):**
```json
{
  "message": "Schedule generated successfully",
  "schedules": [
    {
      "date": "2025-11-28",
      "start_time": "10:00:00",
      "end_time": "12:00:00",
      "block_type": "study",
      "title": "Study for Assignment 1"
    }
  ],
  "count": 15
}
```

---

## 🤖 AI Tools

### Summarize Text
**POST** `/ai/summarize` 🔒

**Request Body:**
```json
{
  "text": "Long text content to summarize...",
  "length": "moderate"
}
```

**Response (200):**
```json
{
  "summary": "Concise summary of the text...",
  "original_length": 5000,
  "summary_length": 500
}
```

---

### Generate Quiz
**POST** `/ai/generate-quiz` 🔒

**Request Body:**
```json
{
  "content": "Study material content...",
  "num_questions": 10,
  "difficulty": "medium"
}
```

**Response (200):**
```json
{
  "quiz": {
    "questions": [
      {
        "question": "What is a binary tree?",
        "options": ["A", "B", "C", "D"],
        "correct_answer": "A",
        "explanation": "..."
      }
    ]
  },
  "count": 10
}
```

---

### Create Flashcards
**POST** `/ai/create-flashcards` 🔒

**Request Body:**
```json
{
  "content": "Study notes content...",
  "num_cards": 20
}
```

**Response (200):**
```json
{
  "flashcards": [
    {
      "question": "What is recursion?",
      "answer": "A function that calls itself..."
    }
  ],
  "count": 20
}
```

---

### Recommend Materials
**POST** `/ai/recommend-materials` 🔒

**Request Body:**
```json
{
  "topic": "Data Structures",
  "type": "video"
}
```

**Response (200):**
```json
{
  "recommendations": [
    {
      "title": "Data Structures Tutorial",
      "url": "https://youtube.com/...",
      "thumbnail": "https://...",
      "duration": "15:30",
      "views": "1.2M"
    }
  ],
  "count": 10
}
```

---

## 📊 Analytics & Progress

### Get Dashboard Stats
**GET** `/progress/dashboard` 🔒

**Response (200):**
```json
{
  "stats": {
    "total_courses": 5,
    "total_tasks": 20,
    "completed_tasks": 15,
    "pending_tasks": 5,
    "completion_rate": 75.0,
    "study_hours_this_week": 18.5,
    "overdue_tasks": 2
  }
}
```

---

### Get Analytics
**GET** `/progress/analytics` 🔒

**Response (200):**
```json
{
  "analytics": {
    "completion_rate": 75.0,
    "study_hours_by_course": {
      "Data Structures": 10.5,
      "Algorithms": 8.0
    },
    "weekly_trend": [
      {"week": "Week 1", "hours": 15},
      {"week": "Week 2", "hours": 18.5}
    ]
  }
}
```

---

### Get Falling Behind Prediction
**GET** `/progress/prediction` 🔒

**Response (200):**
```json
{
  "is_falling_behind": true,
  "severity": "medium",
  "reasons": [
    "Completion rate below 50%",
    "5+ upcoming deadlines"
  ],
  "suggestions": [
    "Increase study hours",
    "Prioritize high-priority tasks"
  ]
}
```

---

## 🔔 Notifications

### Get Notifications
**GET** `/notifications` 🔒

**Query Parameters:**
- `unread_only` - true/false
- `limit` - Number of notifications (default: 50)

**Response (200):**
```json
{
  "notifications": [
    {
      "notification_id": 1,
      "type": "deadline_reminder",
      "title": "Deadline Reminder",
      "message": "Assignment due in 24 hours",
      "is_read": false,
      "created_at": "2025-11-28T10:00:00"
    }
  ],
  "count": 1,
  "unread_count": 1
}
```

---

### Mark Notification as Read
**PATCH** `/notifications/:id/read` 🔒

**Response (200):**
```json
{
  "message": "Notification marked as read"
}
```

---

### Mark All as Read
**PATCH** `/notifications/mark-all-read` 🔒

**Response (200):**
```json
{
  "message": "5 notifications marked as read",
  "count": 5
}
```

---

## 👥 Group Collaboration

### Get User's Groups
**GET** `/groups` 🔒

**Response (200):**
```json
{
  "groups": [
    {
      "group_id": 1,
      "group_name": "Data Structures Study Group",
      "description": "Weekly study sessions",
      "member_count": 5,
      "user_role": "admin"
    }
  ],
  "count": 1
}
```

---

### Create Group
**POST** `/groups` 🔒

**Request Body:**
```json
{
  "group_name": "Python Study Group",
  "description": "Learning Python together",
  "is_private": false,
  "max_members": 20
}
```

**Response (201):**
```json
{
  "message": "Group created successfully",
  "group": {
    "group_id": 1,
    "group_name": "Python Study Group",
    "admin_user_id": 1,
    "member_count": 1
  }
}
```

---

### Join Group
**POST** `/groups/:id/join` 🔒

**Response (200):**
```json
{
  "message": "Successfully joined the group"
}
```

---

### Leave Group
**POST** `/groups/:id/leave` 🔒

**Response (200):**
```json
{
  "message": "Successfully left the group"
}
```

---

## ⚠️ Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing or invalid token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Resource already exists |
| 500 | Internal Server Error |

### Error Response Format
```json
{
  "error": "Error Type",
  "message": "Detailed error message"
}
```

---

## 📝 Notes

- 🔒 indicates protected endpoint (requires authentication)
- All timestamps are in ISO 8601 format (UTC)
- All dates should be in YYYY-MM-DD format
- Maximum file upload size: 10MB
- Rate limiting: 100 requests per minute per user

---

**Last Updated:** November 28, 2025  
**API Version:** 1.0.0
