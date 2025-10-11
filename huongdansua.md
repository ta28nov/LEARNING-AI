Lưu ý quan trọng, mọi thứ trong file này chỉ là hướng dẫn các đề mục để có tài liệu chi tiết nhất, mọi cấu trúc có sẵn hay nội dung ko cần sửa trong file C:\Users\Admin\LEARNING-AI\HE_THONG.md không cần phải thay thế nếu ko liên quan. và đảm bảo bạn làm tốt và đủ dựa trên 12,13 đề mục này
⸻
1. TỔNG QUAN HỆ THỐNG (System Overview)

Mục tiêu: Xác định mục đích, đối tượng sử dụng, giá trị và phạm vi hệ thống.
Nội dung chi tiết:
 • Mục tiêu hệ thống (AI hỗ trợ học tập, gợi ý khóa học, hỏi đáp thông minh, theo dõi tiến độ).
 • Đối tượng: Học sinh, giảng viên, admin.
 • Phạm vi: Web app FE + BE + AI Service.
 • Output: 1 trang mô tả tổng quan + sơ đồ khối (high-level architecture).

⸻

2. USER FLOW TỔNG THỂ

Mục tiêu: Hiểu cách người dùng tương tác xuyên suốt hệ thống.
Nội dung chi tiết:
 • Sơ đồ flow tổng (ví dụ: đăng ký → chọn role → học → hỏi AI → làm quiz → xem tiến độ).
 • Các nhánh chính: Student, Instructor, Admin.
 • Dạng sơ đồ: Mermaid hoặc draw.io.

⸻

3. SYSTEM FLOW & KIẾN TRÚC (System Architecture)

Mục tiêu: Hiểu cách hệ thống hoạt động toàn diện.
Nội dung chi tiết:
 • Sơ đồ FE-BE-DB-AI.
 • Data flow từ frontend → API → database → AI module.
 • Kiến trúc đề xuất:
 • FE: React + Zustand
 • BE: FastAPI + MongoDB
 • AI: Vector Search + GenAI API
 • Cách tích hợp authentication, file upload, AI query, quiz generator.

⸻

4. YÊU CẦU DEVELOPMENT (Development Requirements)

Mục tiêu: Chuẩn hóa môi trường và quy tắc code.
Nội dung chi tiết:
 • Yêu cầu version (Node, Python, MongoDB…).
 • Cấu trúc folder FE/BE.
 • Quy tắc code style, lint, test, commit.
 • Mô hình deploy: Local → Production (Docker, CI/CD).

⸻

5. LUỒNG NGƯỜI DÙNG CHI TIẾT (Detailed User Journeys)

Mục tiêu: Làm rõ hành vi từng loại người dùng.
Nội dung chi tiết:
 • Student: Đăng nhập → chọn khóa → học → quiz → hỏi AI → xem kết quả.
 • Instructor: Tạo khóa → upload tài liệu → gắn quiz → xem học viên.
 • Admin: Quản lý user, course, report.
 • Output: Mỗi role 1 sơ đồ + mô tả use case.

⸻

6. KIẾN TRÚC DATABASE (Database Schema)

Mục tiêu: Làm rõ dữ liệu và mối quan hệ.
Nội dung chi tiết:
 • ERD (Entity Relationship Diagram).
 • Mô tả bảng/collection: User, Course, Chapter, Quiz, Progress, AIChat, Enrollment.
 • Mô hình dữ liệu ví dụ (JSON/Mongo).

⸻

7. API ENDPOINTS

Mục tiêu: Chuẩn hóa kết nối FE ↔ BE.
Nội dung chi tiết:
 • RESTful route list theo module:
 • /auth (login, register, refresh, logout, me)
 • /courses, /chapters, /quiz, /ai, /progress, /uploads
 • Method + Params + Response mẫu + Error code.
 • Tích hợp token JWT, role-based access.

⸻

8. CÔNG NGHỆ SỬ DỤNG

Mục tiêu: Liệt kê toàn bộ stack và phiên bản.
Nội dung chi tiết:
 • Frontend: Vite + React 18 + Zustand + Tailwind.
 • Backend: FastAPI + MongoDB + Beanie.
 • AI: Google GenAI API + Atlas Vector Search.
  Dev tools: pytest, black, isort, Docker.
 • Bảng version kèm lý do chọn.

9. GIAO DIỆN NGƯỜI DÙNG (UI/UX)

Mục tiêu: Chuẩn hóa layout, đảm bảo FE dev có thể triển khai.
Nội dung chi tiết:
 • Wireframe từng trang (Home, Dashboard, Course Detail, Chat AI, Quiz).
 • Component map (Nav, Sidebar, Card, Modal…).
 • Design System: màu, font, spacing, button style.

⸻

10. BẢNG CHỨC NĂNG THEO VAI TRÒ (Role-based Feature Matrix)

Mục tiêu: Biết rõ ai được phép làm gì.
Nội dung chi tiết:
11. SPEC CHI TIẾT MODULE (Feature Specification)

Mục tiêu: Chuẩn hóa logic của từng chức năng.
Nội dung cần:
 • Mô tả input/output từng module (quiz, AI chat, progress tracking, enrollment…).
 • Quy tắc xử lý (VD: quiz auto-grade, AI trả lời dựa vào course context).
 • Mức ưu tiên, trạng thái phát triển.
 • Output: file feature_spec.md theo từng module.

⸻

12. SECURITY & AUTHORIZATION DESIGN

Mục tiêu: Bảo vệ dữ liệu, quản lý truy cập đúng vai trò.
Nội dung cần:
 • Cấu trúc JWT (access, refresh).
 • Role-based access matrix.
 • Quy trình xác thực, phân quyền API.
 • Chính sách bảo mật dữ liệu người dùng (token, upload, rate limit).

⸻

13. AI PIPELINE DOCUMENT

Mục tiêu: Chuẩn hóa cách hệ thống AI hoạt động.
Nội dung cần:
 • Luồng dữ liệu: Course → Chunk → Embedding → Vector DB → Query → Response.
 • Cách cập nhật/chunk dữ liệu khi khóa học thay đổi.
 • API kết nối GenAI / LLM.
 • Mô hình lưu context học viên để hỏi–đáp trong phạm vi khóa.