# AI Learning Application Backend

A comprehensive AI-powered learning platform built with FastAPI, MongoDB, and Google GenAI. This application provides intelligent course management, AI tutoring, quiz generation, and progress tracking.

## Features

### 🎯 Core Features
- **User Authentication**: JWT-based authentication with user registration and login
- **Course Management**: Create, manage, and organize courses with chapters
- **Enrollment System**: Student enrollment with instructor dashboard and analytics
- **AI-Powered Content Generation**: Generate courses from prompts using Google GenAI
- **File Upload & Processing**: Upload PDF, DOCX, and text files with automatic text extraction
- **Intelligent Chat**: AI tutor with strict and hybrid modes for contextual learning
- **Quiz System**: Generate and take quizzes with AI-powered question creation
- **Progress Tracking**: Comprehensive dashboard with learning analytics
- **Vector Search**: Semantic search through course content and uploads

### 🤖 AI Capabilities
- **Course Outline Generation**: Create structured courses from topic prompts
- **Text Extraction & Processing**: Extract and clean text from uploaded documents
- **Quiz Question Generation**: Generate multiple-choice questions from content
- **Flashcard Creation**: Create study flashcards from course material
- **Content Summarization**: Generate summaries of course chapters
- **Contextual Q&A**: Answer questions based on course content or general knowledge

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database with Beanie ODM
- **Google GenAI**: AI model integration for content generation
- **JWT**: Secure authentication and authorization
- **Pydantic**: Data validation and serialization

### Database
- **MongoDB Atlas**: Cloud database with vector search capabilities
- **Beanie ODM**: Async MongoDB object-document mapper
- **Vector Search**: Semantic search through course content

### File Processing
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX document processing
- **python-magic**: File type detection
- **aiofiles**: Async file operations

## Project Structure

```
app/
├── __init__.py
├── main.py                 # FastAPI application entry point
├── config.py              # Application configuration
├── database.py            # Database connection and initialization
├── auth.py                # Authentication utilities
├── models/                # Database models
│   ├── __init__.py
│   ├── user.py           # User model
│   ├── course.py         # Course and Chapter models
│   ├── enrollment.py     # Enrollment model
│   ├── upload.py         # Upload model
│   ├── quiz.py           # Quiz, QuizQuestion, QuizHistory models
│   ├── chat.py           # ChatSession, ChatMessage models
│   └── dashboard.py      # DashboardProgress model
├── schemas/               # Pydantic schemas
│   ├── __init__.py
│   ├── auth.py           # Authentication schemas
│   ├── course.py         # Course schemas
│   ├── enrollment.py     # Enrollment schemas
│   ├── upload.py         # Upload schemas
│   ├── quiz.py           # Quiz schemas
│   ├── chat.py           # Chat schemas
│   └── dashboard.py      # Dashboard schemas
├── services/              # Business logic services
│   ├── __init__.py
│   ├── genai_service.py  # Google GenAI integration
│   ├── file_service.py   # File processing service
│   └── vector_service.py # Vector search service
└── routers/               # API endpoints
    ├── __init__.py
    ├── auth.py           # Authentication endpoints
    ├── courses.py        # Course management endpoints
    ├── student.py        # Student enrollment endpoints
    ├── instructor.py     # Instructor management endpoints
    ├── uploads.py        # File upload endpoints
    ├── quiz.py           # Quiz endpoints
    ├── chat.py           # Chat endpoints
    └── dashboard.py      # Dashboard endpoints
```

## Installation

### Prerequisites
- Python 3.11+
- MongoDB (local or Atlas)
- Google API key for GenAI

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-learning-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` file with your configuration:
   ```env
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=ai_learning_app
   SECRET_KEY=your-secret-key-here
   GOOGLE_API_KEY=your-google-api-key-here
   DEBUG=True
   ```

5. **Run the application**
   ```bash
   python -m app.main
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Documentation

Once the application is running, you can access:

- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## API Endpoints

### Authentication (`/auth`)
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info
- `PUT /auth/me` - Update user profile
- `POST /auth/change-password` - Change password

### Courses (`/courses`)
- `POST /courses/` - Create new course
- `POST /courses/from-prompt` - Create course from AI prompt
- `GET /courses/` - Get user's courses
- `GET /courses/public` - Get public courses
- `GET /courses/{course_id}` - Get specific course
- `PUT /courses/{course_id}` - Update course
- `DELETE /courses/{course_id}` - Delete course
- `POST /courses/{course_id}/chapters` - Create chapter
- `GET /courses/{course_id}/chapters` - Get course chapters
- `GET /courses/{course_id}/chapters/{chapter_id}` - Get specific chapter
- `PUT /courses/{course_id}/chapters/{chapter_id}` - Update chapter
- `DELETE /courses/{course_id}/chapters/{chapter_id}` - Delete chapter

### Uploads (`/uploads`)
- `POST /uploads/` - Upload file
- `GET /uploads/` - Get user's uploads
- `GET /uploads/{upload_id}` - Get specific upload
- `DELETE /uploads/{upload_id}` - Delete upload
- `POST /uploads/{upload_id}/reprocess` - Reprocess upload

### Quiz (`/quiz`)
- `POST /quiz/` - Create quiz
- `POST /quiz/from-course/{course_id}` - Create quiz from course
- `POST /quiz/from-upload/{upload_id}` - Create quiz from upload
- `GET /quiz/` - Get quizzes
- `GET /quiz/{quiz_id}` - Get specific quiz
- `GET /quiz/{quiz_id}/questions` - Get quiz questions
- `POST /quiz/{quiz_id}/submit` - Submit quiz answers
- `GET /quiz/history` - Get quiz history
- `GET /quiz/history/{history_id}` - Get quiz history detail

### Chat (`/chat`)
- `POST /chat/sessions` - Create chat session
- `GET /chat/sessions` - Get chat sessions
- `GET /chat/sessions/{session_id}` - Get specific session
- `GET /chat/sessions/{session_id}/messages` - Get session messages
- `POST /chat/sessions/{session_id}/messages` - Send message
- `POST /chat/freestyle` - Freestyle chat
- `POST /chat/sessions/{session_id}/save-as-course` - Save chat as course
- `DELETE /chat/sessions/{session_id}` - Delete chat session

### Dashboard (`/dashboard`)
- `GET /dashboard/stats` - Get dashboard statistics
- `GET /dashboard/progress` - Get course progress
- `POST /dashboard/progress` - Update progress
- `GET /dashboard/progress/{course_id}` - Get course progress detail
- `GET /dashboard/recommendations` - Get learning recommendations

## Database Schema

### User
- `id`: ObjectId (Primary Key)
- `email`: EmailStr (Unique)
- `password_hash`: str
- `name`: str
- `avatar`: Optional[str]
- `role`: UserRole (student/instructor/admin)
- `is_active`: bool
- `created_at`: datetime
- `updated_at`: datetime

### Course
- `id`: ObjectId (Primary Key)
- `owner_id`: ObjectId (Foreign Key to User)
- `title`: str
- `description`: str
- `outline`: Optional[str]
- `source`: Optional[str]
- `level`: CourseLevel (beginner/intermediate/advanced)
- `tags`: List[str]
- `created_at`: datetime
- `updated_at`: datetime

### Chapter
- `id`: ObjectId (Primary Key)
- `course_id`: ObjectId (Foreign Key to Course)
- `title`: str
- `content`: str
- `order`: int
- `created_at`: datetime
- `updated_at`: datetime

### Upload
- `id`: ObjectId (Primary Key)
- `user_id`: ObjectId (Foreign Key to User)
- `filename`: str
- `file_type`: FileType (pdf/docx/txt/video/image)
- `file_path`: str
- `file_size`: int
- `status`: UploadStatus (pending/processing/completed/failed)
- `extracted_text`: Optional[str]
- `metadata`: Optional[dict]
- `created_at`: datetime

### Quiz
- `id`: ObjectId (Primary Key)
- `course_id`: ObjectId (Foreign Key to Course)
- `chapter_id`: Optional[ObjectId] (Foreign Key to Chapter)
- `title`: str
- `prompt`: str
- `created_at`: datetime

### QuizQuestion
- `id`: ObjectId (Primary Key)
- `quiz_id`: ObjectId (Foreign Key to Quiz)
- `question`: str
- `options`: List[str]
- `correct_answer`: int
- `explanation`: Optional[str]
- `order`: int

### QuizHistory
- `id`: ObjectId (Primary Key)
- `quiz_id`: ObjectId (Foreign Key to Quiz)
- `user_id`: ObjectId (Foreign Key to User)
- `score`: float
- `total_questions`: int
- `correct_answers`: int
- `answers`: List[dict]
- `taken_at`: datetime

### ChatSession
- `id`: ObjectId (Primary Key)
- `user_id`: ObjectId (Foreign Key to User)
- `course_id`: Optional[ObjectId] (Foreign Key to Course)
- `upload_id`: Optional[ObjectId] (Foreign Key to Upload)
- `title`: str
- `mode`: ChatMode (strict/hybrid)
- `status`: ChatStatus (active/archived/deleted)
- `created_at`: datetime
- `updated_at`: datetime

### ChatMessage
- `id`: ObjectId (Primary Key)
- `session_id`: ObjectId (Foreign Key to ChatSession)
- `sender`: str (user/ai)
- `message`: str
- `answer`: Optional[str]
- `metadata`: Optional[dict]
- `created_at`: datetime

### DashboardProgress
- `id`: ObjectId (Primary Key)
- `user_id`: ObjectId (Foreign Key to User)
- `course_id`: ObjectId (Foreign Key to Course)
- `chapter_id`: Optional[ObjectId] (Foreign Key to Chapter)
- `status`: ProgressStatus (not_started/in_progress/completed)
- `progress`: float (0.0-100.0)
- `time_spent`: int (minutes)
- `last_accessed`: datetime
- `created_at`: datetime
- `updated_at`: datetime

## AI Features

### Google GenAI Integration
The application uses Google's Gemini Pro model for various AI-powered features:

1. **Course Outline Generation**: Creates structured course outlines from topic prompts
2. **Text Processing**: Extracts and cleans text from uploaded documents
3. **Quiz Generation**: Creates multiple-choice questions from content
4. **Flashcard Creation**: Generates study flashcards
5. **Content Summarization**: Creates summaries of course material
6. **Contextual Q&A**: Answers questions based on course content

### Chat Modes
- **Strict Mode**: Only answers based on uploaded/course content
- **Hybrid Mode**: Combines course content with general AI knowledge

### Vector Search
- Semantic search through course content and uploads
- Context-aware responses based on relevant content
- MongoDB Atlas Vector Search integration

## File Processing

### Supported Formats
- **PDF**: Text extraction using PyPDF2
- **DOCX**: Document processing using python-docx
- **TXT**: Direct text reading
- **Video/Image**: Metadata extraction (content processing planned)

### Processing Pipeline
1. File upload and validation
2. Text extraction based on file type
3. AI-powered text cleaning and processing
4. Vector indexing for semantic search
5. Content integration with course system

## Security

### Authentication
- JWT-based authentication
- Password hashing with bcrypt
- Token expiration and refresh
- User role-based access control

### File Security
- File type validation
- Size limits and restrictions
- Secure file storage
- User isolation

### API Security
- CORS configuration
- Input validation with Pydantic
- Error handling and logging
- Rate limiting (recommended for production)

## Deployment

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
- `MONGODB_URL`: MongoDB connection string
- `DATABASE_NAME`: Database name
- `SECRET_KEY`: JWT secret key
- `GOOGLE_API_KEY`: Google GenAI API key
- `DEBUG`: Debug mode flag
- `ALLOWED_ORIGINS`: CORS allowed origins

### Production Considerations
- Use environment variables for configuration
- Set up proper logging
- Implement rate limiting
- Use HTTPS in production
- Set up monitoring and health checks
- Configure database backups
- Use a reverse proxy (nginx)

## Development

### Code Quality
- **Black**: Code formatting
- **isort**: Import sorting
- **mypy**: Type checking
- **pytest**: Testing framework

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
isort app/
```

### Type Checking
```bash
mypy app/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the code examples in the routers

## Roadmap

### Planned Features
- [ ] Real-time chat with WebSocket
- [ ] Advanced analytics and reporting
- [ ] Multi-language support
- [ ] Mobile app integration
- [ ] Advanced file processing (video transcription)
- [ ] Collaborative learning features
- [ ] Advanced AI models integration
- [ ] Performance optimization
- [ ] Enhanced security features
