# SO SÁNH API ENDPOINTS: DOCUMENTED vs THỰC TẾ

> **Mục đích**: Phân tích sự khác biệt giữa API endpoints được ghi chép trong SYSTEM_OVERVIEW.md và code thực tế
> **Ngày tạo**: October 3, 2025
> **Trạng thái**: Hoàn chỉnh - dựa trên phân tích chi tiết 12 router files

## 📊 TỔNG QUAN KHÁC BIỆT

### 📈 Thống Kê Endpoints

| Loại | SYSTEM_OVERVIEW.md | Thực Tế (Code) | Chênh Lệch |
|------|-------------------|-----------------|-------------|
| **Tổng Endpoints** | ~45 endpoints | **87 endpoints** | **+42 endpoints** |
| **Authentication** | 8 endpoints | **11 endpoints** | **+3 endpoints** |
| **Course Management** | 12 endpoints | **20 endpoints** | **+8 endpoints** |
| **Chat System** | 7 endpoints | **11 endpoints** | **+4 endpoints** |
| **Quiz System** | 6 endpoints | **16 endpoints** | **+10 endpoints** |
| **File Upload** | 4 endpoints | **6 endpoints** | **+2 endpoints** |
| **Dashboard** | 5 endpoints | **6 endpoints** | **+1 endpoint** |
| **Missing Services** | 0 | **6 services** | **+6 services** |

### 🚨 Các Service Bị Thiếu Hoàn Toàn

| Service | Số Endpoints | Mô Tả |
|---------|-------------|--------|
| **Student Service** | 3 endpoints | Hệ thống enrollment hoàn chỉnh |
| **Instructor Service** | 5 endpoints | Dashboard và analytics cho giảng viên |
| **Admin Service** | 6 endpoints | Quản lý hệ thống và người dùng |
| **Search Service** | 3 endpoints | Vector search và reindexing |
| **Leaderboard Service** | 1 endpoint | Bảng xếp hạng người dùng |
| **Users Service** | 2 endpoints | User profile management |

---

## 🔍 PHÂN TÍCH CHI TIẾT TỪNG SERVICE

### 🔐 1. AUTHENTICATION SERVICE

#### ✅ Endpoints Có Trong Cả Hai
| Endpoint | Documented | Thực Tế | Trạng Thái |
|----------|------------|---------|------------|
| `POST /register` | ✅ | ✅ | **Khớp** |
| `POST /login` | ✅ | ✅ | **Khớp** |
| `GET /me` | ✅ | ✅ | **Khớp** |
| `PUT /me` | ✅ | ✅ | **Khớp** |

#### ❌ Endpoints Thiếu Trong Documentation
| Endpoint | Method | Mô Tả |
|----------|--------|--------|
| `/refresh` | POST | Làm mới JWT access token |
| `/logout` | POST | Đăng xuất và invalidate tokens |
| `/verify-email` | POST | Xác thực email với OTP |
| `/forgot-password` | POST | Gửi email reset password |
| `/reset-password` | POST | Reset password với token |
| `/me` | PATCH | Cập nhật profile (duplicate PUT) |
| `/me/password` | PATCH | Thay đổi mật khẩu |

#### 🔴 Endpoints Sai Trong Documentation
| Documented | Thực Tế | Vấn Đề |
|------------|---------|--------|
| `POST /refresh` | `POST /refresh` | **Parameter schema khác** |
| - | `PATCH /me/password` | **Thiếu hoàn toàn** |

---

### 📚 2. COURSE MANAGEMENT SERVICE

#### ✅ Endpoints Có Trong Cả Hai
| Endpoint | Documented | Thực Tế | Trạng Thái |
|----------|------------|---------|------------|
| `GET /courses` | ✅ | ✅ | **Khớp** |
| `POST /courses` | ✅ | ✅ | **Khớp** |
| `GET /courses/{id}` | ✅ | ✅ | **Khớp** |
| `PUT /courses/{id}` | ✅ | ✅ | **Khớp** |
| `DELETE /courses/{id}` | ✅ | ✅ | **Khớp** |
| `POST /courses/from-prompt` | ✅ | ✅ | **Khớp** |

#### ❌ Endpoints Thiếu Trong Documentation
| Endpoint | Method | Mô Tả | Quan Trọng |
|----------|--------|--------|------------|
| `/courses/public` | GET | Lấy public courses | 🔥 **Cao** |
| `/courses/from-upload` | POST | Tạo course từ file upload | 🔥 **Cao** |
| `/courses/{id}/generate-outline` | POST | Tạo outline bằng AI | 🔶 **Trung bình** |
| `/courses/{id}/chapters` | POST | Tạo chapter mới | 🔥 **Cao** |
| `/courses/{id}/chapters` | GET | Lấy danh sách chapters | 🔥 **Cao** |
| `/courses/{id}/chapters/{chapter_id}` | GET | Lấy chapter cụ thể | 🔥 **Cao** |
| `/courses/{id}/chapters/{chapter_id}` | PUT | Cập nhật chapter | 🔥 **Cao** |
| `/courses/{id}/chapters/{chapter_id}` | DELETE | Xóa chapter | 🔥 **Cao** |
| `/courses/{id}/chat` | POST | Chat với course context | 🔶 **Trung bình** |
| `/courses/{id}/summarize` | POST | Tóm tắt chapter | 🔶 **Trung bình** |
| `/courses/{id}/flashcards` | POST | Tạo flashcards | 🔶 **Trung bình** |

#### 🔴 Sai Lệch Quan Trọng
- **Chapter Management**: Hoàn toàn thiếu hệ thống quản lý chapters (8 endpoints)
- **AI Features**: Thiếu nhiều tính năng AI (3 endpoints)
- **Public Courses**: Thiếu endpoint quan trọng cho public access

---

### 💬 3. CHAT SYSTEM

#### ✅ Endpoints Có Trong Cả Hai
| Endpoint | Documented | Thực Tế | Trạng Thái |
|----------|------------|---------|------------|
| `POST /chat` | ✅ | ✅ | **Khớp** |
| `GET /chat/sessions` | ✅ | ✅ | **Khớp** |
| `GET /chat/history` | ✅ | ✅ | **Khớp** |

#### ❌ Endpoints Thiếu Trong Documentation
| Endpoint | Method | Mô Tả | Quan Trọng |
|----------|--------|--------|------------|
| `/chat/sessions` | POST | Tạo chat session mới | 🔥 **Cao** |
| `/chat/sessions/{id}` | GET | Lấy session cụ thể | 🔥 **Cao** |
| `/chat/sessions/{id}` | DELETE | Xóa chat session | 🔶 **Trung bình** |
| `/chat/sessions/{id}/messages` | GET | Lấy messages trong session | 🔥 **Cao** |
| `/chat/sessions/{id}/messages` | POST | Gửi message trong session | 🔥 **Cao** |
| `/chat/{answer_id}/feedback` | POST | Feedback cho câu trả lời | 🔶 **Trung bình** |
| `/chat/sessions/{id}/save-as-course` | POST | Lưu chat thành course | 🔶 **Trung bình** |
| `/chat/save` | POST | Lưu chat session | 🔶 **Trung bình** |

#### 🔴 Sai Lệch Quan Trọng
- **Session Management**: Thiếu hệ thống session-based chat hoàn chỉnh
- **Message Management**: Thiếu CRUD operations cho messages

---

### 🧠 4. QUIZ SYSTEM

#### ✅ Endpoints Có Trong Cả Hai
| Endpoint | Documented | Thực Tế | Trạng Thái |
|----------|------------|---------|------------|
| `POST /quiz/generate` | ✅ | ✅ | **Khớp** |
| `POST /quiz/manual` | ✅ | ✅ | ✅ **Có nhưng tên khác** |
| `GET /quiz/{id}` | ✅ | ✅ | **Khớp** |
| `POST /quiz/{id}/submit` | ✅ | ✅ | **Khớp** |

#### ❌ Endpoints Thiếu Trong Documentation
| Endpoint | Method | Mô Tả | Quan Trọng |
|----------|--------|--------|------------|
| `/quiz` | POST | Tạo quiz cơ bản | 🔥 **Cao** |
| `/quiz` | GET | Lấy danh sách quizzes | 🔥 **Cao** |
| `/quiz/from-course/{id}` | POST | Tạo quiz từ course | 🔥 **Cao** |
| `/quiz/from-upload/{id}` | POST | Tạo quiz từ upload | 🔥 **Cao** |
| `/quiz/{id}/questions` | GET | Lấy câu hỏi quiz | 🔥 **Cao** |
| `/quiz/{id}` | PATCH | Cập nhật quiz | 🔶 **Trung bình** |
| `/quiz/{id}` | DELETE | Xóa quiz | 🔶 **Trung bình** |
| `/quiz/{id}/grade` | POST | Chấm điểm thủ công | 🔶 **Trung bình** |
| `/quiz/{id}/results` | GET | Lấy kết quả quiz | 🔶 **Trung bình** |
| `/quiz/history` | GET | Lịch sử làm quiz | 🔶 **Trung bình** |
| `/quiz/history/{id}` | GET | Chi tiết lịch sử | 🔶 **Trung bình** |

#### 🔴 Sai Lệch Quan Trọng
- **Quiz CRUD**: Thiếu operations cơ bản (GET, PATCH, DELETE)
- **Specialized Creation**: Thiếu tạo quiz từ course/upload (2 endpoints quan trọng)
- **History System**: Thiếu hệ thống lịch sử hoàn chỉnh

---

### 📤 5. FILE UPLOAD SYSTEM

#### ✅ Endpoints Có Trong Cả Hai
| Endpoint | Documented | Thực Tế | Trạng Thái |
|----------|------------|---------|------------|
| `POST /uploads` | ✅ | ✅ | **Khớp** |
| `GET /uploads` | ✅ | ✅ | **Khớp** |
| `DELETE /uploads/{id}` | ✅ | ✅ | **Khớp** |
| `GET /uploads/{id}/status` | ✅ | ✅ | **Khớp** |

#### ❌ Endpoints Thiếu Trong Documentation
| Endpoint | Method | Mô Tả | Quan Trọng |
|----------|--------|--------|------------|
| `/uploads/{id}` | GET | Lấy thông tin upload cụ thể | 🔶 **Trung bình** |
| `/uploads/{id}/reprocess` | POST | Xử lý lại file upload | 🔶 **Trung bình** |

---

### 📊 6. DASHBOARD SYSTEM

#### ✅ Endpoints Có Trong Cả Hai
| Endpoint | Documented | Thực Tế | Trạng Thái |
|----------|------------|---------|------------|
| `GET /dashboard/overview` | ✅ | ✅ | **Khớp** |
| `GET /dashboard/progress` | ✅ | ✅ | **Khớp** |
| `POST /dashboard/progress` | ✅ | ✅ | **Khớp** |

#### ❌ Endpoints Thiếu Trong Documentation
| Endpoint | Method | Mô Tả | Quan Trọng |
|----------|--------|--------|------------|
| `/dashboard/stats` | GET | Thống kê chi tiết dashboard | 🔥 **Cao** |
| `/dashboard/progress/{id}` | GET | Tiến độ chi tiết course | 🔥 **Cao** |
| `/dashboard/recommendations` | GET | Gợi ý học tập AI | 🔶 **Trung bình** |
| `/dashboard/course-stats/{id}` | GET | Thống kê course cụ thể | 🔶 **Trung bình** |

---

## 🚨 CÁC SERVICE BỊ THIẾU HOÀN TOÀN

### 🎓 1. STUDENT SERVICE (/api/v1/student)
**Chức năng**: Hệ thống enrollment và dashboard cho học viên

| Endpoint | Method | Mô Tả | Quan Trọng |
|----------|--------|--------|------------|
| `/student/courses/{id}/enroll` | POST | Đăng ký học course | 🔥 **Cực Cao** |
| `/student/courses/{id}/enroll` | DELETE | Hủy đăng ký course | 🔥 **Cực Cao** |
| `/student/enrolled-courses` | GET | Courses đã đăng ký | 🔥 **Cực Cao** |
| `/student/dashboard` | GET | Dashboard sinh viên | 🔥 **Cao** |

**Tác động**: Thiếu hệ thống enrollment cơ bản - học viên không thể đăng ký courses!

### 👨‍🏫 2. INSTRUCTOR SERVICE (/api/v1/instructor)
**Chức năng**: Dashboard và analytics cho giảng viên

| Endpoint | Method | Mô Tả | Quan Trọng |
|----------|--------|--------|------------|
| `/instructor/courses` | GET | Courses của instructor | 🔥 **Cao** |
| `/instructor/courses/{id}/students` | GET | Students trong course | 🔥 **Cao** |
| `/instructor/courses/{id}/analytics` | GET | Analytics course | 🔥 **Cao** |
| `/instructor/dashboard` | GET | Dashboard instructor | 🔥 **Cao** |
| `/instructor/students` | GET | Tất cả students | 🔶 **Trung bình** |

**Tác động**: Instructors không có dashboard và analytics để quản lý courses!

### 🔧 3. ADMIN SERVICE (/api/v1/admin)
**Chức năng**: Quản lý hệ thống và người dùng

| Endpoint | Method | Mô Tả | Quan Trọng |
|----------|--------|--------|------------|
| `/admin/users` | GET | Quản lý users | 🔥 **Cực Cao** |
| `/admin/users/{id}/role` | PATCH | Thay đổi role user | 🔥 **Cực Cao** |
| `/admin/stats` | GET | Thống kê hệ thống | 🔥 **Cao** |
| `/admin/courses` | POST | Tạo sample courses | 🔶 **Trung bình** |
| `/admin/courses` | GET | Xem tất cả courses | 🔶 **Trung bình** |
| `/admin/courses/{id}` | DELETE | Xóa bất kỳ course | 🔶 **Trung bình** |

**Tác động**: Không có dashboard admin để quản lý hệ thống!

### 🔍 4. SEARCH SERVICE (/api/v1/search)
**Chức năng**: Vector search và embeddings management

| Endpoint | Method | Mô Tả | Quan Trọng |
|----------|--------|--------|------------|
| `/search` | POST | Vector similarity search | 🔥 **Cao** |
| `/search/embeddings` | POST | Reindex embeddings | 🔶 **Trung bình** |
| `/search/courses/{id}/reindex` | POST | Reindex course | 🔶 **Trung bình** |

**Tác động**: Thiếu tính năng tìm kiếm thông minh trong courses/uploads!

### 🏆 5. LEADERBOARD SERVICE (/api/v1/leaderboard)
**Chức năng**: Bảng xếp hạng và gamification

| Endpoint | Method | Mô Tả | Quan Trọng |
|----------|--------|--------|------------|
| `/leaderboard` | GET | Bảng xếp hạng users | 🔶 **Trung bình** |

**Tác động**: Thiếu tính năng gamification để động viên học viên!

### 👥 6. USERS SERVICE (/api/v1/users)
**Chức năng**: User profile management (riêng biệt với auth)

| Endpoint | Method | Mô Tả | Quan Trọng |
|----------|--------|--------|------------|
| `/users/me` | GET | Profile user hiện tại | 🔶 **Trung bình** |
| `/users/me` | PATCH | Cập nhật profile | 🔶 **Trung bình** |

**Tác động**: Trùng lặp với auth service, cần sắp xếp lại!

---

## 🎯 NHÓM CHỨC NĂNG THEO MỨC ĐỘ QUAN TRỌNG

### 🔥 **CRITICAL - Thiếu Cực Kỳ Quan Trọng**
1. **Student Enrollment System** - 3 endpoints
   - Học viên không thể đăng ký courses
   - Thiếu dashboard học viên

2. **Chapter Management System** - 8 endpoints  
   - Courses không có chapters chi tiết
   - Thiếu CRUD operations cho chapters

3. **Admin User Management** - 2 endpoints
   - Không thể quản lý users và roles
   - Thiếu admin dashboard

### 🔶 **HIGH - Thiếu Quan Trọng**
1. **Quiz Management Extensions** - 10 endpoints
   - Thiếu nhiều operations cho quiz
   - Thiếu tạo quiz từ course/upload

2. **Chat Session Management** - 8 endpoints
   - Chat chỉ freestyle, thiếu session management
   - Thiếu lưu/quản lý chat history

3. **Instructor Analytics** - 5 endpoints
   - Instructors không có analytics
   - Thiếu dashboard giảng viên

### 🔸 **MEDIUM - Thiếu Trung Bình**
1. **AI Enhancement Features** - 6 endpoints
   - Thiếu generate outline, summarize, flashcards
   - Thiếu vector search

2. **Authentication Extensions** - 4 endpoints
   - Thiếu forgot/reset password
   - Thiếu email verification

3. **System Monitoring** - 3 endpoints
   - Thiếu leaderboard
   - Thiếu system stats

---

## 📋 KẾT LUẬN VÀ KHUYẾN NGHỊ

### 🚨 **Vấn Đề Nghiêm Trọng**
1. **Documentation thiếu 48% endpoints** (42/87 endpoints)
2. **6 services quan trọng bị thiếu hoàn toàn**
3. **Không phản ánh kiến trúc thực tế** của hệ thống

### 🎯 **Ưu Tiên Cập Nhật**
1. **Cập nhật SYSTEM_OVERVIEW.md** với API mapping chính xác
2. **Thêm documentation cho 6 services thiếu**
3. **Cập nhật frontend service mapping** 
4. **Review và cập nhật phân quyền system**

### 📊 **Tác Động Lên Hiệu Quả**
- **Developers mới**: Bị mislead về system capabilities
- **API Integration**: Thiếu thông tin để integrate properly  
- **Testing**: Không test được tất cả endpoints
- **Maintenance**: Khó maintain khi documentation không đúng

**🔥 Khuyến nghị**: Cập nhật ngay lập tức SYSTEM_OVERVIEW.md với thông tin từ ACTUAL_API_ENDPOINTS.md!