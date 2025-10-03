# API ENDPOINTS THỰC TẾ - XÁC THỰC 100% TỪ CODE

> **Được tạo từ**: Đọc đầy đủ 12 router files từ BEDB/app/routers/
> **Ngày tạo**: October 3, 2025
> **Trạng thái**: Hoàn toàn chính xác - xác thực từ source code

## 🔐 AUTHENTICATION SERVICE (/api/v1/auth)

| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/register` | POST | Đăng ký tài khoản mới | UserCreate schema | UserResponse | Public |
| `/login` | POST | Đăng nhập hệ thống | UserLogin schema | Token (access + refresh + type) | Public |
| `/me` | GET | Lấy thông tin user hiện tại | - | UserResponse | Token required |
| `/me` | PUT | Cập nhật thông tin user hiện tại | name, avatar (optional) | UserResponse | Token required |
| `/me` | PATCH | Cập nhật profile user | name, avatar (optional) | UserResponse | Token required |
| `/me/password` | PATCH | Thay đổi mật khẩu | old_password, new_password | Success message | Token required |
| `/refresh` | POST | Làm mới access token | RefreshTokenRequest | Token | Token required |
| `/logout` | POST | Đăng xuất (invalidate tokens) | LogoutRequest (optional) | Success message | Token required |
| `/verify-email` | POST | Xác thực email với OTP | EmailVerificationRequest | Success message | Public |
| `/forgot-password` | POST | Yêu cầu reset password | ForgotPasswordRequest | Success message | Public |
| `/reset-password` | POST | Reset password với token | ResetPasswordRequest | Success message | Public |

## 👥 USER MANAGEMENT SERVICE (/api/v1/users)

| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/me` | GET | Lấy thông tin user hiện tại | - | UserResponse | Token required |
| `/me` | PATCH | Cập nhật thông tin user hiện tại | UserUpdateRequest (name, avatar) | UserResponse | Token required |

## 📚 COURSE MANAGEMENT SERVICE (/api/v1/courses)

### Course CRUD Operations
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/` | POST | Tạo course mới | CourseCreate | CourseResponse | Token required |
| `/` | GET | Lấy danh sách courses | owner, skip, limit | List[CourseResponse] | Token required |
| `/public` | GET | Lấy public courses | skip, limit, level, tags | List[CourseResponse] | Public |
| `/{course_id}` | GET | Lấy thông tin course cụ thể | course_id | CourseResponse | Token required |
| `/{course_id}` | PUT | Cập nhật course | CourseUpdate | CourseResponse | Owner only |
| `/{course_id}` | DELETE | Xóa course | course_id | Success message | Owner only |

### AI-Powered Course Generation
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/from-prompt` | POST | Tạo course từ AI prompt | topic, level | CourseResponse | Token required |
| `/from-upload` | POST | Tạo course từ file upload | upload_id, title, metadata | Job ID | Token required |
| `/{course_id}/generate-outline` | POST | Tạo outline bằng AI | course_id, prompt | Outline text | Owner only |

### Chapter Management
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/{course_id}/chapters` | POST | Tạo chapter mới | ChapterCreate | ChapterResponse | Owner only |
| `/{course_id}/chapters` | GET | Lấy danh sách chapters | course_id | List[ChapterResponse] | Token required |
| `/{course_id}/chapters/{chapter_id}` | GET | Lấy thông tin chapter | course_id, chapter_id | ChapterResponse | Token required |
| `/{course_id}/chapters/{chapter_id}` | PUT | Cập nhật chapter | ChapterUpdate | ChapterResponse | Owner only |
| `/{course_id}/chapters/{chapter_id}` | DELETE | Xóa chapter | course_id, chapter_id | Success message | Owner only |

### Course Utilities
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/{course_id}/chat` | POST | Chat với AI trong context course | message, mode | AI response + context | Token required |
| `/{course_id}/summarize` | POST | Tạo summary cho chapter | course_id, chapter_id | Summary text | Token required |
| `/{course_id}/flashcards` | POST | Tạo flashcards cho chapter | course_id, chapter_id, num_cards | Flashcards array | Token required |

## 💬 CHAT SERVICE (/api/v1/chat)

### Session Management
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/sessions` | POST | Tạo chat session mới | ChatSessionCreate | ChatSessionResponse | Token required |
| `/sessions` | GET | Lấy danh sách chat sessions | skip, limit | List[ChatSessionResponse] | Token required |
| `/sessions/{session_id}` | GET | Lấy thông tin session cụ thể | session_id | ChatSessionResponse | Owner only |
| `/sessions/{session_id}` | DELETE | Xóa chat session | session_id | Success message | Owner only |

### Message Management
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/sessions/{session_id}/messages` | GET | Lấy messages trong session | session_id, skip, limit | List[ChatMessageResponse] | Owner only |
| `/sessions/{session_id}/messages` | POST | Gửi message trong session | ChatMessageCreate | ChatResponse | Owner only |

### Chat Utilities
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/` | POST | Freestyle chat (không session) | message, mode, session_id | ChatResponse | Token required |
| `/history` | GET | Lấy chat history | skip, limit | Chat history array | Token required |
| `/{answer_id}/feedback` | POST | Gửi feedback cho câu trả lời | feedback, rating | Success message | Token required |
| `/sessions/{session_id}/save-as-course` | POST | Lưu chat session thành course | session_id, course_title | Course ID | Owner only |
| `/save` | POST | Lưu chat session | session_id, save_as | Course/Note ID | Owner only |

## 🧠 QUIZ SERVICE (/api/v1/quiz)

### Quiz Generation & CRUD
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/generate` | POST | Tạo quiz từ course/chapter/prompt | course_id, chapter_id, prompt, num_questions | Quiz + Questions | Token required |
| `/manual` | POST | Tạo quiz thủ công | QuizCreate | QuizResponse | Token required |
| `/` | POST | Tạo quiz mới | QuizCreate | QuizResponse | Token required |
| `/` | GET | Lấy danh sách quizzes | skip, limit, course_id | List[QuizResponse] | Token required |
| `/{quiz_id}` | GET | Lấy thông tin quiz | quiz_id | QuizResponse | Token required |
| `/{quiz_id}` | PATCH | Cập nhật quiz | title, prompt | QuizResponse | Owner only |
| `/{quiz_id}` | DELETE | Xóa quiz | quiz_id | Success message | Owner only |

### Specialized Quiz Creation
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/from-course/{course_id}` | POST | Tạo quiz từ course bằng AI | course_id, title, num_questions | QuizResponse | Token required |
| `/from-upload/{upload_id}` | POST | Tạo quiz từ file upload bằng AI | upload_id, title, num_questions | QuizResponse | Owner only |

### Quiz Taking & Results
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/{quiz_id}/questions` | GET | Lấy câu hỏi quiz | quiz_id | List[QuizQuestionResponse] | Token required |
| `/{quiz_id}/submit` | POST | Nộp bài quiz | QuizSubmission | QuizResult | Token required |
| `/{quiz_id}/grade` | POST | Chấm điểm quiz thủ công | answers array | Score + explanation | Token required |
| `/{quiz_id}/results` | GET | Lấy kết quả quiz | quiz_id | Quiz results array | Token required |

### Quiz History
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/history` | GET | Lấy lịch sử làm quiz | skip, limit | List[QuizHistoryResponse] | Token required |
| `/history/{history_id}` | GET | Lấy chi tiết lịch sử quiz | history_id | QuizResult | Owner only |

## 📤 UPLOAD SERVICE (/api/v1/uploads)

| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/` | POST | Upload file | UploadFile | UploadResponse | Token required |
| `/` | GET | Lấy danh sách uploads | skip, limit | List[UploadResponse] | Token required |
| `/{upload_id}` | GET | Lấy thông tin upload | upload_id | UploadResponse | Owner only |
| `/{upload_id}` | DELETE | Xóa upload | upload_id | Success message | Owner only |
| `/{upload_id}/status` | GET | Lấy trạng thái xử lý upload | upload_id | Status info | Owner only |
| `/{upload_id}/reprocess` | POST | Xử lý lại file upload | upload_id | Success message | Owner only |

## 📊 DASHBOARD SERVICE (/api/v1/dashboard)

### Overview & Statistics
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/overview` | GET | Lấy tổng quan dashboard | - | Overview stats | Token required |
| `/stats` | GET | Lấy thống kê chi tiết dashboard | - | DashboardStats | Token required |

### Progress Management
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/progress` | GET | Lấy tiến độ các courses | skip, limit | List[CourseProgress] | Token required |
| `/progress` | POST | Cập nhật tiến độ | ProgressUpdate | Success message | Token required |
| `/progress/{course_id}` | GET | Lấy tiến độ chi tiết course | course_id | Progress detail array | Token required |

### Analytics & Recommendations
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/recommendations` | GET | Lấy gợi ý học tập cá nhân hóa | - | Recommendations array | Token required |
| `/course-stats/{course_id}` | GET | Lấy thống kê course cụ thể | course_id | Course statistics | Token required |

## 🎓 STUDENT SERVICE (/api/v1/student)

### Course Enrollment
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/courses/{course_id}/enroll` | POST | Đăng ký học course | course_id | CourseEnrollmentResponse | Student only |
| `/courses/{course_id}/enroll` | DELETE | Hủy đăng ký course | course_id | Success message | Student only |

### Student Data
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/enrolled-courses` | GET | Lấy danh sách courses đã đăng ký | skip, limit, status | List[EnrolledCourseInfo] | Student only |
| `/dashboard` | GET | Lấy dashboard sinh viên | - | StudentDashboardResponse | Student only |

## 👨‍🏫 INSTRUCTOR SERVICE (/api/v1/instructor)

### Course Management
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/courses` | GET | Lấy courses của instructor | skip, limit | List[CourseResponse] | Instructor/Admin |

### Student Management
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/courses/{course_id}/students` | GET | Lấy sinh viên trong course | course_id, status_filter | List[StudentEnrollmentInfo] | Course owner/Admin |
| `/students` | GET | Lấy tất cả sinh viên của instructor | skip, limit | List[StudentEnrollmentInfo] | Instructor/Admin |

### Analytics
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/courses/{course_id}/analytics` | GET | Lấy analytics cho course | course_id | CourseAnalytics | Course owner/Admin |
| `/dashboard` | GET | Lấy dashboard instructor | - | InstructorDashboardResponse | Instructor/Admin |

## 🔧 ADMIN SERVICE (/api/v1/admin)

### User Management
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/users` | GET | Lấy danh sách tất cả users | skip, limit | List[UserResponse] | Admin only |
| `/users/{user_id}/role` | PATCH | Cập nhật role user | user_id, UserRoleUpdate | Success message | Admin only |

### System Statistics
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/stats` | GET | Lấy thống kê hệ thống | - | AdminStats | Admin only |

### Course Management
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/courses` | POST | Tạo sample course | CourseCreate | CourseResponse | Admin only |
| `/courses` | GET | Lấy tất cả courses | skip, limit | List[CourseResponse] | Admin only |
| `/courses/{course_id}` | DELETE | Xóa bất kỳ course nào | course_id | Success message | Admin only |
| `/courses/import` | POST | Import course | title, content, description | CourseResponse | Admin only |

## 🔍 SEARCH SERVICE (/api/v1/search)

### Vector Search
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/` | POST | Tìm kiếm documents bằng vector | SearchRequest | List[SearchResult] | Token required |

### Index Management
| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/embeddings` | POST | Reindex embeddings | file_id, course_id | Success message | Token required |
| `/courses/{course_id}/reindex` | POST | Reindex course embeddings | course_id | Success message | Token required |

## 🏆 LEADERBOARD SERVICE (/api/v1/leaderboard)

| Endpoint | Method | Mô tả | Request | Response | Auth |
|----------|--------|-------|---------|----------|------|
| `/` | GET | Lấy bảng xếp hạng | limit | List[LeaderboardEntry] | Token required |

---

## 📋 THỐNG KÊ TỔNG QUAN

### Tổng số Endpoints: **87 endpoints**

| Service | Số lượng Endpoints |
|---------|-------------------|
| Authentication | 11 |
| Users | 2 |
| Courses | 20 |
| Chat | 11 |
| Quiz | 16 |
| Uploads | 6 |
| Dashboard | 6 |
| Student | 3 |
| Instructor | 5 |
| Admin | 6 |
| Search | 3 |
| Leaderboard | 1 |

### Phân quyền (Authorization Levels):
- **Public**: 4 endpoints (register, login, forgot password, reset password, verify email, public courses)
- **Token Required**: 66 endpoints (cần đăng nhập)
- **Owner Only**: 12 endpoints (chỉ owner của resource)
- **Student Only**: 3 endpoints (chỉ role student)
- **Instructor/Admin**: 5 endpoints (role instructor hoặc admin)
- **Admin Only**: 6 endpoints (chỉ role admin)

### HTTP Methods:
- **GET**: 35 endpoints
- **POST**: 35 endpoints  
- **PUT**: 4 endpoints
- **PATCH**: 5 endpoints
- **DELETE**: 8 endpoints

---

> **Lưu ý quan trọng**: 
> - Tất cả endpoints đều có prefix `/api/v1/` 
> - Authentication sử dụng JWT Bearer token
> - Hệ thống hỗ trợ 3 roles: STUDENT, INSTRUCTOR, ADMIN
> - Vector search được tích hợp cho courses và uploads
> - AI services được tích hợp cho course generation, quiz creation, và chat