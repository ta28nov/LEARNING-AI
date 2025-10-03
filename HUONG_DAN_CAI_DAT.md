# Hướng Dẫn Cài Đặt - Nền Tảng Học Tập AI

Tài liệu này hướng dẫn chi tiết cách cài đặt và thiết lập toàn bộ hệ thống Nền Tảng Học Tập AI bao gồm Backend API và Frontend.

## Tổng Quan Hệ Thống

### Kiến Trúc
- **Backend**: FastAPI + MongoDB + Google GenAI
- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Database**: MongoDB với Vector Search
- **AI Engine**: Google Gemini Pro

### Yêu Cầu Hệ Thống
- **Python**: 3.11 trở lên
- **Node.js**: 18 trở lên
- **MongoDB**: Phiên bản mới nhất (local hoặc Atlas)
- **Google API Key**: Cho GenAI services

## Cài Đặt Backend

### Bước 1: Chuẩn Bị Môi Trường

1. **Cài đặt Python và MongoDB**
   ```bash
   # Kiểm tra Python
   python --version  # >= 3.11

   # Khởi động MongoDB (Windows)
   net start MongoDB
   ```

2. **Thiết lập Backend**
   ```bash
   cd BEDB
   
   # Tạo môi trường ảo
   python -m venv venv
   
   # Kích hoạt môi trường ảo
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   
   # Cài đặt dependencies
   pip install -r requirements.txt
   ```

### Bước 2: Cấu Hình

1. **Tạo file cấu hình**
   ```bash
   cp env.example .env
   ```

2. **Chỉnh sửa file .env**
   ```env
   # Cơ sở dữ liệu
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=ai_learning_app

   # JWT Authentication
   SECRET_KEY=your-very-secure-secret-key-here-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Google GenAI
   GOOGLE_API_KEY=your-google-api-key-here

   # Ứng dụng
   DEBUG=True
   HOST=0.0.0.0
   PORT=8000

   # File Upload
   MAX_FILE_SIZE=10485760  # 10MB
   UPLOAD_DIR=uploads

   # CORS
   ALLOWED_ORIGINS=["http://localhost:3000"]
   ```

### Bước 3: Khởi Tạo Database

1. **Chạy script khởi tạo**
   ```bash
   python scripts/init_database.py
   ```

   Script này sẽ:
   - Tạo tất cả collections cần thiết
   - Thiết lập indexes
   - Tạo tài khoản admin mặc định
   - Thêm dữ liệu mẫu

2. **Tài khoản mặc định**
   ```
   Email: admin@ailearning.com
   Password: admin123456
   Role: admin
   ```

### Bước 4: Chạy Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Kiểm tra:**
- API docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

## Cài Đặt Frontend

### Bước 1: Thiết Lập Frontend

```bash
cd learning-app-fe

# Cài đặt dependencies
npm install

# Tạo file cấu hình
cp .env.example .env
```

### Bước 2: Cấu Hình Frontend

Chỉnh sửa file `.env`:
```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Nền Tảng Học Tập AI
```

### Bước 3: Chạy Frontend

```bash
npm run dev
```

Ứng dụng sẽ chạy tại: http://localhost:3000

## Kiểm Tra Toàn Bộ Hệ Thống

### Backend Health Check

1. **Kiểm tra API endpoints**
   ```bash
   # Test đăng nhập với tài khoản admin
   curl -X POST "http://localhost:8000/api/v1/auth/login" \
   -H "Content-Type: application/json" \
   -d '{"email": "admin@ailearning.com", "password": "admin123456"}'
   ```

2. **Chạy test suite**
   ```bash
   cd BEDB
   python run_tests.py
   ```

### Frontend Health Check

1. **Truy cập http://localhost:3000**
2. **Kiểm tra các tính năng:**
   - Đăng nhập với tài khoản admin
   - Chuyển đổi dark/light mode
   - Thay đổi ngôn ngữ
   - Tạo khóa học mới
   - Chat với AI

## Xử Lý Sự Cố

### Backend Issues

1. **MongoDB Connection Error**
   ```bash
   # Kiểm tra MongoDB đang chạy
   mongosh
   # Nếu không kết nối được, khởi động MongoDB
   net start MongoDB  # Windows
   sudo systemctl start mongod  # Linux
   ```

2. **Google API Key Error**
   - Kiểm tra API key trong .env
   - Đảm bảo API key có quyền truy cập Gemini Pro
   - Kiểm tra quota API

3. **Import Error**
   ```bash
   # Cài đặt lại dependencies
   pip install -r requirements.txt --force-reinstall
   ```

### Frontend Issues

1. **API Connection Error**
   - Kiểm tra backend đang chạy tại port 8000
   - Kiểm tra VITE_API_URL trong .env
   - Kiểm tra CORS settings trong backend

2. **Build Errors**
   ```bash
   # Xóa node_modules và cài đặt lại
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **TypeScript Errors**
   ```bash
   # Kiểm tra TypeScript
   npm run type-check
   ```

## Development Workflow

### 1. Chạy Cả Hai Services

**Terminal 1 - Backend:**
```bash
cd BEDB
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd learning-app-fe
npm run dev
```

### 2. Hot Reload

- Backend: Tự động reload khi thay đổi Python files
- Frontend: Tự động reload khi thay đổi React files

### 3. Debugging

**Backend:**
- Sử dụng FastAPI docs tại `/docs`
- Check logs trong terminal
- Sử dụng debugger trong IDE

**Frontend:**
- Sử dụng React DevTools
- Check browser console
- Network tab để debug API calls

## Production Setup

### Backend Production

1. **Environment Variables**
   ```env
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
   ALLOWED_ORIGINS=["https://yourdomain.com"]
   ```

2. **Deploy với Docker**
   ```bash
   docker build -t ai-learning-backend .
   docker run -p 8000:8000 ai-learning-backend
   ```

### Frontend Production

1. **Build**
   ```bash
   npm run build
   ```

2. **Deploy to Vercel**
   ```bash
   npx vercel --prod
   ```

## Bảo Mật

### Backend Security

1. **Environment Variables**
   - Không commit file .env
   - Sử dụng secret key mạnh
   - Cấu hình CORS chính xác

2. **Database Security**
   - Sử dụng MongoDB Atlas với authentication
   - Thiết lập network access restrictions
   - Regular backups

### Frontend Security

1. **Environment Variables**
   - Chỉ sử dụng VITE_ prefix cho public vars
   - Không expose sensitive keys

2. **Authentication**
   - JWT tokens được lưu securely
   - Automatic token refresh
   - Proper logout handling

## Monitoring và Logs

### Backend Monitoring

1. **Logs**
   - FastAPI access logs
   - Application logs
   - Error tracking

2. **Health Checks**
   - Database connectivity
   - API response times
   - Memory usage

### Frontend Monitoring

1. **Error Tracking**
   - JavaScript errors
   - Network failures
   - User interactions

2. **Performance**
   - Page load times
   - Bundle size
   - Core Web Vitals

## Backup và Recovery

### Database Backup

```bash
# Backup MongoDB
mongodump --uri="mongodb://localhost:27017/ai_learning_app" --out=backup/

# Restore MongoDB
mongorestore backup/ai_learning_app/
```

### Code Backup

- Git repository backup
- Environment files backup
- SSL certificates backup

## Tài Liệu Tham Khảo

### Backend
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Google AI Documentation](https://ai.google.dev/)

### Frontend  
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Vite Documentation](https://vitejs.dev/)

## Hỗ Trợ

Nếu gặp vấn đề trong quá trình cài đặt:

1. Kiểm tra logs chi tiết
2. Đảm bảo tất cả requirements được cài đặt
3. Kiểm tra network connectivity
4. Tham khảo troubleshooting section ở trên