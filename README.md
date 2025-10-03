# Nền Tảng Học Tập Thông Minh AI

Một hệ thống học tập toàn diện được hỗ trợ bởi trí tuệ nhân tạo, cho phép tạo khóa học, chat với AI, làm quiz và theo dõi tiến độ học tập.

## Giới Thiệu

Nền Tảng Học Tập AI là một ứng dụng web hiện đại kết hợp sức mạnh của React, FastAPI và Google GenAI để tạo ra trải nghiệm học tập tương tác và thông minh. Hệ thống hỗ trợ nhiều vai trò người dùng và cung cấp các công cụ học tập đa dạng.

## Tính Năng Chính

### Cho Sinh Viên
- **Ghi danh khóa học**: Đăng ký các khóa học công khai từ giảng viên
- **Học tương tác**: Giao diện học tập trực quan với theo dõi tiến độ
- **Chat AI**: Trò chuyện với gia sư AI 24/7 theo hai chế độ (Strict/Hybrid)
- **Quiz thông minh**: Làm bài quiz được tạo tự động từ nội dung khóa học
- **Tải lên tài liệu**: Upload PDF, DOCX, TXT để AI xử lý và tạo nội dung
- **Dashboard cá nhân**: Theo dõi tiến độ, điểm số và thời gian học

### Cho Giảng Viên
- **Tạo khóa học**: Tạo khóa học thủ công hoặc sinh tự động bằng AI
- **Quản lý sinh viên**: Xem danh sách, tiến độ và hoạt động của học viên
- **Phân tích dữ liệu**: Dashboard với thống kê chi tiết về khóa học
- **Tạo quiz**: Sinh câu hỏi tự động từ nội dung bài giảng
- **Chat hỗ trợ**: Tương tác với sinh viên qua AI assistant

### Cho Quản Trị Viên
- **Quản lý người dùng**: Phân quyền, theo dõi hoạt động toàn hệ thống
- **Thống kê tổng quan**: Báo cáo về sử dụng, hiệu suất hệ thống
- **Quản lý nội dung**: Kiểm soát và điều phối tất cả khóa học

## Công Nghệ Sử Dụng

### Backend
- **FastAPI**: Framework API hiện đại với Python
- **MongoDB**: Cơ sở dữ liệu NoSQL với Beanie ODM
- **Google GenAI**: Trí tuệ nhân tạo Gemini Pro
- **JWT**: Xác thực và phân quyền bảo mật
- **Vector Search**: Tìm kiếm semantic thông minh

### Frontend
- **React 18**: Thư viện UI với TypeScript
- **Tailwind CSS**: Framework CSS utility-first
- **Zustand**: Quản lý state đơn giản
- **Framer Motion**: Animation mượt mà
- **React i18next**: Hỗ trợ đa ngôn ngữ (Việt/Anh)

## Cài Đặt Nhanh

### Yêu Cầu Hệ Thống
- Python 3.11+
- Node.js 18+
- MongoDB (local hoặc Atlas)
- Google API Key

### Khởi Động Backend
```bash
cd BEDB
pip install -r requirements.txt
cp env.example .env
# Chỉnh sửa .env với thông tin cấu hình
python scripts/init_database.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Khởi Động Frontend
```bash
cd learning-app-fe
npm install
cp .env.example .env
# Chỉnh sửa .env: VITE_API_URL=http://localhost:8000
npm run dev
```

### Truy Cập Ứng Dụng
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Đăng nhập mặc định**: admin@ailearning.com / admin123456

## Cấu Trúc Dự Án

```
LEARNING-AI/
├── BEDB/                           # Backend API
│   ├── app/
│   │   ├── models/                 # Database models
│   │   ├── routers/                # API endpoints
│   │   ├── services/               # Business logic
│   │   └── schemas/                # Request/response schemas
│   ├── scripts/                    # Database scripts
│   └── README.md                   # Backend documentation
├── learning-app-fe/                # Frontend React App
│   ├── src/
│   │   ├── components/             # React components
│   │   ├── pages/                  # Route pages
│   │   ├── services/               # API integration
│   │   ├── stores/                 # State management
│   │   └── i18n/                   # Language files
│   └── README.md                   # Frontend documentation
├── HUONG_DAN_CAI_DAT.md           # Setup guide
├── KIEN_TRUC_HE_THONG.md          # System architecture
├── HUONG_DAN_DEPLOY.md            # Deployment guide
└── README.md                       # This file
```

## Tài Liệu Chi Tiết

- **[Hướng Dẫn Cài Đặt](HUONG_DAN_CAI_DAT.md)**: Cài đặt chi tiết từng bước
- **[Kiến Trúc Hệ Thống](KIEN_TRUC_HE_THONG.md)**: Thiết kế và kiến trúc tổng thể
- **[Hướng Dẫn Deploy](HUONG_DAN_DEPLOY.md)**: Triển khai lên production
- **[Backend README](BEDB/README.md)**: Documentation API backend
- **[Frontend README](learning-app-fe/README.md)**: Documentation React frontend

## Quy Trình Phát Triển

### Development Environment
```bash
# Terminal 1 - Backend
cd BEDB && uvicorn app.main:app --reload

# Terminal 2 - Frontend  
cd learning-app-fe && npm run dev
```

### Testing
```bash
# Backend testing
cd BEDB && python run_tests.py

# Frontend testing
cd learning-app-fe && npm run lint
```

## Deployment

### Development
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- Database: MongoDB local

### Production
- **Frontend**: Vercel/Netlify static hosting
- **Backend**: Docker container trên cloud (DigitalOcean, AWS, GCP)
- **Database**: MongoDB Atlas
- **CDN**: CloudFlare cho performance

## Bảo Mật

### Tính Năng Bảo Mật
- JWT authentication với refresh tokens
- Role-based access control (Student/Instructor/Admin)
- Input validation và sanitization
- File upload security với type checking
- CORS configuration
- Rate limiting cho API calls
- HTTPS enforced trong production

### Best Practices
- Environment variables cho sensitive data
- Regular security updates
- Database backup tự động
- Error handling không expose sensitive info
- Logging và monitoring

## Performance

### Tối Ưu Backend
- Database indexing cho queries thường dùng
- Async processing cho file uploads
- Caching cho frequent data
- Connection pooling
- Pagination cho large datasets

### Tối Ưu Frontend
- Code splitting theo routes
- Lazy loading components
- Image optimization
- Bundle size optimization
- CDN cho static assets

## Monitoring

### Application Monitoring
- Sentry để track errors
- Performance monitoring
- User analytics
- API response times
- Database query performance

### Infrastructure Monitoring
- Server health checks
- Memory và CPU usage
- Disk space monitoring
- Network performance
- Backup verification

## Đóng Góp

### Development Workflow
1. Fork repository
2. Tạo feature branch từ `main`
3. Implement changes với tests
4. Submit pull request
5. Code review và merge

### Code Standards
- **Backend**: Black formatter, isort, mypy
- **Frontend**: Prettier, ESLint, TypeScript strict
- **Commit**: Conventional commits format
- **Documentation**: Update docs cho new features


## Hỗ Trợ

### Tài Liệu
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Google AI Documentation](https://ai.google.dev/)

### Community
- GitHub Issues cho bug reports
- GitHub Discussions cho feature requests
- Code examples trong documentation
- Regular updates và improvements

## Giấy Phép

MIT License 

## Credits

Phát triển bởi team AI Learning Platform với sự hỗ trợ của:
- Google GenAI cho AI capabilities
- MongoDB Atlas cho database hosting
- Vercel cho frontend hosting
- Open source community

---

**Nền Tảng Học Tập AI** 