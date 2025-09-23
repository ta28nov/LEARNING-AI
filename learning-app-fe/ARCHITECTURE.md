# 🏗️ Sơ đồ kiến trúc AI Learning Platform

## 📋 Tổng quan hệ thống

```mermaid
graph TB
    subgraph "Frontend (React + TypeScript)"
        UI[User Interface]
        ROUTER[React Router]
        STORES[Zustand Stores]
        SERVICES[API Services]
        COMPONENTS[UI Components]
    end
    
    subgraph "Backend (FastAPI + Python)"
        API[FastAPI Routes]
        MODELS[Beanie Models]
        SCHEMAS[Pydantic Schemas]
        SERVICES_BE[Business Services]
        AI[Google GenAI]
    end
    
    subgraph "Database"
        MONGO[(MongoDB)]
        VECTOR[Vector Search]
    end
    
    UI --> ROUTER
    ROUTER --> COMPONENTS
    COMPONENTS --> STORES
    STORES --> SERVICES
    SERVICES -->|HTTP/JSON| API
    API --> SCHEMAS
    SCHEMAS --> MODELS
    MODELS --> MONGO
    API --> SERVICES_BE
    SERVICES_BE --> AI
    SERVICES_BE --> VECTOR
    VECTOR --> MONGO
```

## 🎯 Frontend Architecture

### 📁 Cấu trúc thư mục Frontend

```
learning-app-fe/src/
├── 🎨 components/
│   ├── ui/                 # Base UI Components
│   │   ├── Button.tsx      # → Variants: primary, secondary, ghost
│   │   ├── Card.tsx        # → Layout components
│   │   ├── Input.tsx       # → Form inputs với validation
│   │   ├── Modal.tsx       # → Dialog components
│   │   ├── ThemeToggle.tsx # → Dark/Light mode switch
│   │   └── ...animations   # → Framer Motion components
│   └── layout/
│       ├── DashboardLayout.tsx  # → Main app layout
│       └── ProtectedRoute.tsx   # → Auth guard
│
├── 📄 pages/              # Route Components
│   ├── auth/              # → Login, Register
│   ├── courses/           # → Course management
│   ├── chat/              # → AI Chat interface
│   ├── quiz/              # → Quiz system
│   └── admin/             # → Admin panel
│
├── 🔄 stores/             # Zustand State Management
│   ├── authStore.ts       # → User authentication
│   ├── courseStore.ts     # → Course data
│   ├── chatStore.ts       # → Chat sessions
│   └── ...
│
├── 🌐 services/           # API Integration Layer
│   ├── api.ts             # → Base API client
│   ├── authService.ts     # → Auth endpoints
│   ├── courseService.ts   # → Course CRUD
│   └── ...
│
├── 🎭 contexts/           # React Contexts
│   └── ThemeContext.tsx   # → Theme management
│
├── 🌍 i18n/               # Internationalization
│   ├── index.ts           # → i18n configuration
│   └── locales/           # → Translation files
│
└── 📝 types/              # TypeScript Definitions
    └── index.ts           # → Shared interfaces
```

### 🔄 Data Flow Frontend

```mermaid
graph LR
    subgraph "User Interaction"
        USER[👤 User]
        UI[🎨 UI Component]
    end
    
    subgraph "State Management"
        STORE[📦 Zustand Store]
        STATE[💾 Local State]
    end
    
    subgraph "API Layer"
        SERVICE[🌐 API Service]
        CLIENT[🔗 API Client]
    end
    
    subgraph "Backend"
        API[🚀 FastAPI]
    end
    
    USER --> UI
    UI --> STORE
    UI --> STATE
    STORE --> SERVICE
    SERVICE --> CLIENT
    CLIENT -->|HTTP Request| API
    API -->|JSON Response| CLIENT
    CLIENT --> SERVICE
    SERVICE --> STORE
    STORE --> UI
    UI --> USER
```

### 🧩 Component Relationships

```mermaid
graph TD
    APP[App.tsx]
    APP --> THEME[ThemeProvider]
    APP --> I18N[i18n Provider]
    APP --> ROUTER[React Router]
    
    ROUTER --> LANDING[LandingPage]
    ROUTER --> AUTH[Auth Pages]
    ROUTER --> PROTECTED[ProtectedRoute]
    
    PROTECTED --> LAYOUT[DashboardLayout]
    LAYOUT --> SIDEBAR[Sidebar Navigation]
    LAYOUT --> MAIN[Main Content Area]
    
    MAIN --> DASHBOARD[Dashboard]
    MAIN --> COURSES[Courses Pages]
    MAIN --> CHAT[Chat Pages]
    MAIN --> QUIZ[Quiz Pages]
    MAIN --> UPLOADS[Upload Pages]
    MAIN --> ADMIN[Admin Pages]
    
    subgraph "Shared Components"
        BUTTON[Button]
        CARD[Card]
        INPUT[Input]
        MODAL[Modal]
        LOADER[LoadingSpinner]
    end
    
    DASHBOARD --> BUTTON
    COURSES --> CARD
    CHAT --> INPUT
    QUIZ --> MODAL
    UPLOADS --> LOADER
```

## 🚀 Backend Architecture

### 📁 Cấu trúc thư mục Backend

```
BEDB/app/
├── 🎯 main.py             # FastAPI Application Entry
├── ⚙️ config.py           # Configuration Management
├── 🗄️ database.py         # MongoDB Connection
├── 🔐 auth.py             # JWT Authentication
│
├── 📊 models/             # Beanie ODM Models
│   ├── user.py            # → User, Profile models
│   ├── course.py          # → Course, Chapter models
│   ├── quiz.py            # → Quiz, Question models
│   ├── chat.py            # → ChatSession, Message
│   ├── upload.py          # → File upload models
│   └── dashboard.py       # → Progress tracking
│
├── 🔄 schemas/            # Pydantic Schemas
│   ├── auth.py            # → Request/Response schemas
│   ├── course.py          # → Course data validation
│   ├── quiz.py            # → Quiz schemas
│   └── ...
│
├── 🛣️ routers/            # API Route Handlers
│   ├── auth.py            # → /api/v1/auth/*
│   ├── courses.py         # → /api/v1/courses/*
│   ├── quiz.py            # → /api/v1/quiz/*
│   ├── chat.py            # → /api/v1/chat/*
│   ├── uploads.py         # → /api/v1/uploads/*
│   ├── dashboard.py       # → /api/v1/dashboard/*
│   ├── admin.py           # → /api/v1/admin/*
│   ├── search.py          # → /api/v1/search/*
│   └── leaderboard.py     # → /api/v1/leaderboard
│
└── 🔧 services/           # Business Logic
    ├── genai_service.py   # → Google GenAI integration
    ├── file_service.py    # → File processing
    └── vector_service.py  # → Vector search
```

### 🔄 Backend Request Flow

```mermaid
sequenceDiagram
    participant FE as Frontend
    participant API as FastAPI Router
    participant AUTH as Auth Middleware
    participant SCHEMA as Pydantic Schema
    participant SERVICE as Business Service
    participant MODEL as Beanie Model
    participant DB as MongoDB
    participant AI as Google GenAI
    
    FE->>API: HTTP Request + JWT Token
    API->>AUTH: Validate JWT Token
    AUTH->>API: User Info
    API->>SCHEMA: Validate Request Data
    SCHEMA->>SERVICE: Process Business Logic
    
    alt AI Operation
        SERVICE->>AI: Generate Content
        AI->>SERVICE: AI Response
    end
    
    SERVICE->>MODEL: Database Operation
    MODEL->>DB: Query/Update
    DB->>MODEL: Result
    MODEL->>SERVICE: Processed Data
    SERVICE->>SCHEMA: Format Response
    SCHEMA->>API: Validated Response
    API->>FE: JSON Response
```

## 🔗 API Endpoints Mapping

### 🔐 Authentication Flow

```mermaid
graph LR
    subgraph "Frontend Auth"
        LOGIN[LoginPage.tsx]
        STORE[authStore.ts]
        SERVICE[authService.ts]
    end
    
    subgraph "Backend Auth"
        ROUTER[auth.py router]
        SCHEMA[auth.py schema]
        MODEL[user.py model]
    end
    
    LOGIN --> STORE
    STORE --> SERVICE
    SERVICE -->|POST /api/v1/auth/login| ROUTER
    ROUTER --> SCHEMA
    SCHEMA --> MODEL
    MODEL --> SCHEMA
    SCHEMA --> ROUTER
    ROUTER -->|JWT Token| SERVICE
    SERVICE --> STORE
    STORE --> LOGIN
```

### 📚 Course Management Flow

```mermaid
graph TD
    subgraph "Frontend Course"
        COURSES[CoursesPage.tsx]
        DETAIL[CourseDetailPage.tsx]
        STORE[courseStore.ts]
        SERVICE[courseService.ts]
    end
    
    subgraph "Backend Course"
        ROUTER[courses.py]
        SCHEMA[course.py schema]
        MODEL[course.py model]
        AI_SERVICE[genai_service.py]
    end
    
    COURSES --> STORE
    DETAIL --> STORE
    STORE --> SERVICE
    
    SERVICE -->|GET /api/v1/courses| ROUTER
    SERVICE -->|POST /api/v1/courses| ROUTER
    SERVICE -->|POST /api/v1/courses/from-prompt| ROUTER
    
    ROUTER --> SCHEMA
    SCHEMA --> MODEL
    ROUTER --> AI_SERVICE
    AI_SERVICE -->|Generate Content| ROUTER
    MODEL --> SCHEMA
    SCHEMA --> ROUTER
    ROUTER --> SERVICE
    SERVICE --> STORE
    STORE --> COURSES
    STORE --> DETAIL
```

### 💬 Chat System Flow

```mermaid
sequenceDiagram
    participant UI as ChatPage.tsx
    participant STORE as chatStore.ts
    participant SERVICE as chatService.ts
    participant API as chat.py router
    participant AI as genai_service.py
    participant DB as MongoDB
    
    UI->>STORE: Send Message
    STORE->>SERVICE: freestyleChat()
    SERVICE->>API: POST /api/v1/chat
    API->>AI: Generate Response
    AI->>API: AI Answer
    API->>DB: Save Chat History
    DB->>API: Saved
    API->>SERVICE: Response + Answer
    SERVICE->>STORE: Update Messages
    STORE->>UI: Display Messages
```

### 🧠 Quiz System Flow

```mermaid
graph TB
    subgraph "Frontend Quiz"
        QUIZ_LIST[QuizPage.tsx]
        QUIZ_DETAIL[QuizDetailPage.tsx]
        STORE[quizStore.ts]
        SERVICE[quizService.ts]
    end
    
    subgraph "Backend Quiz"
        ROUTER[quiz.py]
        SCHEMA[quiz.py schema]
        MODEL[quiz.py model]
        AI[genai_service.py]
    end
    
    QUIZ_LIST --> STORE
    QUIZ_DETAIL --> STORE
    STORE --> SERVICE
    
    SERVICE -->|POST /api/v1/quiz/generate| ROUTER
    SERVICE -->|POST /api/v1/quiz/{id}/submit| ROUTER
    SERVICE -->|GET /api/v1/quiz/history| ROUTER
    
    ROUTER --> AI
    AI -->|Generate Questions| ROUTER
    ROUTER --> SCHEMA
    SCHEMA --> MODEL
    MODEL --> SCHEMA
    SCHEMA --> ROUTER
    ROUTER --> SERVICE
    SERVICE --> STORE
```

## 🔄 State Management Flow

### 📦 Zustand Stores Architecture

```mermaid
graph TD
    subgraph "Zustand Stores"
        AUTH[authStore.ts]
        COURSE[courseStore.ts]
        CHAT[chatStore.ts]
        QUIZ[quizStore.ts]
        UPLOAD[uploadStore.ts]
        DASHBOARD[dashboardStore.ts]
    end
    
    subgraph "API Services"
        AUTH_API[authService.ts]
        COURSE_API[courseService.ts]
        CHAT_API[chatService.ts]
        QUIZ_API[quizService.ts]
        UPLOAD_API[uploadService.ts]
        DASHBOARD_API[dashboardService.ts]
    end
    
    subgraph "React Components"
        LOGIN[LoginPage]
        COURSES[CoursesPage]
        CHAT_UI[ChatPage]
        QUIZ_UI[QuizPage]
        UPLOAD_UI[UploadsPage]
        DASH[DashboardPage]
    end
    
    AUTH --> AUTH_API
    COURSE --> COURSE_API
    CHAT --> CHAT_API
    QUIZ --> QUIZ_API
    UPLOAD --> UPLOAD_API
    DASHBOARD --> DASHBOARD_API
    
    LOGIN --> AUTH
    COURSES --> COURSE
    CHAT_UI --> CHAT
    QUIZ_UI --> QUIZ
    UPLOAD_UI --> UPLOAD
    DASH --> DASHBOARD
```

### 🔄 Store Update Pattern

```mermaid
sequenceDiagram
    participant COMP as React Component
    participant STORE as Zustand Store
    participant SERVICE as API Service
    participant API as Backend API
    
    COMP->>STORE: Call Action (e.g., createCourse)
    STORE->>STORE: Set Loading State
    STORE->>SERVICE: API Call
    SERVICE->>API: HTTP Request
    API->>SERVICE: Response
    SERVICE->>STORE: Success/Error
    
    alt Success
        STORE->>STORE: Update State
        STORE->>STORE: Clear Loading
        STORE->>COMP: Re-render with New Data
    else Error
        STORE->>STORE: Set Error State
        STORE->>COMP: Show Error Message
    end
```

## 🎨 UI Component Architecture

### 🧩 Component Hierarchy

```mermaid
graph TD
    subgraph "Layout Components"
        LAYOUT[DashboardLayout]
        SIDEBAR[Sidebar]
        HEADER[Header]
        MAIN[Main Content]
    end
    
    subgraph "UI Components"
        BUTTON[Button]
        CARD[Card]
        INPUT[Input]
        MODAL[Modal]
        PROGRESS[Progress]
        SPINNER[LoadingSpinner]
    end
    
    subgraph "Feature Components"
        COURSE_CARD[CourseCard]
        CHAT_MESSAGE[ChatMessage]
        QUIZ_QUESTION[QuizQuestion]
        UPLOAD_ZONE[UploadZone]
    end
    
    subgraph "Animation Components"
        FADE_IN[FadeIn]
        STAGGER[StaggerContainer]
        ANIMATED_PAGE[AnimatedPage]
        FLOATING_BTN[FloatingButton]
    end
    
    LAYOUT --> SIDEBAR
    LAYOUT --> HEADER
    LAYOUT --> MAIN
    
    MAIN --> COURSE_CARD
    MAIN --> CHAT_MESSAGE
    MAIN --> QUIZ_QUESTION
    MAIN --> UPLOAD_ZONE
    
    COURSE_CARD --> CARD
    COURSE_CARD --> BUTTON
    COURSE_CARD --> PROGRESS
    
    CHAT_MESSAGE --> INPUT
    CHAT_MESSAGE --> SPINNER
    
    QUIZ_QUESTION --> MODAL
    QUIZ_QUESTION --> BUTTON
    
    UPLOAD_ZONE --> PROGRESS
    UPLOAD_ZONE --> SPINNER
    
    FADE_IN --> COURSE_CARD
    STAGGER --> CHAT_MESSAGE
    ANIMATED_PAGE --> MAIN
    FLOATING_BTN --> BUTTON
```

### 🎭 Theme & Animation System

```mermaid
graph LR
    subgraph "Theme System"
        CONTEXT[ThemeContext]
        TOGGLE[ThemeToggle]
        PROVIDER[ThemeProvider]
    end
    
    subgraph "Animation System"
        FRAMER[Framer Motion]
        VARIANTS[Animation Variants]
        TRANSITIONS[Transitions]
    end
    
    subgraph "Styling"
        TAILWIND[Tailwind CSS]
        CLASSES[CSS Classes]
        DARK[Dark Mode Classes]
    end
    
    PROVIDER --> CONTEXT
    CONTEXT --> TOGGLE
    TOGGLE --> TAILWIND
    TAILWIND --> CLASSES
    TAILWIND --> DARK
    
    FRAMER --> VARIANTS
    VARIANTS --> TRANSITIONS
    TRANSITIONS --> CLASSES
```

## 🔐 Authentication & Security

### 🛡️ Security Flow

```mermaid
graph TD
    subgraph "Frontend Security"
        TOKEN[JWT Token Storage]
        INTERCEPTOR[Axios Interceptor]
        GUARD[Route Guard]
        REFRESH[Token Refresh]
    end
    
    subgraph "Backend Security"
        MIDDLEWARE[Auth Middleware]
        JWT_VERIFY[JWT Verification]
        ROLE_CHECK[Role-based Access]
        BCRYPT[Password Hashing]
    end
    
    TOKEN --> INTERCEPTOR
    INTERCEPTOR --> GUARD
    GUARD --> REFRESH
    
    INTERCEPTOR -->|Authorization Header| MIDDLEWARE
    MIDDLEWARE --> JWT_VERIFY
    JWT_VERIFY --> ROLE_CHECK
    ROLE_CHECK -->|Access Granted| INTERCEPTOR
    
    BCRYPT --> JWT_VERIFY
```

### 🔄 Token Refresh Flow

```mermaid
sequenceDiagram
    participant FE as Frontend
    participant STORE as Auth Store
    participant API as API Client
    participant BE as Backend
    
    FE->>API: Request with Expired Token
    API->>BE: HTTP Request
    BE->>API: 401 Unauthorized
    API->>STORE: Token Expired
    STORE->>API: Refresh Token Request
    API->>BE: POST /api/v1/auth/refresh
    BE->>API: New Access Token
    API->>STORE: Update Token
    STORE->>API: Retry Original Request
    API->>BE: Request with New Token
    BE->>API: Success Response
    API->>FE: Data
```

## 📊 Database Schema Relationships

### 🗄️ MongoDB Collections

```mermaid
erDiagram
    User ||--o{ Course : creates
    User ||--o{ Upload : uploads
    User ||--o{ ChatSession : starts
    User ||--o{ QuizHistory : takes
    User ||--o{ Progress : tracks
    
    Course ||--o{ Quiz : generates
    Course ||--o{ ChatSession : discusses
    Course ||--o{ Progress : measures
    
    Upload ||--o{ Quiz : generates
    Upload ||--o{ ChatSession : discusses
    
    Quiz ||--o{ QuizHistory : records
    
    ChatSession ||--o{ ChatMessage : contains
    
    User {
        ObjectId id PK
        string email UK
        string password_hash
        string name
        string role
        boolean is_active
        datetime created_at
        datetime updated_at
    }
    
    Course {
        ObjectId id PK
        ObjectId owner_id FK
        string title
        string description
        string outline
        string level
        array tags
        datetime created_at
        datetime updated_at
    }
    
    Quiz {
        ObjectId id PK
        ObjectId course_id FK
        string title
        array questions
        datetime created_at
    }
    
    ChatSession {
        ObjectId id PK
        ObjectId user_id FK
        ObjectId course_id FK
        ObjectId upload_id FK
        string title
        string mode
        string status
        datetime created_at
    }
    
    Upload {
        ObjectId id PK
        ObjectId user_id FK
        string filename
        string file_type
        string status
        string extracted_text
        datetime created_at
    }
```

## 🚀 Deployment Architecture

### 🌐 Production Setup

```mermaid
graph TB
    subgraph "Frontend Deployment"
        VERCEL[Vercel/Netlify]
        CDN[CDN Distribution]
        DNS[Custom Domain]
    end
    
    subgraph "Backend Deployment"
        DOCKER[Docker Container]
        API_SERVER[FastAPI Server]
        NGINX[Nginx Reverse Proxy]
    end
    
    subgraph "Database"
        MONGO_ATLAS[MongoDB Atlas]
        VECTOR_SEARCH[Vector Search Index]
    end
    
    subgraph "External Services"
        GOOGLE_AI[Google GenAI API]
        EMAIL[Email Service]
        STORAGE[File Storage]
    end
    
    DNS --> CDN
    CDN --> VERCEL
    VERCEL -->|API Calls| NGINX
    NGINX --> DOCKER
    DOCKER --> API_SERVER
    API_SERVER --> MONGO_ATLAS
    API_SERVER --> VECTOR_SEARCH
    API_SERVER --> GOOGLE_AI
    API_SERVER --> EMAIL
    API_SERVER --> STORAGE
```

### 🔄 CI/CD Pipeline

```mermaid
graph LR
    subgraph "Development"
        DEV[Developer]
        GIT[Git Repository]
    end
    
    subgraph "CI/CD"
        GITHUB[GitHub Actions]
        BUILD[Build & Test]
        DEPLOY[Deploy]
    end
    
    subgraph "Production"
        FE_PROD[Frontend Production]
        BE_PROD[Backend Production]
        DB_PROD[Database]
    end
    
    DEV --> GIT
    GIT --> GITHUB
    GITHUB --> BUILD
    BUILD --> DEPLOY
    DEPLOY --> FE_PROD
    DEPLOY --> BE_PROD
    DEPLOY --> DB_PROD
```

## 📈 Performance & Monitoring

### 🔍 Monitoring Stack

```mermaid
graph TD
    subgraph "Frontend Monitoring"
        WEB_VITALS[Web Vitals]
        ERROR_TRACKING[Error Tracking]
        ANALYTICS[User Analytics]
    end
    
    subgraph "Backend Monitoring"
        API_METRICS[API Metrics]
        ERROR_LOGS[Error Logs]
        PERFORMANCE[Performance Monitoring]
    end
    
    subgraph "Infrastructure"
        HEALTH_CHECKS[Health Checks]
        UPTIME[Uptime Monitoring]
        ALERTS[Alert System]
    end
    
    WEB_VITALS --> ANALYTICS
    ERROR_TRACKING --> ERROR_LOGS
    API_METRICS --> PERFORMANCE
    HEALTH_CHECKS --> UPTIME
    UPTIME --> ALERTS
```

---

## 🎯 Kết luận

Hệ thống AI Learning Platform được thiết kế với kiến trúc:

✅ **Frontend**: Modern React + TypeScript với Zustand state management  
✅ **Backend**: FastAPI + MongoDB với AI integration  
✅ **Security**: JWT authentication với role-based access control  
✅ **Performance**: Optimized với lazy loading và caching  
✅ **Scalability**: Microservices-ready architecture  
✅ **Monitoring**: Comprehensive logging và error tracking  

**🚀 Sẵn sàng cho production deployment!**
