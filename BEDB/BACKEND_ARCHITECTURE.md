# 🏗️ Backend Architecture - AI Learning Platform

## 📋 Tổng quan Backend

### 🚀 FastAPI Application Structure

```mermaid
graph TB
    subgraph "FastAPI Application"
        MAIN[main.py - App Entry Point]
        CONFIG[config.py - Settings]
        DATABASE[database.py - MongoDB Connection]
        AUTH[auth.py - JWT Authentication]
    end
    
    subgraph "API Layer"
        ROUTERS[routers/ - API Endpoints]
        MIDDLEWARE[Middleware Stack]
        CORS[CORS Configuration]
    end
    
    subgraph "Business Logic"
        SERVICES[services/ - Business Services]
        MODELS[models/ - Database Models]
        SCHEMAS[schemas/ - Data Validation]
    end
    
    subgraph "External Services"
        GENAI[Google GenAI]
        MONGODB[MongoDB Atlas]
        VECTOR[Vector Search]
    end
    
    MAIN --> CONFIG
    MAIN --> DATABASE
    MAIN --> AUTH
    MAIN --> ROUTERS
    ROUTERS --> MIDDLEWARE
    MIDDLEWARE --> CORS
    
    ROUTERS --> SERVICES
    SERVICES --> MODELS
    MODELS --> SCHEMAS
    
    SERVICES --> GENAI
    MODELS --> MONGODB
    SERVICES --> VECTOR
```

## 📁 Chi tiết cấu trúc Backend

### 🎯 Core Files

```
BEDB/app/
├── main.py              # 🚀 FastAPI application entry point
├── config.py            # ⚙️ Environment configuration
├── database.py          # 🗄️ MongoDB connection setup
└── auth.py              # 🔐 JWT authentication utilities
```

#### main.py - Application Entry
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import all routers
from app.routers import (
    auth, courses, uploads, chat, 
    quiz, dashboard, admin, search, leaderboard
)

app = FastAPI(
    title="AI Learning Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware setup
app.add_middleware(CORSMiddleware, ...)

# Include all routers with /api/v1 prefix
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(courses.router, prefix="/api/v1/courses", tags=["Courses"])
# ... other routers
```

#### config.py - Configuration Management
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database
    MONGODB_URL: str
    DATABASE_NAME: str
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Google GenAI
    GOOGLE_API_KEY: str
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 🗄️ Models Layer (Beanie ODM)

```mermaid
graph TD
    subgraph "models/"
        USER[user.py - User Models]
        COURSE[course.py - Course Models]
        QUIZ[quiz.py - Quiz Models]
        CHAT[chat.py - Chat Models]
        UPLOAD[upload.py - Upload Models]
        DASHBOARD[dashboard.py - Progress Models]
    end
    
    subgraph "Beanie Features"
        ODM[Object Document Mapper]
        VALIDATION[Data Validation]
        INDEXES[Database Indexes]
        RELATIONSHIPS[Document References]
    end
    
    USER --> ODM
    COURSE --> ODM
    QUIZ --> ODM
    CHAT --> ODM
    UPLOAD --> ODM
    DASHBOARD --> ODM
    
    ODM --> VALIDATION
    ODM --> INDEXES
    ODM --> RELATIONSHIPS
```

#### user.py - User Models
```python
from beanie import Document, Indexed
from pydantic import EmailStr
from typing import Optional
from datetime import datetime

class User(Document):
    email: Indexed(EmailStr, unique=True)
    password_hash: str
    name: str
    role: str = "student"  # student, instructor, admin
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    class Settings:
        name = "users"
        indexes = [
            [("email", 1)],
            [("role", 1)],
            [("created_at", -1)]
        ]

class UserProfile(Document):
    user_id: PydanticObjectId
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    preferences: dict = {}
    
    class Settings:
        name = "user_profiles"
```

#### course.py - Course Models
```python
class Course(Document):
    title: str
    description: str
    outline: Optional[str] = None
    level: str = "beginner"  # beginner, intermediate, advanced
    tags: List[str] = []
    owner_id: PydanticObjectId
    source: str = "manual"  # manual, ai_generated, from_upload
    is_public: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    class Settings:
        name = "courses"
        indexes = [
            [("owner_id", 1)],
            [("level", 1)],
            [("tags", 1)],
            [("created_at", -1)]
        ]

class Chapter(Document):
    course_id: PydanticObjectId
    title: str
    content: str
    order: int
    duration_minutes: Optional[int] = None
    
    class Settings:
        name = "chapters"
        indexes = [
            [("course_id", 1), ("order", 1)]
        ]
```

### 🔄 Schemas Layer (Pydantic)

```mermaid
graph LR
    subgraph "schemas/"
        AUTH_SCHEMA[auth.py - Auth Schemas]
        COURSE_SCHEMA[course.py - Course Schemas]
        QUIZ_SCHEMA[quiz.py - Quiz Schemas]
        CHAT_SCHEMA[chat.py - Chat Schemas]
        UPLOAD_SCHEMA[upload.py - Upload Schemas]
        DASHBOARD_SCHEMA[dashboard.py - Dashboard Schemas]
    end
    
    subgraph "Schema Types"
        REQUEST[Request Schemas]
        RESPONSE[Response Schemas]
        UPDATE[Update Schemas]
        CREATE[Create Schemas]
    end
    
    AUTH_SCHEMA --> REQUEST
    COURSE_SCHEMA --> RESPONSE
    QUIZ_SCHEMA --> UPDATE
    CHAT_SCHEMA --> CREATE
```

#### auth.py - Authentication Schemas
```python
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
```

#### course.py - Course Schemas
```python
class CourseCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., max_length=1000)
    level: str = Field(default="beginner", regex="^(beginner|intermediate|advanced)$")
    tags: List[str] = Field(default=[], max_items=10)

class CourseResponse(BaseModel):
    id: str
    title: str
    description: str
    outline: Optional[str]
    level: str
    tags: List[str]
    owner_id: str
    source: str
    is_public: bool
    created_at: datetime
    updated_at: Optional[datetime]

class AIGenerateRequest(BaseModel):
    topic: str = Field(..., min_length=5, max_length=200)
    level: str = Field(default="beginner")
    num_chapters: int = Field(default=5, ge=3, le=20)
```

### 🛣️ Routers Layer (API Endpoints)

```mermaid
graph TB
    subgraph "routers/"
        AUTH_ROUTER[auth.py - Authentication]
        COURSE_ROUTER[courses.py - Course Management]
        UPLOAD_ROUTER[uploads.py - File Upload]
        CHAT_ROUTER[chat.py - AI Chat]
        QUIZ_ROUTER[quiz.py - Quiz System]
        DASHBOARD_ROUTER[dashboard.py - Analytics]
        ADMIN_ROUTER[admin.py - Admin Panel]
        SEARCH_ROUTER[search.py - Vector Search]
        LEADERBOARD_ROUTER[leaderboard.py - Rankings]
        USERS_ROUTER[users.py - User Management]
    end
    
    subgraph "HTTP Methods"
        GET[GET - Retrieve Data]
        POST[POST - Create Data]
        PATCH[PATCH - Update Data]
        DELETE[DELETE - Remove Data]
    end
    
    AUTH_ROUTER --> POST
    COURSE_ROUTER --> GET
    COURSE_ROUTER --> POST
    COURSE_ROUTER --> PATCH
    COURSE_ROUTER --> DELETE
    UPLOAD_ROUTER --> POST
    CHAT_ROUTER --> POST
    QUIZ_ROUTER --> GET
    QUIZ_ROUTER --> POST
    DASHBOARD_ROUTER --> GET
```

#### auth.py - Authentication Router
```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    """User login with email and password"""
    user = await User.find_one(User.email == credentials.email)
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    tokens = create_tokens(user.id)
    return LoginResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        user=UserResponse.from_orm(user)
    )

@router.post("/register", response_model=UserResponse)
async def register(user_data: RegisterRequest):
    """Register new user account"""
    # Check if user exists
    existing_user = await User.find_one(User.email == user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password
    )
    await user.insert()
    
    return UserResponse.from_orm(user)

@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return UserResponse.from_orm(current_user)
```

#### courses.py - Course Management Router
```python
@router.get("/", response_model=List[CourseResponse])
async def get_courses(
    skip: int = 0,
    limit: int = 20,
    owner: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get user's courses or system courses"""
    query = {}
    if owner == "user":
        query["owner_id"] = current_user.id
    elif owner == "system":
        query["is_public"] = True
    
    courses = await Course.find(query).skip(skip).limit(limit).to_list()
    return [CourseResponse.from_orm(course) for course in courses]

@router.post("/", response_model=CourseResponse)
async def create_course(
    course_data: CourseCreateRequest,
    current_user: User = Depends(get_current_user)
):
    """Create a new course manually"""
    course = Course(
        **course_data.dict(),
        owner_id=current_user.id
    )
    await course.insert()
    return CourseResponse.from_orm(course)

@router.post("/from-prompt", response_model=CourseResponse)
async def create_course_from_ai(
    ai_request: AIGenerateRequest,
    current_user: User = Depends(get_current_user),
    genai_service: GenAIService = Depends()
):
    """Generate course using AI"""
    # Generate course outline using AI
    outline = await genai_service.generate_course_outline(
        topic=ai_request.topic,
        level=ai_request.level,
        num_chapters=ai_request.num_chapters
    )
    
    course = Course(
        title=ai_request.topic,
        description=f"AI-generated course about {ai_request.topic}",
        outline=outline,
        level=ai_request.level,
        owner_id=current_user.id,
        source="ai_generated"
    )
    await course.insert()
    
    return CourseResponse.from_orm(course)
```

### 🔧 Services Layer (Business Logic)

```mermaid
graph TD
    subgraph "services/"
        GENAI[genai_service.py - AI Integration]
        FILE[file_service.py - File Processing]
        VECTOR[vector_service.py - Search]
    end
    
    subgraph "External APIs"
        GOOGLE_AI[Google GenAI API]
        MONGODB_VECTOR[MongoDB Vector Search]
        FILE_STORAGE[File Storage System]
    end
    
    GENAI --> GOOGLE_AI
    FILE --> FILE_STORAGE
    VECTOR --> MONGODB_VECTOR
```

#### genai_service.py - AI Integration
```python
import google.generativeai as genai
from app.config import settings

class GenAIService:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate_course_outline(
        self, 
        topic: str, 
        level: str, 
        num_chapters: int
    ) -> str:
        """Generate course outline using AI"""
        prompt = f"""
        Create a detailed course outline for: {topic}
        Level: {level}
        Number of chapters: {num_chapters}
        
        Format as JSON with chapters array containing:
        - title: Chapter title
        - content: Detailed content description
        - duration: Estimated duration in minutes
        """
        
        response = await self.model.generate_content_async(prompt)
        return response.text
    
    async def generate_quiz_questions(
        self, 
        content: str, 
        num_questions: int = 5
    ) -> List[dict]:
        """Generate quiz questions from content"""
        prompt = f"""
        Based on this content, create {num_questions} multiple choice questions:
        
        {content}
        
        Format as JSON array with:
        - question: The question text
        - options: Array of 4 options
        - correct_answer: Index of correct option (0-3)
        - explanation: Why this answer is correct
        """
        
        response = await self.model.generate_content_async(prompt)
        return json.loads(response.text)
    
    async def chat_response(
        self, 
        message: str, 
        context: Optional[str] = None,
        mode: str = "hybrid"
    ) -> str:
        """Generate chat response"""
        if mode == "strict" and context:
            prompt = f"""
            Context: {context}
            
            User question: {message}
            
            Answer based ONLY on the provided context.
            If the answer is not in the context, say "I don't have that information in the provided context."
            """
        else:
            prompt = f"""
            User question: {message}
            
            Provide a helpful and accurate response.
            """
        
        response = await self.model.generate_content_async(prompt)
        return response.text
```

#### file_service.py - File Processing
```python
import PyPDF2
import docx
from typing import Optional

class FileService:
    async def extract_text_from_file(self, file_path: str, file_type: str) -> str:
        """Extract text from uploaded file"""
        try:
            if file_type == "application/pdf":
                return await self._extract_from_pdf(file_path)
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return await self._extract_from_docx(file_path)
            elif file_type == "text/plain":
                return await self._extract_from_txt(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        except Exception as e:
            raise Exception(f"Error extracting text: {str(e)}")
    
    async def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    
    async def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    
    async def _extract_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
```

#### vector_service.py - Vector Search
```python
from pymongo import MongoClient
from typing import List, Dict

class VectorService:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_URL)
        self.db = self.client[settings.DATABASE_NAME]
        self.collection = self.db.embeddings
    
    async def create_embeddings(self, text: str, source_id: str, source_type: str):
        """Create embeddings for text content"""
        # Split text into chunks
        chunks = self._split_text(text)
        
        embeddings = []
        for i, chunk in enumerate(chunks):
            # Generate embedding using AI service
            embedding = await self._generate_embedding(chunk)
            
            embeddings.append({
                "source_id": source_id,
                "source_type": source_type,
                "chunk_index": i,
                "text": chunk,
                "embedding": embedding,
                "created_at": datetime.utcnow()
            })
        
        # Insert embeddings to MongoDB
        await self.collection.insert_many(embeddings)
    
    async def vector_search(
        self, 
        query: str, 
        limit: int = 10,
        source_types: Optional[List[str]] = None
    ) -> List[Dict]:
        """Perform vector search"""
        # Generate query embedding
        query_embedding = await self._generate_embedding(query)
        
        # Build aggregation pipeline
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": limit * 10,
                    "limit": limit
                }
            }
        ]
        
        if source_types:
            pipeline.append({
                "$match": {"source_type": {"$in": source_types}}
            })
        
        results = await self.collection.aggregate(pipeline).to_list(length=limit)
        return results
    
    def _split_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        """Split text into chunks"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            if current_size + len(word) > chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_size = len(word)
            else:
                current_chunk.append(word)
                current_size += len(word) + 1
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
```

## 🔄 Request/Response Flow

### 📊 Complete API Request Flow

```mermaid
sequenceDiagram
    participant Client as Frontend Client
    participant Router as FastAPI Router
    participant Auth as Auth Middleware
    participant Schema as Pydantic Schema
    participant Service as Business Service
    participant Model as Beanie Model
    participant DB as MongoDB
    participant AI as Google GenAI
    
    Client->>Router: HTTP Request + JWT
    Router->>Auth: Validate Token
    Auth->>Router: User Context
    Router->>Schema: Validate Request
    Schema->>Service: Business Logic
    
    alt AI Operation
        Service->>AI: Generate Content
        AI->>Service: AI Response
    end
    
    Service->>Model: Database Operation
    Model->>DB: Query/Update
    DB->>Model: Result
    Model->>Service: Processed Data
    Service->>Schema: Format Response
    Schema->>Router: Validated Response
    Router->>Client: JSON Response
```

### 🔐 Authentication Flow

```mermaid
graph LR
    subgraph "Login Process"
        LOGIN[POST /api/v1/auth/login]
        VALIDATE[Validate Credentials]
        HASH[Check Password Hash]
        TOKEN[Generate JWT Tokens]
        RESPONSE[Return Tokens + User]
    end
    
    subgraph "Protected Request"
        REQUEST[API Request + Token]
        MIDDLEWARE[Auth Middleware]
        VERIFY[Verify JWT Token]
        USER[Extract User Info]
        PROCEED[Continue to Endpoint]
    end
    
    LOGIN --> VALIDATE
    VALIDATE --> HASH
    HASH --> TOKEN
    TOKEN --> RESPONSE
    
    REQUEST --> MIDDLEWARE
    MIDDLEWARE --> VERIFY
    VERIFY --> USER
    USER --> PROCEED
```

## 🗄️ Database Design

### 📊 MongoDB Collections Structure

```mermaid
erDiagram
    users ||--o{ courses : owns
    users ||--o{ uploads : creates
    users ||--o{ chat_sessions : starts
    users ||--o{ quiz_history : takes
    users ||--o{ progress : tracks
    
    courses ||--o{ chapters : contains
    courses ||--o{ quizzes : generates
    courses ||--o{ chat_sessions : discusses
    
    uploads ||--o{ embeddings : indexes
    uploads ||--o{ quizzes : generates
    
    chat_sessions ||--o{ chat_messages : contains
    quizzes ||--o{ quiz_history : records
    
    users {
        ObjectId _id PK
        string email UK
        string password_hash
        string name
        string role
        boolean is_active
        datetime created_at
        datetime updated_at
    }
    
    courses {
        ObjectId _id PK
        string title
        string description
        string outline
        string level
        array tags
        ObjectId owner_id FK
        string source
        boolean is_public
        datetime created_at
        datetime updated_at
    }
    
    uploads {
        ObjectId _id PK
        ObjectId user_id FK
        string filename
        string file_type
        int file_size
        string status
        string extracted_text
        string file_path
        datetime created_at
        datetime updated_at
    }
    
    embeddings {
        ObjectId _id PK
        ObjectId source_id FK
        string source_type
        int chunk_index
        string text
        array embedding
        datetime created_at
    }
```

### 📈 Indexes Strategy

```python
# User indexes
users.create_index([("email", 1)], unique=True)
users.create_index([("role", 1)])
users.create_index([("created_at", -1)])

# Course indexes
courses.create_index([("owner_id", 1)])
courses.create_index([("level", 1)])
courses.create_index([("tags", 1)])
courses.create_index([("is_public", 1)])
courses.create_index([("created_at", -1)])

# Upload indexes
uploads.create_index([("user_id", 1)])
uploads.create_index([("status", 1)])
uploads.create_index([("file_type", 1)])

# Vector search index
embeddings.create_search_index(
    {
        "definition": {
            "fields": [
                {
                    "type": "vector",
                    "path": "embedding",
                    "numDimensions": 1536,
                    "similarity": "cosine"
                }
            ]
        }
    },
    name="vector_index"
)
```

## 🔧 Configuration & Environment

### ⚙️ Environment Variables

```bash
# Database Configuration
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=ai_learning_platform

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Google GenAI
GOOGLE_API_KEY=your-google-genai-api-key

# File Upload
MAX_FILE_SIZE=10485760  # 10MB in bytes
UPLOAD_DIR=uploads
ALLOWED_EXTENSIONS=pdf,docx,txt

# Email Configuration (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Redis (for caching, optional)
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60  # seconds
```

## 🚀 Deployment Configuration

### 🐳 Docker Setup

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app ./app

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongo:27017/ai_learning
      - JWT_SECRET_KEY=your-secret-key
      - GOOGLE_API_KEY=your-google-api-key
    depends_on:
      - mongo
      - redis
    volumes:
      - ./uploads:/app/uploads

  mongo:
    image: mongo:7.0
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  mongo_data:
  redis_data:
```

## 📊 API Performance & Monitoring

### 🔍 Logging Strategy

```python
import logging
from fastapi import Request
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.4f}s")
    
    return response
```

### 📈 Health Check Endpoints

```python
@app.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with dependencies"""
    checks = {
        "api": "healthy",
        "database": "unknown",
        "ai_service": "unknown"
    }
    
    # Check database connection
    try:
        await User.find_one()
        checks["database"] = "healthy"
    except Exception:
        checks["database"] = "unhealthy"
    
    # Check AI service
    try:
        genai_service = GenAIService()
        await genai_service.model.generate_content_async("test")
        checks["ai_service"] = "healthy"
    except Exception:
        checks["ai_service"] = "unhealthy"
    
    overall_status = "healthy" if all(
        status == "healthy" for status in checks.values()
    ) else "unhealthy"
    
    return {
        "status": overall_status,
        "checks": checks,
        "timestamp": datetime.utcnow()
    }
```

---

## 🎯 Kết luận Backend Architecture

Backend AI Learning Platform được thiết kế với:

✅ **FastAPI Framework**: Modern, fast, và type-safe  
✅ **MongoDB + Beanie**: NoSQL database với ODM  
✅ **Google GenAI**: AI content generation  
✅ **Vector Search**: Semantic search capabilities  
✅ **JWT Authentication**: Secure token-based auth  
✅ **Pydantic Validation**: Request/response validation  
✅ **Modular Architecture**: Scalable và maintainable  
✅ **Docker Ready**: Containerized deployment  
✅ **Comprehensive Logging**: Monitoring và debugging  

**🚀 Production-ready backend với full API coverage!**
