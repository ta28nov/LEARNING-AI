# Phân Tích và Yêu Cầu Cập Nhật Hệ Thống

## 📊 Phân Tích Hiện Trạng

### ✅ Đã Có Trong Hệ Thống

#### 1. **Roles System**
- ✅ 3 roles: `student`, `instructor`, `admin` (trong `UserRole` enum)
- ✅ Admin có endpoints riêng tại `/api/v1/admin/*`
- ✅ Role check qua `get_admin_user` dependency

#### 2. **Course Management**
- ✅ CRUD operations cho courses
- ✅ AI-generated courses từ prompt
- ✅ Course từ file upload
- ✅ Owner-based access control (chỉ owner hoặc admin mới xóa/sửa)

#### 3. **Authentication**
- ✅ JWT-based authentication
- ✅ Register, Login, Logout
- ✅ Password change
- ✅ Profile update

#### 4. **File Upload**
- ✅ Upload PDF, DOCX, TXT
- ✅ Text extraction
- ✅ Vector embeddings

#### 5. **Quiz System**
- ✅ AI-generated quizzes
- ✅ Quiz submission và grading
- ✅ Quiz history tracking

#### 6. **Chat System**
- ✅ Freestyle chat
- ✅ Course-specific chat
- ✅ Strict và Hybrid modes

#### 7. **Dashboard**
- ✅ Progress tracking
- ✅ Statistics
- ✅ Learning recommendations

---

## 🎯 Yêu Cầu Cập Nhật Dựa Trên Flow Diagrams

### 1. **Instructor Role Enhancement**

#### 📝 Yêu Cầu
Theo `teacherflow.png`, instructor cần có quyền:
- Tạo và quản lý courses (đã có)
- Xem danh sách học sinh đăng ký khóa học của mình
- Quản lý nội dung chapters
- Tạo và quản lý quizzes cho courses của mình
- Xem báo cáo tiến độ học sinh

#### 🔧 Cần Bổ Sung
1. **Course Enrollment System**
   - Model: `CourseEnrollment` (student_id, course_id, enrolled_at, status)
   - API: `/api/v1/courses/{course_id}/enroll` (POST)
   - API: `/api/v1/courses/{course_id}/students` (GET - instructor only)

2. **Instructor-specific Course Management**
   - API: `/api/v1/instructor/courses` (GET - courses created by instructor)
   - API: `/api/v1/instructor/courses/{course_id}/students` (GET - enrolled students)
   - API: `/api/v1/instructor/courses/{course_id}/analytics` (GET - course analytics)

3. **Quiz Management for Instructors**
   - API: `/api/v1/instructor/quizzes` (GET - quizzes created by instructor)
   - API: `/api/v1/instructor/quizzes/{quiz_id}/results` (GET - student results)

---

### 2. **Student Role Enhancement**

#### 📝 Yêu Cầu
Theo `studentflow.png`, student cần có:
- Browse và enroll vào courses
- Xem tiến độ học tập của mình
- Làm quizzes và xem kết quả
- Chat với AI tutor
- Upload files để tạo courses

#### 🔧 Cần Bổ Sung
1. **Course Browsing & Enrollment**
   - API: `/api/v1/courses/public` (GET - browse public courses) ✅ Đã có
   - API: `/api/v1/courses/{course_id}/enroll` (POST - enroll in course)
   - API: `/api/v1/student/enrolled-courses` (GET - my enrolled courses)
   - API: `/api/v1/student/courses/{course_id}/unenroll` (DELETE - unenroll)

2. **Learning Progress**
   - API: `/api/v1/student/progress` (GET - my progress across all courses) ✅ Đã có phần này
   - API: `/api/v1/student/courses/{course_id}/progress` (GET - progress in specific course)

3. **Quiz Participation**
   - Current quiz APIs are already accessible to students ✅

---

### 3. **Admin Role Enhancement**

#### 📝 Yêu Cầu
Theo `adminflow.png`, admin cần có:
- Quản lý tất cả users (CRUD)
- Quản lý tất cả courses
- Xem thống kê hệ thống
- Approve/reject instructor applications

#### 🔧 Cần Bổ Sung
1. **User Management** ✅ Đã có cơ bản
   - API: `/api/v1/admin/users` (GET) ✅
   - API: `/api/v1/admin/users/{id}/role` (PATCH) ✅
   - Cần bổ sung: `/api/v1/admin/users/{id}` (DELETE - soft delete)
   - Cần bổ sung: `/api/v1/admin/users/{id}/activate` (PATCH - activate/deactivate)

2. **System Monitoring**
   - API: `/api/v1/admin/stats` ✅ Đã có
   - Cần bổ sung: `/api/v1/admin/analytics` (GET - detailed analytics)
   - Cần bổ sung: `/api/v1/admin/logs` (GET - system logs)

3. **Content Moderation**
   - Cần bổ sung: `/api/v1/admin/courses/{id}/approve` (PATCH)
   - Cần bổ sung: `/api/v1/admin/courses/{id}/reject` (PATCH)

---

### 4. **Course Visibility & Access Control**

#### 📝 Yêu Cầu
- Public courses: Ai cũng xem được, cần enroll để học
- Private courses: Chỉ owner và enrolled students
- Draft courses: Chỉ owner

#### 🔧 Cần Bổ Sung
1. **Course Model Update**
   ```python
   class CourseVisibility(str, Enum):
       PUBLIC = "public"
       PRIVATE = "private"
       DRAFT = "draft"
   
   class Course(BaseDocument):
       # ... existing fields
       visibility: CourseVisibility = CourseVisibility.DRAFT
       is_approved: bool = False  # For admin approval
   ```

2. **Access Control Logic**
   - Students chỉ xem được courses đã enroll
   - Instructors xem được courses của mình
   - Admin xem được tất cả

---

### 5. **Chapter Progress Tracking**

#### 📝 Yêu Cầu
- Track progress cho từng chapter
- Mark chapter as completed
- Calculate overall course progress

#### 🔧 Cần Bổ Sung
1. **ChapterProgress Model**
   ```python
   class ChapterProgress(BaseDocument):
       user_id: PyObjectId
       chapter_id: PyObjectId
       course_id: PyObjectId
       status: str  # "not_started", "in_progress", "completed"
       time_spent: int  # minutes
       last_accessed: datetime
   ```

2. **APIs**
   - API: `/api/v1/chapters/{chapter_id}/progress` (GET, POST)
   - API: `/api/v1/chapters/{chapter_id}/complete` (POST)

---

## 🔄 Luồng Hoạt Động Mới

### Student Flow
```
1. Register/Login
2. Browse Public Courses
3. Enroll in Course
4. View Course Content (Chapters)
5. Mark Chapters as Complete
6. Take Quizzes
7. Chat with AI Tutor
8. View Progress Dashboard
```

### Instructor Flow
```
1. Register/Login
2. Create Course (Draft)
3. Add Chapters to Course
4. Create Quizzes for Course
5. Publish Course (Public/Private)
6. View Enrolled Students
7. Monitor Student Progress
8. Grade Assignments (future)
```

### Admin Flow
```
1. Login (Admin account)
2. View System Statistics
3. Manage Users (CRUD, Change Roles)
4. Approve/Reject Courses
5. Monitor System Activity
6. Manage Content
```

---

## 📋 Danh Sách API Endpoints Cần Bổ Sung

### Course Enrollment
- `POST /api/v1/courses/{course_id}/enroll` - Enroll in course
- `DELETE /api/v1/courses/{course_id}/enroll` - Unenroll from course
- `GET /api/v1/courses/{course_id}/students` - Get enrolled students (instructor/admin)
- `GET /api/v1/student/enrolled-courses` - Get my enrolled courses

### Course Visibility
- `PATCH /api/v1/courses/{course_id}/visibility` - Change visibility (owner/admin)
- `PATCH /api/v1/courses/{course_id}/publish` - Publish course (owner/admin)

### Chapter Progress
- `GET /api/v1/chapters/{chapter_id}/progress` - Get chapter progress
- `POST /api/v1/chapters/{chapter_id}/progress` - Update chapter progress
- `POST /api/v1/chapters/{chapter_id}/complete` - Mark chapter complete

### Instructor Dashboard
- `GET /api/v1/instructor/dashboard` - Instructor dashboard stats
- `GET /api/v1/instructor/courses` - My courses as instructor
- `GET /api/v1/instructor/students` - All my students across courses
- `GET /api/v1/instructor/courses/{course_id}/analytics` - Course analytics

### Student Dashboard
- `GET /api/v1/student/dashboard` - Student dashboard
- `GET /api/v1/student/enrolled-courses` - Enrolled courses
- `GET /api/v1/student/progress` - Overall progress

### Admin Extensions
- `DELETE /api/v1/admin/users/{user_id}` - Soft delete user
- `PATCH /api/v1/admin/users/{user_id}/activate` - Activate/deactivate user
- `GET /api/v1/admin/analytics` - System analytics
- `PATCH /api/v1/admin/courses/{course_id}/approve` - Approve course
- `PATCH /api/v1/admin/courses/{course_id}/reject` - Reject course

---

## 🗄️ Database Schema Updates

### New Models

#### 1. CourseEnrollment
```python
class CourseEnrollment(BaseDocument):
    student_id: PyObjectId
    course_id: PyObjectId
    enrolled_at: datetime
    status: str  # "active", "completed", "dropped"
    progress: float  # 0-100
```

#### 2. ChapterProgress
```python
class ChapterProgress(BaseDocument):
    user_id: PyObjectId
    chapter_id: PyObjectId
    course_id: PyObjectId
    status: str  # "not_started", "in_progress", "completed"
    time_spent: int
    completed_at: Optional[datetime]
```

### Updated Models

#### Course
```python
class Course(BaseDocument):
    # ... existing fields
    visibility: CourseVisibility  # NEW
    is_approved: bool  # NEW
    approved_by: Optional[PyObjectId]  # NEW
    approved_at: Optional[datetime]  # NEW
    enrollment_count: int = 0  # NEW
```

---

## ✅ Ưu Tiên Triển Khai

### Phase 1: Core Enrollment System (Ưu tiên cao)
1. ✅ Tạo CourseEnrollment model
2. ✅ API enroll/unenroll courses
3. ✅ Update Course model với visibility
4. ✅ Student enrolled courses endpoint

### Phase 2: Progress Tracking Enhancement (Ưu tiên cao)
1. ✅ Tạo ChapterProgress model
2. ✅ Chapter progress APIs
3. ✅ Update Dashboard với detailed progress

### Phase 3: Role-specific Dashboards (Ưu tiên trung bình)
1. ✅ Instructor dashboard và analytics
2. ✅ Student dashboard enhancement
3. ✅ Admin analytics expansion

### Phase 4: Course Approval Workflow (Ưu tiên thấp)
1. ⏳ Admin course approval system
2. ⏳ Course visibility management
3. ⏳ Content moderation tools

---

## 🔐 Security & Permissions Matrix

| Endpoint | Student | Instructor | Admin |
|----------|---------|------------|-------|
| Create Course | ✅ | ✅ | ✅ |
| View Own Courses | ✅ | ✅ | ✅ |
| View All Courses | ❌ | ❌ | ✅ |
| Edit Own Course | ✅ | ✅ | ✅ |
| Edit Any Course | ❌ | ❌ | ✅ |
| Delete Own Course | ✅ | ✅ | ✅ |
| Delete Any Course | ❌ | ❌ | ✅ |
| Enroll in Course | ✅ | ❌ | ❌ |
| View Enrolled Students | ❌ | ✅ (own) | ✅ (all) |
| Change User Role | ❌ | ❌ | ✅ |
| Approve Course | ❌ | ❌ | ✅ |
| View Analytics | ✅ (own) | ✅ (own) | ✅ (all) |

---

## 📝 Ghi Chú Triển Khai

### 1. Backward Compatibility
- Các API hiện tại phải vẫn hoạt động
- Thêm endpoints mới, không sửa endpoints cũ
- Migration script cho database changes

### 2. Testing Requirements
- Unit tests cho mỗi endpoint mới
- Integration tests cho enrollment flow
- Permission tests cho role-based access

### 3. Documentation Updates
- API_DOCUMENTATION.md
- BACKEND_ARCHITECTURE.md
- SYSTEM_OVERVIEW.md
- Copilot instructions

---

Tài liệu này sẽ được sử dụng làm reference cho việc triển khai các thay đổi trong hệ thống.
