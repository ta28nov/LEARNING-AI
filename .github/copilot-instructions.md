# AI Learning Platform - Copilot Instructions

## 🎯 Project Overview

**AI-powered learning platform** with dual frontend-backend architecture:
- **Frontend**: React 18 + TypeScript + Zustand state management
- **Backend**: FastAPI + MongoDB + Google GenAI integration
- **Core Features**: AI course generation, intelligent chat, quiz system, file processing, progress tracking

## 🏗️ Architecture Fundamentals

### Monorepo Structure
```
LEARNING-AI/
├── BEDB/                    # Backend (FastAPI + MongoDB)
│   └── app/
│       ├── routers/         # API endpoints (auth, courses, chat, quiz, etc.)
│       ├── models/          # Beanie ODM models
│       ├── schemas/         # Pydantic request/response schemas
│       └── services/        # Business logic (genai, file, vector)
├── learning-app-fe/         # Frontend (React + TypeScript)
│   └── src/
│       ├── pages/           # Route components
│       ├── components/      # Reusable UI components
│       ├── stores/          # Zustand state management
│       ├── services/        # API integration layer
│       └── i18n/            # Internationalization (vi/en)
└── tailieubosung/           # Project documentation and rules
```

### Data Flow Pattern
**Frontend → Service → API Router → Business Service → Model → MongoDB**

Example flow for course creation:
1. User action in `CoursesPage.tsx`
2. Zustand store action (`courseStore.ts`)
3. API service call (`courseService.ts`)
4. Backend router handles request (`BEDB/app/routers/courses.py`)
5. Google GenAI service generates content (`BEDB/app/services/genai_service.py`)
6. Beanie model saves to MongoDB (`BEDB/app/models/course.py`)

## 🔧 Critical Development Workflows

### Backend Development (BEDB/)

**Running the API:**
```bash
# Development mode with auto-reload
cd BEDB
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Initialize database with sample data
python scripts/init_database.py
```

**Adding New Endpoints:**
1. Define Pydantic schemas in `app/schemas/`
2. Create/update Beanie models in `app/models/`
3. Implement router logic in `app/routers/`
4. Register router in `app/main.py` with `/api/v1/` prefix
5. Update API documentation in `API_DOCUMENTATION.md`

**Database Operations:**
```python
# Always use Beanie ODM async patterns
from app.models.course import Course

# Query examples
course = await Course.find_one(Course.id == course_id)
courses = await Course.find(Course.owner_id == user_id).to_list()
await course.insert()  # Create
await course.save()     # Update
await course.delete()   # Delete
```

### Frontend Development (learning-app-fe/)

**Running the Development Server:**
```bash
cd learning-app-fe
npm install
npm run dev  # Starts on http://localhost:3000
```

**State Management Pattern (Zustand):**
```typescript
// In stores/ - Always use this pattern
const useMyStore = create<MyState>()(
  persist(
    (set, get) => ({
      items: [],
      isLoading: false,
      
      fetchItems: async () => {
        set({ isLoading: true });
        try {
          const data = await myService.getItems();
          set({ items: data, isLoading: false });
        } catch (error) {
          set({ isLoading: false });
          // Error handled by API client
        }
      },
    }),
    { name: 'my-storage' }
  )
);
```

**API Integration Pattern:**
```typescript
// In services/ - Always use apiClient from ./api.ts
export const myService = {
  async getItems(): Promise<Item[]> {
    return apiClient.get('/api/v1/items');
  },
  
  async createItem(data: CreateItemData): Promise<Item> {
    return apiClient.post('/api/v1/items', data);
  },
};
```

## 📋 Project-Specific Conventions

### Backend Conventions

**1. Router Structure:**
- All routes prefixed with `/api/v1/`
- Use dependency injection for auth: `current_user: User = Depends(get_current_user)`
- Return Pydantic schemas, not raw models
- Always validate input with schemas

**2. Service Layer Pattern:**
```python
# Business logic in services/, not routers
class GenAIService:
    async def generate_course_outline(self, topic: str, level: str) -> str:
        # AI logic here
        pass
```

**3. Error Handling:**
```python
from fastapi import HTTPException

# Use HTTPException for expected errors
if not course:
    raise HTTPException(status_code=404, detail="Course not found")
```

**4. MongoDB Indexes:**
- Always define indexes in model `Settings` class
- Use compound indexes for common queries
- Vector search index required for embeddings collection

### Frontend Conventions

**1. Component Organization:**
```typescript
// Base UI components in components/ui/
// Feature components in pages/
// Reusable layouts in components/layout/
```

**2. Translation Keys:**
```typescript
// Always use i18n for user-facing text
const { t } = useTranslation();
return <h1>{t('dashboard.title')}</h1>;

// Add keys to both locales/vi.json and locales/en.json
```

**3. Theme-Aware Styling:**
```typescript
// Use dark: prefix for dark mode styles
<div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white">
```

**4. Animation Components:**
```typescript
// Wrap animated content with FadeIn or StaggerContainer
import { FadeIn } from '@/components/ui/FadeIn';

<FadeIn direction="up" delay={0.2}>
  <Card>Content</Card>
</FadeIn>
```

## 🔌 API Integration Points

### Authentication Flow
- JWT tokens stored in authStore
- Axios interceptor adds `Authorization: Bearer <token>` header
- Auto token refresh on 401 responses
- Protected routes use `<ProtectedRoute>` wrapper

### Key API Endpoints
```
POST   /api/v1/auth/login                      # Login
POST   /api/v1/auth/register                   # Register
GET    /api/v1/courses                         # List courses
POST   /api/v1/courses/from-prompt             # AI course generation
POST   /api/v1/chat/freestyle                  # AI chat
POST   /api/v1/quiz/from-course/{course_id}    # Generate quiz
POST   /api/v1/uploads                         # File upload
GET    /api/v1/dashboard/stats                 # Dashboard data
```

### File Upload Handling
- Max size: 10MB
- Supported: PDF, DOCX, TXT
- Backend extracts text and creates embeddings
- Status tracking: `pending` → `processing` → `completed`

## 🤖 Google GenAI Integration

### Usage Patterns
```python
# In services/genai_service.py
from app.services.genai_service import GenAIService

genai = GenAIService()

# Course generation
outline = await genai.generate_course_outline(topic, level, num_chapters)

# Quiz generation
questions = await genai.generate_quiz_questions(content, num_questions)

# Chat responses
answer = await genai.chat_response(message, context, mode="strict|hybrid")
```

### Chat Modes
- **Strict Mode**: Answers only from provided context (course/upload content)
- **Hybrid Mode**: Combines context with general AI knowledge

## 🗄️ Database Schema Patterns

### User Roles
```python
# role field: "student" | "instructor" | "admin"
# Always check role for admin endpoints
```

### Course Source Types
```python
# source field: "manual" | "ai_generated" | "from_upload"
```

### Progress Tracking
```python
# DashboardProgress model tracks:
# - course_id, chapter_id (optional)
# - status: "not_started" | "in_progress" | "completed"
# - progress: 0.0-100.0 (float)
# - time_spent: minutes (int)
```

### Vector Search
```python
# Embeddings collection structure:
{
  "source_id": ObjectId,      # Course or Upload ID
  "source_type": str,         # "course" | "upload"
  "chunk_index": int,
  "text": str,
  "embedding": array,         # Vector embedding
  "created_at": datetime
}
```

## 🚦 Testing and Debugging

### Backend Testing
```bash
# Run all tests
cd BEDB
pytest

# Test specific file
pytest tests/test_courses.py

# Interactive API testing
# Visit http://localhost:8000/docs
```

### Frontend Testing
```bash
cd learning-app-fe
npm run test        # Unit tests
npm run test:e2e    # E2E tests (when available)
npm run lint        # ESLint check
```

### Common Issues
- **CORS errors**: Check `ALLOWED_ORIGINS` in `.env`
- **Auth failures**: Verify JWT token in localStorage
- **AI errors**: Validate `GOOGLE_API_KEY` environment variable
- **File upload failures**: Check `uploads/` directory permissions

## 📦 Deployment Considerations

### Environment Variables
**Backend (.env):**
```bash
MONGODB_URL=mongodb+srv://...
DATABASE_NAME=ai_learning_platform
JWT_SECRET_KEY=<secret>
GOOGLE_API_KEY=<key>
ALLOWED_ORIGINS=["http://localhost:3000"]
```

**Frontend (.env):**
```bash
VITE_API_URL=http://localhost:8000
```

### Docker Deployment
```bash
# Backend
cd BEDB
docker build -t ai-learning-backend .
docker-compose up -d

# Frontend
cd learning-app-fe
npm run build
# Deploy dist/ to Vercel/Netlify
```

## 🔒 Security Requirements

1. **Always validate user input** with Pydantic schemas
2. **Never expose raw password_hash** in responses
3. **Use parameterized queries** (Beanie handles this)
4. **Validate file types** before processing uploads
5. **Check user ownership** before update/delete operations
6. **Rate limit** AI service calls (production)

## 🎨 UI/UX Standards

- **Responsive breakpoints**: mobile (<640px), tablet (640-1024px), desktop (>1024px)
- **Dark mode**: All components must support dark theme
- **Loading states**: Show spinners during async operations
- **Error messages**: Display user-friendly errors via toast notifications
- **Animations**: Use Framer Motion for page transitions and interactive elements
- **Accessibility**: Include ARIA labels and keyboard navigation

## 📚 Key Files to Reference

When working on specific features, refer to these exemplar files:

- **API Router Pattern**: `BEDB/app/routers/courses.py`
- **Zustand Store Pattern**: `learning-app-fe/src/stores/courseStore.ts`
- **Service Integration**: `learning-app-fe/src/services/courseService.ts`
- **AI Service Usage**: `BEDB/app/services/genai_service.py`
- **UI Component Pattern**: `learning-app-fe/src/components/ui/Button.tsx`
- **Page Layout**: `learning-app-fe/src/pages/courses/CoursesPage.tsx`

## ⚠️ Important Rules

1. **Modular-First**: Break logic into small, reusable components/modules
2. **Test-Driven**: Write tests before implementing features (when applicable)
3. **Incremental**: One module/feature at a time, confirm before proceeding
4. **Documentation**: Update relevant MD files when changing architecture
5. **Context-Aware**: Check existing patterns before implementing new solutions
6. **Version Stable**: Only use stable, verified dependencies
7. **Type Safety**: Use TypeScript/Pydantic for all data structures
8. **Consistent Naming**: Follow existing naming conventions in each layer

## 🔄 Common Task Patterns

### Adding a New Feature End-to-End

**Example: Add "Course Rating" feature**

1. **Backend Model** (`BEDB/app/models/course.py`):
```python
class CourseRating(Document):
    course_id: PydanticObjectId
    user_id: PydanticObjectId
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

2. **Backend Schema** (`BEDB/app/schemas/course.py`):
```python
class CourseRatingCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None

class CourseRatingResponse(BaseModel):
    id: str
    course_id: str
    rating: int
    comment: Optional[str]
    created_at: datetime
```

3. **Backend Router** (`BEDB/app/routers/courses.py`):
```python
@router.post("/{course_id}/rate", response_model=CourseRatingResponse)
async def rate_course(
    course_id: str,
    rating_data: CourseRatingCreate,
    current_user: User = Depends(get_current_user)
):
    # Implementation
```

4. **Frontend Type** (`learning-app-fe/src/types/index.ts`):
```typescript
export interface CourseRating {
  id: string;
  course_id: string;
  rating: number;
  comment?: string;
  created_at: string;
}
```

5. **Frontend Service** (`learning-app-fe/src/services/courseService.ts`):
```typescript
async rateCourse(courseId: string, rating: number, comment?: string): Promise<CourseRating> {
  return apiClient.post(`/api/v1/courses/${courseId}/rate`, { rating, comment });
}
```

6. **Frontend Store** (`learning-app-fe/src/stores/courseStore.ts`):
```typescript
rateCourse: async (courseId: string, rating: number, comment?: string) => {
  try {
    const result = await courseService.rateCourse(courseId, rating, comment);
    // Update state
    return result;
  } catch (error) {
    // Handle error
  }
}
```

7. **Frontend Component** (in relevant page/component):
```typescript
const { rateCourse } = useCourseStore();
const handleRating = async (rating: number) => {
  await rateCourse(courseId, rating);
  toast.success(t('course.ratingSuccess'));
};
```

8. **Add Translations** (both `vi.json` and `en.json`):
```json
{
  "course": {
    "ratingSuccess": "Đánh giá thành công! / Rating submitted successfully!"
  }
}
```

---

**Generated for GitHub Copilot**: This file guides AI agents to be immediately productive in the LEARNING-AI codebase by documenting architecture, workflows, conventions, and integration patterns specific to this project.
