# Kiến Trúc Hệ Thống - Nền Tảng Học Tập AI

Tài liệu này mô tả chi tiết kiến trúc tổng thể của Nền Tảng Học Tập AI, bao gồm backend, frontend và cách chúng tương tác với nhau.

## Tổng Quan Kiến Trúc

### Kiến Trúc Tổng Thể

```
┌─────────────────┐    HTTP/HTTPS    ┌─────────────────┐
│                 │ ◄─────────────► │                 │
│   Frontend      │     REST API     │   Backend API   │
│   (React)       │                  │   (FastAPI)     │
│                 │                  │                 │
└─────────────────┘                  └─────────────────┘
                                              │
                                              │ MongoDB Driver
                                              ▼
                                    ┌─────────────────┐
                                    │                 │
                                    │   MongoDB       │
                                    │   + Vector      │
                                    │   Search        │
                                    │                 │
                                    └─────────────────┘
                                              │
                                              │ API Calls
                                              ▼
                                    ┌─────────────────┐
                                    │                 │
                                    │  Google GenAI   │
                                    │  (Gemini Pro)   │
                                    │                 │
                                    └─────────────────┘
```

### Công Nghệ Stack

**Frontend:**
- React 18 với TypeScript
- Tailwind CSS cho styling
- Zustand cho state management
- Framer Motion cho animations
- React i18next cho đa ngôn ngữ

**Backend:**
- FastAPI với Python 3.11+
- Beanie ODM cho MongoDB
- JWT cho authentication
- Pydantic cho validation
- Google GenAI SDK

**Database:**
- MongoDB với Vector Search
- Collections cho từng loại dữ liệu
- Indexes tối ưu cho performance

**External Services:**
- Google Gemini Pro API
- File storage system
- Email services (future)

## Kiến Trúc Backend

### Cấu Trúc Thư Mục

```
BEDB/app/
├── main.py                 # FastAPI application entry
├── config.py              # Configuration management
├── database.py            # MongoDB connection
├── auth.py                # JWT authentication utilities
├── models/                # Beanie ODM models
│   ├── user.py           # User, roles
│   ├── course.py         # Course, Chapter
│   ├── enrollment.py     # Student enrollment
│   ├── upload.py         # File uploads
│   ├── quiz.py           # Quiz system
│   ├── chat.py           # AI chat
│   └── dashboard.py      # Progress tracking
├── schemas/               # Pydantic request/response
│   ├── auth.py
│   ├── course.py
│   ├── enrollment.py
│   └── ...
├── services/              # Business logic
│   ├── genai_service.py  # Google AI integration
│   ├── file_service.py   # File processing
│   └── vector_service.py # Vector search
└── routers/               # API endpoints
    ├── auth.py           # Authentication
    ├── courses.py        # Course management
    ├── student.py        # Student operations
    ├── instructor.py     # Instructor operations
    ├── uploads.py        # File operations
    ├── quiz.py           # Quiz operations
    ├── chat.py           # Chat operations
    └── dashboard.py      # Dashboard operations
```

### Data Flow Pattern

```
HTTP Request → Router → Service → Model → Database
                ↓         ↓       ↓
            Validation  Business  Data
                       Logic    Persistence
```

### API Design

**Base URL:** `/api/v1/`

**Authentication:** JWT Bearer Token

**Response Format:**
```json
{
  "data": {...},
  "message": "Success",
  "status_code": 200
}
```

### Database Schema

#### Collections chính:

1. **users** - Thông tin người dùng
2. **courses** - Khóa học và chương
3. **enrollments** - Ghi danh sinh viên
4. **uploads** - File tải lên
5. **quizzes** - Quiz và câu hỏi
6. **quiz_history** - Lịch sử làm bài
7. **chat_sessions** - Phiên chat
8. **chat_messages** - Tin nhắn chat
9. **dashboard_progress** - Tiến độ học tập
10. **embeddings** - Vector embeddings cho search

#### Relationships:

```
User (1) ──→ (N) Course
User (1) ──→ (N) Enrollment ←── (1) Course
User (1) ──→ (N) Upload
Course (1) ──→ (N) Quiz
Quiz (1) ──→ (N) QuizQuestion
User + Quiz ──→ QuizHistory
User (1) ──→ (N) ChatSession
ChatSession (1) ──→ (N) ChatMessage
```

## Kiến Trúc Frontend

### Cấu Trúc Thư Mục

```
learning-app-fe/src/
├── components/
│   ├── ui/               # Base components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   └── ...
│   ├── layout/           # Layout components
│   │   ├── DashboardLayout.tsx
│   │   └── ProtectedRoute.tsx
│   └── enrollment/       # Feature components
├── pages/                # Route pages
│   ├── auth/
│   ├── courses/
│   ├── enrollment/
│   ├── chat/
│   ├── quiz/
│   └── admin/
├── services/             # API integration
│   ├── api.ts           # Base API client
│   ├── authService.ts
│   ├── courseService.ts
│   └── ...
├── stores/               # Zustand stores
│   ├── authStore.ts
│   ├── courseStore.ts
│   └── ...
├── types/                # TypeScript types
├── i18n/                 # Internationalization
└── lib/                  # Utilities
```

### Component Architecture

```
App
├── Router
    ├── PublicRoutes
    │   ├── LandingPage
    │   ├── LoginPage
    │   └── RegisterPage
    └── ProtectedRoutes
        ├── DashboardLayout
        │   ├── Sidebar
        │   ├── Header
        │   └── MainContent
        └── Pages
            ├── Dashboard
            ├── Courses
            ├── Chat
            └── ...
```

### State Management

**Zustand Stores:**

1. **authStore** - User authentication state
2. **courseStore** - Course data and operations
3. **enrollmentStore** - Enrollment operations
4. **uploadStore** - File upload state
5. **chatStore** - Chat sessions and messages
6. **quizStore** - Quiz data and results
7. **dashboardStore** - Dashboard statistics
8. **uiStore** - UI state (theme, language, etc.)

### Data Flow

```
User Action → Component → Store Action → API Service → Backend
                ↓             ↓            ↓
            UI Update    State Update   HTTP Request
```

## Tích Hợp AI

### Google GenAI Integration

**Service:** `genai_service.py`

**Capabilities:**
1. **Course Generation** - Tạo khóa học từ prompt
2. **Quiz Generation** - Sinh câu hỏi từ nội dung
3. **Chat Responses** - Trả lời câu hỏi
4. **Content Summarization** - Tóm tắt nội dung
5. **Flashcard Creation** - Tạo thẻ ghi nhớ

**Chat Modes:**
- **Strict Mode**: Chỉ trả lời dựa trên nội dung khóa học
- **Hybrid Mode**: Kết hợp nội dung khóa học và kiến thức chung

### Vector Search

**Implementation:**
- MongoDB Atlas Vector Search
- Text embeddings cho semantic search
- Context-aware responses

**Process:**
1. Text extraction từ files/courses
2. Generate embeddings
3. Store trong embeddings collection
4. Search và retrieve relevant context
5. Generate AI response với context

## Authentication & Authorization

### JWT Implementation

**Flow:**
1. User login → Backend validates → Generate JWT
2. JWT stored trong client (localStorage)
3. JWT sent với mỗi API request
4. Backend validates JWT → Allow/Deny access

**Token Structure:**
```json
{
  "user_id": "...",
  "email": "...",
  "role": "student|instructor|admin",
  "exp": "...",
  "iat": "..."
}
```

### Role-Based Access Control

**Roles:**
- **Student**: Cơ bản - học, làm quiz, chat
- **Instructor**: Tạo khóa học, quản lý sinh viên
- **Admin**: Quản lý toàn hệ thống

**Implementation:**
- Middleware kiểm tra role
- Route protection
- UI elements conditional rendering

## File Processing

### Supported Formats

1. **PDF** - PyPDF2 extraction
2. **DOCX** - python-docx processing  
3. **TXT** - Direct reading
4. **Future**: Video transcription, Image OCR

### Processing Pipeline

```
File Upload → Validation → Text Extraction → AI Processing → Vector Indexing → Integration
```

**Steps:**
1. **Upload**: Client uploads file
2. **Validation**: File type, size checks
3. **Storage**: Secure file storage
4. **Processing**: Background text extraction
5. **AI Enhancement**: Clean và process text
6. **Indexing**: Generate embeddings
7. **Integration**: Available cho chat/quiz

## Deployment Architecture

### Development

```
Developer Machine
├── Backend (localhost:8000)
├── Frontend (localhost:3000)
├── MongoDB (localhost:27017)
└── Google AI API (external)
```

### Production

```
Load Balancer
├── Frontend (Static hosting - Vercel/Netlify)
├── Backend API (Container/VPS)
├── MongoDB Atlas (Cloud)
└── CDN (Static assets)
```

## Security Architecture

### Backend Security

1. **Authentication**: JWT với secure secret
2. **Authorization**: Role-based access
3. **Input Validation**: Pydantic schemas
4. **File Security**: Type validation, size limits
5. **CORS**: Configured origins
6. **Rate Limiting**: API call limits

### Frontend Security

1. **XSS Protection**: React built-in protection
2. **CSRF**: SameSite cookies
3. **Secure Storage**: JWT trong httpOnly cookies (future)
4. **Input Sanitization**: Form validation
5. **Error Handling**: No sensitive data exposure

## Performance Optimization

### Backend Performance

1. **Database Indexing**: Optimized queries
2. **Caching**: Redis for frequent data (future)
3. **Async Processing**: File processing queue
4. **Connection Pooling**: MongoDB connections
5. **API Response Optimization**: Pagination, filtering

### Frontend Performance

1. **Code Splitting**: Route-based splitting
2. **Lazy Loading**: Components, images
3. **Caching**: API response caching
4. **Bundle Optimization**: Tree shaking
5. **Image Optimization**: WebP, lazy loading

## Monitoring và Logging

### Backend Monitoring

1. **API Metrics**: Response times, error rates
2. **Database Metrics**: Query performance, connections
3. **System Metrics**: CPU, memory, disk
4. **Application Logs**: Structured logging
5. **Error Tracking**: Exception monitoring

### Frontend Monitoring

1. **User Analytics**: Page views, interactions
2. **Performance Metrics**: Core Web Vitals
3. **Error Tracking**: JavaScript errors
4. **Network Monitoring**: API call performance

## Scalability Considerations

### Horizontal Scaling

1. **API Servers**: Load balancer + multiple instances
2. **Database**: MongoDB sharding
3. **File Storage**: Distributed storage
4. **CDN**: Global content delivery

### Vertical Scaling

1. **Server Resources**: CPU, RAM upgrades
2. **Database**: Optimized queries, indexing
3. **Caching**: Redis implementation
4. **Connection Pooling**: Efficient resource usage

## Future Architecture Enhancements

### Planned Improvements

1. **Microservices**: Split monolith into services
2. **Message Queue**: Async job processing
3. **Caching Layer**: Redis implementation
4. **WebSocket**: Real-time features
5. **CDN**: Global content delivery
6. **Container Orchestration**: Kubernetes
7. **CI/CD Pipeline**: Automated deployment
8. **API Gateway**: Centralized API management

