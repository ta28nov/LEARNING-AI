# API Documentation

## Overview

The AI Learning Application API provides comprehensive endpoints for managing courses, quizzes, chat sessions, file uploads, and user progress. All endpoints require authentication except for the root and health check endpoints.

## Base URL

```
http://localhost:8000
```

## Authentication

The API uses JWT (JSON Web Token) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Response Format

All API responses follow a consistent format:

### Success Response
```json
{
  "data": <response_data>,
  "message": "Success message"
}
```

### Error Response
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

## Endpoints

### Authentication

#### Register User
```http
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "id": "64f1a2b3c4d5e6f7g8h9i0j1",
  "email": "user@example.com",
  "name": "John Doe",
  "avatar": null,
  "role": "student",
  "is_active": true,
  "created_at": "2023-09-01T10:00:00Z",
  "updated_at": "2023-09-01T10:00:00Z"
}
```

#### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /auth/me
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "64f1a2b3c4d5e6f7g8h9i0j1",
  "email": "user@example.com",
  "name": "John Doe",
  "avatar": null,
  "role": "student",
  "is_active": true,
  "created_at": "2023-09-01T10:00:00Z",
  "updated_at": "2023-09-01T10:00:00Z"
}
```

### Courses

#### Create Course
```http
POST /courses/
```

**Request Body:**
```json
{
  "title": "Introduction to Python",
  "description": "Learn Python programming from scratch",
  "outline": "1. Variables and Data Types\n2. Control Structures\n3. Functions",
  "source": "AI Generated",
  "level": "beginner",
  "tags": ["python", "programming", "beginner"]
}
```

**Response:**
```json
{
  "id": "64f1a2b3c4d5e6f7g8h9i0j2",
  "owner_id": "64f1a2b3c4d5e6f7g8h9i0j1",
  "title": "Introduction to Python",
  "description": "Learn Python programming from scratch",
  "outline": "1. Variables and Data Types\n2. Control Structures\n3. Functions",
  "source": "AI Generated",
  "level": "beginner",
  "tags": ["python", "programming", "beginner"],
  "created_at": "2023-09-01T10:00:00Z",
  "updated_at": "2023-09-01T10:00:00Z"
}
```

#### Create Course from Prompt
```http
POST /courses/from-prompt
```

**Request Body:**
```json
{
  "topic": "Machine Learning Fundamentals",
  "level": "intermediate"
}
```

**Response:**
```json
{
  "id": "64f1a2b3c4d5e6f7g8h9i0j3",
  "owner_id": "64f1a2b3c4d5e6f7g8h9i0j1",
  "title": "AI Generated Course: Machine Learning Fundamentals",
  "description": "An AI-generated course about Machine Learning Fundamentals",
  "outline": "Course Outline:\n\n1. Introduction to Machine Learning\n   - What is ML?\n   - Types of ML\n   - Applications\n\n2. Data Preprocessing\n   - Data cleaning\n   - Feature engineering\n   - Data splitting\n\n...",
  "source": "AI Generated",
  "level": "intermediate",
  "tags": ["machine learning fundamentals", "ai-generated"],
  "created_at": "2023-09-01T10:00:00Z",
  "updated_at": "2023-09-01T10:00:00Z"
}
```

#### Get Courses
```http
GET /courses/?skip=0&limit=10
```

**Response:**
```json
[
  {
    "id": "64f1a2b3c4d5e6f7g8h9i0j2",
    "owner_id": "64f1a2b3c4d5e6f7g8h9i0j1",
    "title": "Introduction to Python",
    "description": "Learn Python programming from scratch",
    "outline": "1. Variables and Data Types\n2. Control Structures\n3. Functions",
    "source": "AI Generated",
    "level": "beginner",
    "tags": ["python", "programming", "beginner"],
    "created_at": "2023-09-01T10:00:00Z",
    "updated_at": "2023-09-01T10:00:00Z"
  }
]
```

#### Get Course by ID
```http
GET /courses/{course_id}
```

**Response:**
```json
{
  "id": "64f1a2b3c4d5e6f7g8h9i0j2",
  "owner_id": "64f1a2b3c4d5e6f7g8h9i0j1",
  "title": "Introduction to Python",
  "description": "Learn Python programming from scratch",
  "outline": "1. Variables and Data Types\n2. Control Structures\n3. Functions",
  "source": "AI Generated",
  "level": "beginner",
  "tags": ["python", "programming", "beginner"],
  "created_at": "2023-09-01T10:00:00Z",
  "updated_at": "2023-09-01T10:00:00Z"
}
```

#### Create Chapter
```http
POST /courses/{course_id}/chapters
```

**Request Body:**
```json
{
  "title": "Variables and Data Types",
  "content": "In Python, variables are used to store data...",
  "order": 1
}
```

**Response:**
```json
{
  "id": "64f1a2b3c4d5e6f7g8h9i0j4",
  "course_id": "64f1a2b3c4d5e6f7g8h9i0j2",
  "title": "Variables and Data Types",
  "content": "In Python, variables are used to store data...",
  "order": 1,
  "created_at": "2023-09-01T10:00:00Z",
  "updated_at": "2023-09-01T10:00:00Z"
}
```

### File Uploads

#### Upload File
```http
POST /uploads/
```

**Request:** Multipart form data
- `file`: File to upload (PDF, DOCX, TXT)

**Response:**
```json
{
  "id": "64f1a2b3c4d5e6f7g8h9i0j5",
  "user_id": "64f1a2b3c4d5e6f7g8h9i0j1",
  "filename": "document.pdf",
  "file_type": "pdf",
  "file_path": "/uploads/64f1a2b3c4d5e6f7g8h9i0j5.pdf",
  "file_size": 1024000,
  "status": "completed",
  "extracted_text": "This is the extracted text from the document...",
  "metadata": null,
  "created_at": "2023-09-01T10:00:00Z"
}
```

#### Get Uploads
```http
GET /uploads/?skip=0&limit=10
```

**Response:**
```json
[
  {
    "id": "64f1a2b3c4d5e6f7g8h9i0j5",
    "user_id": "64f1a2b3c4d5e6f7g8h9i0j1",
    "filename": "document.pdf",
    "file_type": "pdf",
    "file_path": "/uploads/64f1a2b3c4d5e6f7g8h9i0j5.pdf",
    "file_size": 1024000,
    "status": "completed",
    "extracted_text": "This is the extracted text from the document...",
    "metadata": null,
    "created_at": "2023-09-01T10:00:00Z"
  }
]
```

### Quiz System

#### Create Quiz from Course
```http
POST /quiz/from-course/{course_id}
```

**Request Body:**
```json
{
  "title": "Python Basics Quiz",
  "num_questions": 5
}
```

**Response:**
```json
{
  "id": "64f1a2b3c4d5e6f7g8h9i0j6",
  "course_id": "64f1a2b3c4d5e6f7g8h9i0j2",
  "chapter_id": null,
  "title": "Python Basics Quiz",
  "prompt": "AI-generated quiz from course: Introduction to Python",
  "created_at": "2023-09-01T10:00:00Z"
}
```

#### Get Quiz Questions
```http
GET /quiz/{quiz_id}/questions
```

**Response:**
```json
[
  {
    "id": "64f1a2b3c4d5e6f7g8h9i0j7",
    "quiz_id": "64f1a2b3c4d5e6f7g8h9i0j6",
    "question": "What is the correct way to declare a variable in Python?",
    "options": [
      "var name = 'John'",
      "name = 'John'",
      "string name = 'John'",
      "name := 'John'"
    ],
    "correct_answer": 1,
    "explanation": "In Python, variables are declared by simply assigning a value to a name.",
    "order": 1
  }
]
```

#### Submit Quiz
```http
POST /quiz/{quiz_id}/submit
```

**Request Body:**
```json
{
  "quiz_id": "64f1a2b3c4d5e6f7g8h9i0j6",
  "answers": [
    {
      "question_id": "64f1a2b3c4d5e6f7g8h9i0j7",
      "answer": 1
    }
  ]
}
```

**Response:**
```json
{
  "quiz_id": "64f1a2b3c4d5e6f7g8h9i0j6",
  "user_id": "64f1a2b3c4d5e6f7g8h9i0j1",
  "score": 100.0,
  "total_questions": 1,
  "correct_answers": 1,
  "answers": [
    {
      "question_id": "64f1a2b3c4d5e6f7g8h9i0j7",
      "question": "What is the correct way to declare a variable in Python?",
      "user_answer": 1,
      "correct_answer": 1,
      "is_correct": true,
      "explanation": "In Python, variables are declared by simply assigning a value to a name."
    }
  ],
  "taken_at": "2023-09-01T10:00:00Z"
}
```

### Chat System

#### Create Chat Session
```http
POST /chat/sessions
```

**Request Body:**
```json
{
  "course_id": "64f1a2b3c4d5e6f7g8h9i0j2",
  "title": "Python Learning Chat",
  "mode": "hybrid"
}
```

**Response:**
```json
{
  "id": "64f1a2b3c4d5e6f7g8h9i0j8",
  "user_id": "64f1a2b3c4d5e6f7g8h9i0j1",
  "course_id": "64f1a2b3c4d5e6f7g8h9i0j2",
  "upload_id": null,
  "title": "Python Learning Chat",
  "mode": "hybrid",
  "status": "active",
  "created_at": "2023-09-01T10:00:00Z",
  "updated_at": "2023-09-01T10:00:00Z"
}
```

#### Send Message
```http
POST /chat/sessions/{session_id}/messages
```

**Request Body:**
```json
{
  "message": "What is a variable in Python?"
}
```

**Response:**
```json
{
  "message": "What is a variable in Python?",
  "answer": "A variable in Python is a container that stores data values. Unlike other programming languages, Python doesn't require you to declare variables with a specific type. You can simply assign a value to a variable name, and Python will automatically determine the data type...",
  "metadata": null
}
```

#### Freestyle Chat
```http
POST /chat/freestyle
```

**Request Body:**
```json
{
  "message": "Explain machine learning in simple terms",
  "mode": "hybrid"
}
```

**Response:**
```json
{
  "message": "Explain machine learning in simple terms",
  "answer": "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed for every task...",
  "metadata": null
}
```

### Dashboard

#### Get Dashboard Stats
```http
GET /dashboard/stats
```

**Response:**
```json
{
  "total_courses": 5,
  "completed_courses": 2,
  "total_quizzes": 15,
  "total_time_spent": 120,
  "average_score": 85.5,
  "recent_activity": [
    {
      "type": "quiz",
      "title": "Quiz completed",
      "score": 90.0,
      "date": "2023-09-01T10:00:00Z"
    }
  ],
  "progress_by_course": [
    {
      "course_id": "64f1a2b3c4d5e6f7g8h9i0j2",
      "course_title": "Introduction to Python",
      "progress": 75.0
    }
  ],
  "weekly_progress": [
    {
      "week": "Week 1",
      "quizzes_taken": 3,
      "average_score": 85.0
    }
  ]
}
```

#### Update Progress
```http
POST /dashboard/progress
```

**Request Body:**
```json
{
  "course_id": "64f1a2b3c4d5e6f7g8h9i0j2",
  "chapter_id": "64f1a2b3c4d5e6f7g8h9i0j4",
  "status": "completed",
  "progress": 100.0,
  "time_spent": 30
}
```

**Response:**
```json
{
  "message": "Progress updated successfully"
}
```

#### Get Learning Recommendations
```http
GET /dashboard/recommendations
```

**Response:**
```json
[
  {
    "type": "continue_course",
    "title": "Continue learning: Introduction to Python",
    "description": "You're 75.0% through this course",
    "course_id": "64f1a2b3c4d5e6f7g8h9i0j2",
    "priority": "high"
  },
  {
    "type": "review_quizzes",
    "title": "Review recent quiz performance",
    "description": "You scored below 70% on 2 recent quizzes",
    "priority": "high"
  }
]
```

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Invalid or missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 413 | Payload Too Large - File too large |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

## Rate Limiting

The API implements rate limiting to prevent abuse. Default limits:
- 100 requests per minute per user
- 10 file uploads per minute per user

## File Upload Limits

- Maximum file size: 10MB
- Supported formats: PDF, DOCX, TXT
- Maximum files per user: 100

## WebSocket Support

Real-time chat functionality is planned for future releases.

## SDKs and Libraries

### Python
```python
import requests

# Set up authentication
headers = {
    'Authorization': 'Bearer your-jwt-token',
    'Content-Type': 'application/json'
}

# Create a course
response = requests.post(
    'http://localhost:8000/courses/',
    json={
        'title': 'My Course',
        'description': 'Course description',
        'level': 'beginner'
    },
    headers=headers
)
```

### JavaScript
```javascript
// Set up authentication
const headers = {
    'Authorization': 'Bearer your-jwt-token',
    'Content-Type': 'application/json'
};

// Create a course
const response = await fetch('http://localhost:8000/courses/', {
    method: 'POST',
    headers: headers,
    body: JSON.stringify({
        title: 'My Course',
        description: 'Course description',
        level: 'beginner'
    })
});
```

### Student Endpoints

#### Enroll in Course
```http
POST /student/courses/{course_id}/enroll
```

**Description:** Enroll current student in a public course.

**Headers:**
```
Authorization: Bearer <student-token>
```

**Response:**
```json
{
  "id": "64f1a2b3c4d5e6f7g8h9i0j5",
  "student_id": "64f1a2b3c4d5e6f7g8h9i0j1",
  "course_id": "64f1a2b3c4d5e6f7g8h9i0j2",
  "status": "active",
  "progress": 0.0,
  "enrolled_at": "2023-09-01T10:00:00Z",
  "last_accessed": "2023-09-01T10:00:00Z"
}
```

**Error Responses:**
- `400`: Already enrolled or course not available
- `404`: Course not found
- `403`: Only students can enroll

#### Unenroll from Course
```http
DELETE /student/courses/{course_id}/enroll
```

**Description:** Unenroll current student from a course.

**Headers:**
```
Authorization: Bearer <student-token>
```

**Response:**
```json
{
  "message": "Successfully unenrolled from course"
}
```

**Error Responses:**
- `404`: Not enrolled in this course

#### Get Enrolled Courses
```http
GET /student/enrolled-courses?status=active&skip=0&limit=10
```

**Description:** Get list of courses the student is enrolled in.

**Query Parameters:**
- `status` (optional): Filter by enrollment status (active, completed, dropped)
- `skip` (optional): Pagination offset (default: 0)
- `limit` (optional): Results per page (default: 10)

**Headers:**
```
Authorization: Bearer <student-token>
```

**Response:**
```json
[
  {
    "id": "64f1a2b3c4d5e6f7g8h9i0j5",
    "student_id": "64f1a2b3c4d5e6f7g8h9i0j1",
    "course_id": "64f1a2b3c4d5e6f7g8h9i0j2",
    "status": "active",
    "progress": 45.5,
    "enrolled_at": "2023-09-01T10:00:00Z",
    "last_accessed": "2023-09-02T14:30:00Z",
    "course_details": {
      "title": "Introduction to Python",
      "description": "Learn Python programming from scratch",
      "level": "beginner",
      "tags": ["python", "programming"]
    }
  }
]
```

#### Get Student Dashboard
```http
GET /student/dashboard
```

**Description:** Get student dashboard statistics and recent activity.

**Headers:**
```
Authorization: Bearer <student-token>
```

**Response:**
```json
{
  "total_enrollments": 5,
  "active_enrollments": 3,
  "completed_courses": 2,
  "total_progress": 62.5,
  "recent_courses": [
    {
      "id": "64f1a2b3c4d5e6f7g8h9i0j5",
      "course_id": "64f1a2b3c4d5e6f7g8h9i0j2",
      "course_title": "Introduction to Python",
      "progress": 45.5,
      "last_accessed": "2023-09-02T14:30:00Z",
      "status": "active"
    }
  ],
  "achievements": {
    "courses_completed": 2,
    "total_time_spent": 1250
  }
}
```

### Instructor Endpoints

#### Get Instructor Courses
```http
GET /instructor/courses?skip=0&limit=10
```

**Description:** Get list of courses created by the instructor.

**Query Parameters:**
- `skip` (optional): Pagination offset (default: 0)
- `limit` (optional): Results per page (default: 10)

**Headers:**
```
Authorization: Bearer <instructor-token>
```

**Response:**
```json
[
  {
    "id": "64f1a2b3c4d5e6f7g8h9i0j2",
    "owner_id": "64f1a2b3c4d5e6f7g8h9i0j1",
    "title": "Introduction to Python",
    "description": "Learn Python programming from scratch",
    "visibility": "public",
    "is_approved": true,
    "enrollment_count": 15,
    "level": "beginner",
    "created_at": "2023-09-01T10:00:00Z"
  }
]
```

#### Get Course Students
```http
GET /instructor/courses/{course_id}/students
```

**Description:** Get list of students enrolled in instructor's course.

**Headers:**
```
Authorization: Bearer <instructor-token>
```

**Response:**
```json
[
  {
    "id": "64f1a2b3c4d5e6f7g8h9i0j5",
    "student_id": "64f1a2b3c4d5e6f7g8h9i0j3",
    "student_name": "Jane Student",
    "student_email": "student@example.com",
    "status": "active",
    "progress": 45.5,
    "enrolled_at": "2023-09-01T10:00:00Z",
    "last_accessed": "2023-09-02T14:30:00Z"
  }
]
```

**Error Responses:**
- `403`: Not the course owner
- `404`: Course not found

#### Get Course Analytics
```http
GET /instructor/courses/{course_id}/analytics
```

**Description:** Get detailed analytics for instructor's course.

**Headers:**
```
Authorization: Bearer <instructor-token>
```

**Response:**
```json
{
  "course_id": "64f1a2b3c4d5e6f7g8h9i0j2",
  "course_title": "Introduction to Python",
  "total_students": 15,
  "active_students": 12,
  "completed_students": 3,
  "average_progress": 62.8,
  "completion_rate": 20.0,
  "average_time_spent": 450,
  "enrollment_trend": [
    {"date": "2023-09-01", "count": 5},
    {"date": "2023-09-02", "count": 8},
    {"date": "2023-09-03", "count": 2}
  ],
  "chapter_completion": [
    {"chapter_id": "...", "completion_rate": 85.0},
    {"chapter_id": "...", "completion_rate": 60.0}
  ]
}
```

#### Get All Students (Instructor View)
```http
GET /instructor/all-students
```

**Description:** Get all students enrolled in any of instructor's courses.

**Headers:**
```
Authorization: Bearer <instructor-token>
```

**Response:**
```json
[
  {
    "student_id": "64f1a2b3c4d5e6f7g8h9i0j3",
    "student_name": "Jane Student",
    "student_email": "student@example.com",
    "enrolled_courses_count": 2,
    "courses": [
      {
        "course_id": "64f1a2b3c4d5e6f7g8h9i0j2",
        "course_title": "Introduction to Python",
        "progress": 45.5,
        "status": "active"
      }
    ]
  }
]
```

#### Get Instructor Dashboard
```http
GET /instructor/dashboard
```

**Description:** Get instructor dashboard with overall statistics.

**Headers:**
```
Authorization: Bearer <instructor-token>
```

**Response:**
```json
{
  "total_courses": 8,
  "published_courses": 6,
  "draft_courses": 2,
  "total_students": 45,
  "total_enrollments": 120,
  "average_course_rating": 4.5,
  "recent_enrollments": [
    {
      "student_name": "Jane Student",
      "course_title": "Introduction to Python",
      "enrolled_at": "2023-09-02T14:30:00Z"
    }
  ],
  "top_courses": [
    {
      "course_id": "64f1a2b3c4d5e6f7g8h9i0j2",
      "title": "Introduction to Python",
      "enrollment_count": 35,
      "average_progress": 65.5
    }
  ]
}
```

## Course Visibility

Courses can have three visibility levels:

- **public**: Available to all users, can be enrolled by any student
- **private**: Only visible to owner and explicitly shared users
- **draft**: Work in progress, not visible to students

### Enrollment Rules

1. Students can only enroll in **public** courses that are **approved**
2. Instructors can see their own courses regardless of visibility
3. Admins can see all courses
4. Enrollment count updates automatically on enroll/unenroll

## Testing

Use the interactive API documentation at `/docs` to test endpoints directly in your browser.

## Support

For API support and questions:
- Check the interactive documentation at `/docs`
- Review the error messages and status codes
- Ensure proper authentication headers are included
- Verify request body format matches the schemas
