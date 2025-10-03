# Nền Tảng Học Tập Thông Minh - Backend API

Một hệ thống backend hoàn chỉnh cho nền tảng học tập được hỗ trợ bởi AI, xây dựng bằng FastAPI, MongoDB và Google GenAI. Ứng dụng cung cấp quản lý khóa học thông minh, gia sư AI, tạo quiz tự động và theo dõi tiến độ học tập.

## Tính Năng Chính

### Chức Năng Cốt Lõi
- **Xác thực người dùng**: Hệ thống authentication dựa trên JWT với đăng ký và đăng nhập
- **Quản lý khóa học**: Tạo, quản lý và tổ chức khóa học với các chương học chi tiết
- **Hệ thống ghi danh**: Sinh viên đăng ký khóa học với dashboard giảng viên và phân tích dữ liệu
- **Tạo nội dung bằng AI**: Sinh khóa học từ prompt sử dụng Google GenAI
- **Tải lên và xử lý file**: Tải lên PDF, DOCX, TXT với tự động trích xuất văn bản
- **Chat thông minh**: Gia sư AI với chế độ strict và hybrid cho học tập theo ngữ cảnh
- **Hệ thống Quiz**: Tạo và làm quiz với câu hỏi được sinh bởi AI
- **Theo dõi tiến độ**: Dashboard toàn diện với phân tích học tập
- **Tìm kiếm vector**: Tìm kiếm semantic qua nội dung khóa học và file tải lên

### Khả Năng AI
- **Sinh outline khóa học**: Tạo khóa học có cấu trúc từ chủ đề prompt
- **Trích xuất và xử lý văn bản**: Trích xuất và làm sạch text từ tài liệu tải lên
- **Sinh câu hỏi Quiz**: Tạo câu hỏi trắc nghiệm từ nội dung
- **Tạo thẻ ghi nhớ**: Tạo flashcard học tập từ tài liệu khóa học
- **Tóm tắt nội dung**: Sinh tóm tắt các chương của khóa học
- **Hỏi đáp theo ngữ cảnh**: Trả lời câu hỏi dựa trên nội dung khóa học hoặc kiến thức tổng quát

## Công Nghệ Sử Dụng

### Backend
- **FastAPI**: Framework web hiện đại, nhanh cho việc xây dựng API
- **MongoDB**: Cơ sở dữ liệu NoSQL với Beanie ODM
- **Google GenAI**: Tích hợp mô hình AI để tạo nội dung
- **JWT**: Xác thực và phân quyền bảo mật
- **Pydantic**: Validation và serialization dữ liệu

### Cơ Sở Dữ Liệu
- **MongoDB Atlas**: Cơ sở dữ liệu cloud với khả năng tìm kiếm vector
- **Beanie ODM**: Object-document mapper bất đồng bộ cho MongoDB
- **Vector Search**: Tìm kiếm semantic qua nội dung khóa học

### Xử Lý File
- **PyPDF2**: Trích xuất text từ PDF
- **python-docx**: Xử lý tài liệu DOCX
- **python-magic**: Phát hiện loại file
- **aiofiles**: Thao tác file bất đồng bộ

## Cấu Trúc Dự Án

```
app/
├── __init__.py
├── main.py                 # Điểm khởi tạo ứng dụng FastAPI
├── config.py              # Cấu hình ứng dụng
├── database.py            # Kết nối và khởi tạo cơ sở dữ liệu
├── auth.py                # Tiện ích xác thực
├── models/                # Mô hình cơ sở dữ liệu
│   ├── __init__.py
│   ├── user.py           # Mô hình người dùng
│   ├── course.py         # Mô hình khóa học và chương học
│   ├── enrollment.py     # Mô hình ghi danh
│   ├── upload.py         # Mô hình tải lên file
│   ├── quiz.py           # Mô hình Quiz, câu hỏi và lịch sử làm bài
│   ├── chat.py           # Mô hình phiên chat và tin nhắn
│   └── dashboard.py      # Mô hình tiến độ dashboard
├── schemas/               # Pydantic schemas
│   ├── __init__.py
│   ├── auth.py           # Schema xác thực
│   ├── course.py         # Schema khóa học
│   ├── enrollment.py     # Schema ghi danh
│   ├── upload.py         # Schema tải lên
│   ├── quiz.py           # Schema quiz
│   ├── chat.py           # Schema chat
│   └── dashboard.py      # Schema dashboard
├── services/              # Dịch vụ logic nghiệp vụ
│   ├── __init__.py
│   ├── genai_service.py  # Tích hợp Google GenAI
│   ├── file_service.py   # Dịch vụ xử lý file
│   └── vector_service.py # Dịch vụ tìm kiếm vector
└── routers/               # API endpoints
    ├── __init__.py
    ├── auth.py           # Endpoint xác thực
    ├── courses.py        # Endpoint quản lý khóa học
    ├── student.py        # Endpoint ghi danh sinh viên
    ├── instructor.py     # Endpoint quản lý giảng viên
    ├── uploads.py        # Endpoint tải lên file
    ├── quiz.py           # Endpoint quiz
    ├── chat.py           # Endpoint chat
    └── dashboard.py      # Endpoint dashboard
```

## Cài Đặt

### Yêu Cầu Hệ Thống
- Python 3.11 trở lên
- MongoDB (local hoặc Atlas)
- Google API key cho GenAI

### Hướng Dẫn Cài Đặt

1. **Sao chép repository**
   ```bash
   git clone <url-repository>
   cd LEARNING-AI/BEDB
   ```

2. **Tạo môi trường ảo**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Trên Windows: venv\Scripts\activate
   ```

3. **Cài đặt dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Cấu hình môi trường**
   ```bash
   cp env.example .env
   ```
   
   Chỉnh sửa file `.env` với cấu hình của bạn:
   ```env
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=ai_learning_app
   SECRET_KEY=your-secret-key-here
   GOOGLE_API_KEY=your-google-api-key-here
   DEBUG=True
   ```

5. **Khởi tạo cơ sở dữ liệu**
   ```bash
   python scripts/init_database.py
   ```

6. **Chạy ứng dụng**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Tài Liệu API

Sau khi ứng dụng chạy, bạn có thể truy cập:

- **Tài liệu API tương tác**: http://localhost:8000/docs
- **Tài liệu ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Các API Endpoint

### Xác Thực (`/api/v1/auth`)
- `POST /auth/register` - Đăng ký người dùng mới
- `POST /auth/login` - Đăng nhập người dùng
- `GET /auth/me` - Lấy thông tin người dùng hiện tại
- `PATCH /users/me` - Cập nhật hồ sơ người dùng
- `PATCH /users/me/password` - Đổi mật khẩu

### Khóa Học (`/api/v1/courses`)
- `POST /courses/` - Tạo khóa học mới
- `POST /courses/from-prompt` - Tạo khóa học từ AI prompt
- `GET /courses/` - Lấy danh sách khóa học của người dùng
- `GET /courses/{course_id}` - Lấy thông tin khóa học cụ thể
- `PATCH /courses/{course_id}` - Cập nhật khóa học
- `DELETE /courses/{course_id}` - Xóa khóa học
- `POST /courses/{course_id}/chat` - Chat với khóa học
- `POST /courses/{course_id}/summarize` - Tóm tắt chương học

### Ghi Danh (`/api/v1/student` và `/api/v1/instructor`)
- `GET /student/courses` - Danh sách khóa học công khai
- `POST /student/courses/{course_id}/enroll` - Ghi danh khóa học
- `DELETE /student/courses/{course_id}/unenroll` - Hủy ghi danh
- `GET /student/my-courses` - Khóa học đã ghi danh
- `GET /instructor/courses` - Khóa học của giảng viên
- `GET /instructor/courses/{course_id}/students` - Danh sách sinh viên

### Tải Lên File (`/api/v1/uploads`)
- `POST /uploads/` - Tải lên file
- `GET /uploads/` - Lấy danh sách file đã tải
- `GET /uploads/{upload_id}` - Lấy thông tin file cụ thể
- `DELETE /uploads/{upload_id}` - Xóa file
- `GET /uploads/{upload_id}/status` - Kiểm tra trạng thái xử lý

### Quiz (`/api/v1/quiz`)
- `POST /quiz/from-course/{course_id}` - Tạo quiz từ khóa học
- `POST /quiz/from-upload/{upload_id}` - Tạo quiz từ file tải lên
- `GET /quiz/` - Lấy danh sách quiz
- `GET /quiz/{quiz_id}` - Lấy thông tin quiz cụ thể
- `POST /quiz/{quiz_id}/submit` - Nộp bài quiz
- `GET /quiz/history` - Lịch sử làm quiz

### Chat AI (`/api/v1/chat`)
- `POST /chat/freestyle` - Chat tự do với AI
- `POST /chat/save` - Lưu phiên chat
- `GET /chat/history` - Lịch sử chat

### Dashboard (`/api/v1/dashboard`)
- `GET /dashboard/stats` - Thống kê tổng quan
- `GET /dashboard/progress` - Get course progress
- `POST /dashboard/progress` - Update progress
- `GET /dashboard/progress/{course_id}` - Get course progress detail
- `GET /dashboard/recommendations` - Gợi ý học tập

## Cấu Trúc Cơ Sở Dữ Liệu

### Người Dùng (User)
- `id`: ObjectId (Khóa chính)
- `email`: EmailStr (Duy nhất)
- `password_hash`: str (Mật khẩu đã mã hóa)
- `name`: str (Tên người dùng)
- `avatar`: Optional[str] (Ảnh đại diện)
- `role`: UserRole (student/instructor/admin - Vai trò)
- `is_active`: bool (Trạng thái hoạt động)
- `created_at`: datetime (Thời gian tạo)
- `updated_at`: datetime (Thời gian cập nhật)

### Khóa Học (Course)
- `id`: ObjectId (Khóa chính)
- `owner_id`: ObjectId (Khóa ngoại đến User)
- `title`: str (Tiêu đề khóa học)
- `description`: str (Mô tả)
- `outline`: Optional[str] (Đề cương)
- `source`: Optional[str] (Nguồn tạo: manual/ai_generated/from_upload)
- `level`: CourseLevel (beginner/intermediate/advanced - Cấp độ)
- `tags`: List[str] (Thẻ tag)
- `visibility`: str (DRAFT/PUBLIC/PRIVATE - Hiển thị)
- `created_at`: datetime (Thời gian tạo)
- `updated_at`: datetime (Thời gian cập nhật)

### Chương Học (Chapter)
- `id`: ObjectId (Khóa chính)
- `course_id`: ObjectId (Khóa ngoại đến Course)
- `title`: str (Tiêu đề chương)
- `content`: str (Nội dung chương)
- `order`: int (Thứ tự chương)
- `created_at`: datetime (Thời gian tạo)
- `updated_at`: datetime (Thời gian cập nhật)

### Ghi Danh (Enrollment)
- `id`: ObjectId (Khóa chính)
- `student_id`: ObjectId (Khóa ngoại đến User - sinh viên)
- `course_id`: ObjectId (Khóa ngoại đến Course)
- `enrolled_at`: datetime (Thời gian ghi danh)
- `progress`: float (Tiến độ học 0.0-100.0)
- `last_accessed`: Optional[datetime] (Lần truy cập cuối)

### Tải Lên File (Upload)
- `id`: ObjectId (Khóa chính)
- `user_id`: ObjectId (Khóa ngoại đến User)
- `filename`: str (Tên file)
- `file_type`: FileType (pdf/docx/txt/video/image - Loại file)
- `file_path`: str (Đường dẫn file)
- `file_size`: int (Kích thước file)
- `status`: UploadStatus (pending/processing/completed/failed - Trạng thái)
- `extracted_text`: Optional[str] (Văn bản đã trích xuất)
- `metadata`: Optional[dict] (Metadata bổ sung)
- `created_at`: datetime (Thời gian tạo)

### Quiz
- `id`: ObjectId (Khóa chính)
- `course_id`: ObjectId (Khóa ngoại đến Course)
- `upload_id`: Optional[ObjectId] (Khóa ngoại đến Upload)
- `title`: str (Tiêu đề quiz)
- `description`: Optional[str] (Mô tả)
- `created_at`: datetime (Thời gian tạo)

### Câu Hỏi Quiz (QuizQuestion)
- `id`: ObjectId (Khóa chính)
- `quiz_id`: ObjectId (Khóa ngoại đến Quiz)
- `question`: str (Câu hỏi)
- `options`: List[str] (Các lựa chọn)
- `correct_answer`: int (Đáp án đúng)
- `explanation`: Optional[str] (Giải thích)
- `order`: int (Thứ tự câu hỏi)

### Lịch Sử Quiz (QuizHistory)
- `id`: ObjectId (Khóa chính)
- `quiz_id`: ObjectId (Khóa ngoại đến Quiz)
- `user_id`: ObjectId (Khóa ngoại đến User)
- `score`: float (Điểm số)
- `total_questions`: int (Tổng số câu hỏi)
- `correct_answers`: int (Số câu đúng)
- `answers`: List[dict] (Danh sách câu trả lời)
- `taken_at`: datetime (Thời gian làm bài)

### Phiên Chat (ChatSession)
- `id`: ObjectId (Khóa chính)
- `user_id`: ObjectId (Khóa ngoại đến User)
- `course_id`: Optional[ObjectId] (Khóa ngoại đến Course)
- `upload_id`: Optional[ObjectId] (Khóa ngoại đến Upload)
- `title`: str (Tiêu đề phiên chat)
- `mode`: ChatMode (strict/hybrid - Chế độ chat)
- `status`: ChatStatus (active/archived/deleted - Trạng thái)
- `created_at`: datetime (Thời gian tạo)
- `updated_at`: datetime (Thời gian cập nhật)

### Tin Nhắn Chat (ChatMessage)
- `id`: ObjectId (Khóa chính)
- `session_id`: ObjectId (Khóa ngoại đến ChatSession)
- `sender`: str (user/ai - Người gửi)
- `message`: str (Tin nhắn)
- `answer`: Optional[str] (Câu trả lời)
- `metadata`: Optional[dict] (Metadata bổ sung)
- `created_at`: datetime (Thời gian tạo)

### Tiến Độ Dashboard (DashboardProgress)
- `id`: ObjectId (Khóa chính)
- `user_id`: ObjectId (Khóa ngoại đến User)
- `course_id`: ObjectId (Khóa ngoại đến Course)
- `chapter_id`: Optional[ObjectId] (Khóa ngoại đến Chapter)
- `status`: ProgressStatus (not_started/in_progress/completed - Trạng thái)
- `progress`: float (Tiến độ 0.0-100.0)
- `time_spent`: int (Thời gian học - phút)
- `last_accessed`: datetime (Lần truy cập cuối)
- `created_at`: datetime (Thời gian tạo)
- `updated_at`: datetime (Thời gian cập nhật)

## Tính Năng AI

### Tích Hợp Google GenAI
Ứng dụng sử dụng mô hình Gemini Pro của Google cho các tính năng AI:

1. **Sinh đề cương khóa học**: Tạo đề cương có cấu trúc từ chủ đề prompt
2. **Xử lý văn bản**: Trích xuất và làm sạch văn bản từ tài liệu
3. **Tạo Quiz**: Sinh câu hỏi trắc nghiệm từ nội dung
4. **Tạo Flashcard**: Sinh thẻ ghi nhớ học tập
5. **Tóm tắt nội dung**: Tạo tóm tắt tài liệu khóa học
6. **Hỏi đáp theo ngữ cảnh**: Trả lời dựa trên nội dung khóa học

### Chế Độ Chat
- **Chế độ Strict**: Chỉ trả lời dựa trên nội dung đã tải lên/khóa học
- **Chế độ Hybrid**: Kết hợp nội dung khóa học với kiến thức AI tổng quát

### Tìm Kiếm Vector
- Tìm kiếm semantic qua nội dung khóa học và file tải lên
- Phản hồi theo ngữ cảnh dựa trên nội dung liên quan
- Tích hợp MongoDB Atlas Vector Search

## Xử Lý File

### Định Dạng Hỗ Trợ
- **PDF**: Trích xuất văn bản bằng PyPDF2
- **DOCX**: Xử lý tài liệu bằng python-docx
- **TXT**: Đọc trực tiếp văn bản
- **Video/Image**: Trích xuất metadata (xử lý nội dung sẽ được bổ sung)

### Quy Trình Xử Lý
1. Tải lên và xác thực file
2. Trích xuất văn bản theo loại file
3. Xử lý và làm sạch văn bản bằng AI
4. Tạo chỉ mục vector cho tìm kiếm semantic
5. Tích hợp nội dung với hệ thống khóa học

## Bảo Mật

### Xác Thực
- Xác thực dựa trên JWT
- Mã hóa mật khẩu bằng bcrypt
- Hết hạn và làm mới token
- Kiểm soát truy cập theo vai trò người dùng

### Bảo Mật File
- Xác thực loại file
- Giới hạn kích thước và hạn chế
- Lưu trữ file an toàn
- Cách ly người dùng

### Bảo Mật API
- Cấu hình CORS
- Xác thực đầu vào bằng Pydantic
- Xử lý lỗi và ghi log
- Giới hạn tốc độ (khuyến nghị cho production)

## Triển Khai

### Triển Khai Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Biến Môi Trường
- `MONGODB_URL`: Chuỗi kết nối MongoDB
- `DATABASE_NAME`: Tên cơ sở dữ liệu
- `SECRET_KEY`: Khóa bí mật JWT
- `GOOGLE_API_KEY`: Khóa API Google GenAI
- `DEBUG`: Cờ chế độ debug
- `ALLOWED_ORIGINS`: Origins được phép CORS

### Lưu Ý Production
- Sử dụng biến môi trường cho cấu hình
- Thiết lập logging phù hợp
- Triển khai giới hạn tốc độ
- Sử dụng HTTPS trong production
- Thiết lập monitoring và health checks
- Cấu hình backup cơ sở dữ liệu
- Sử dụng reverse proxy (nginx)

## Phát Triển

### Chất Lượng Code
- **Black**: Định dạng code
- **isort**: Sắp xếp import
- **mypy**: Kiểm tra kiểu
- **pytest**: Framework testing

### Chạy Tests
```bash
pytest
python run_tests.py
```

### Định Dạng Code
```bash
black app/
isort app/
```

### Kiểm Tra Kiểu
```bash
mypy app/
```

## Đóng Góp

1. Fork repository
2. Tạo feature branch
3. Thực hiện thay đổi
4. Thêm tests cho tính năng mới
5. Đảm bảo tất cả tests pass
6. Gửi pull request

## Giấy Phép

Dự án này được cấp phép theo MIT License - xem file LICENSE để biết chi tiết.

## Hỗ Trợ

Để được hỗ trợ và đặt câu hỏi:
- Tạo issue trong repository
- Kiểm tra tài liệu API tại `/docs`
- Xem code examples trong routers
