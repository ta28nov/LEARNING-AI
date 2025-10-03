# Nền Tảng Học Tập Thông Minh - Frontend

Giao diện người dùng hiện đại cho nền tảng học tập được hỗ trợ bởi AI, xây dựng bằng React, TypeScript với thiết kế responsive và đa ngôn ngữ.

## Tính Năng Chính

### Giao Diện Người Dùng
- **Chế độ Dark/Light**: Chuyển đổi liền mạch giữa chế độ sáng và tối với lưu trữ tùy chọn
- **Đa ngôn ngữ**: Hỗ trợ đầy đủ Tiếng Việt và English với react-i18next
- **Thiết kế Responsive**: Tối ưu hoàn hảo cho Desktop, Tablet và Mobile
- **Hiệu ứng Animation**: Sử dụng Framer Motion cho trải nghiệm tương tác mượt mà

### Quản Lý Khóa Học
- **Danh sách khóa học**: Xem và tìm kiếm khóa học với bộ lọc thông minh theo cấp độ, thẻ tag
- **Tạo khóa học**: Hỗ trợ tạo khóa học thủ công hoặc sinh tự động bằng AI từ prompt
- **Chi tiết khóa học**: Hiển thị nội dung chi tiết, các chương học và theo dõi tiến độ
- **Giao diện học tập**: Navigation trực quan với thanh tiến độ và bookmark

### Hệ Thống Ghi Danh
- **Ghi danh khóa học**: Đăng ký tham gia khóa học công khai với một cú click
- **Quản lý học viên**: Giảng viên theo dõi danh sách sinh viên, hoạt động và tiến độ
- **Dashboard sinh viên**: Xem tất cả khóa học đã đăng ký với thống kê tiến độ
- **Dashboard giảng viên**: Quản lý khóa học, analytics chi tiết và thống kê học viên
- **Phân quyền động**: Chỉ khóa học có visibility PUBLIC mới cho phép ghi danh
- **Hủy ghi danh**: Sinh viên linh hoạt hủy đăng ký bất cứ lúc nào

### Quản Lý File
- **Drag & Drop**: Giao diện kéo thả file trực quan và dễ sử dụng
- **Đa định dạng**: Hỗ trợ PDF, DOCX, TXT với xử lý tự động
- **Theo dõi realtime**: Hiển thị trạng thái xử lý file theo thời gian thực
- **Quản lý nâng cao**: Xóa, tái xử lý file với xác nhận an toàn

### Chat AI Thông Minh
- **Gia sư AI 24/7**: Trò chuyện với AI tutor bất cứ lúc nào
- **Chế độ Strict/Hybrid**: Lựa chọn chế độ chat dựa trên nội dung hoặc kiến thức tổng quát
- **Lịch sử đầy đủ**: Lưu trữ và quản lý tất cả cuộc trò chuyện
- **Chat theo ngữ cảnh**: Tích hợp với nội dung khóa học cụ thể

### Hệ Thống Quiz
- **Tạo quiz AI**: Sinh quiz tự động từ nội dung khóa học hoặc file tải lên
- **Giao diện làm bài**: Interface thân thiện với timer và navigation câu hỏi
- **Kết quả chi tiết**: Hiển thị đáp án đúng, giải thích và phân tích lỗi
- **Lịch sử hoàn chỉnh**: Theo dõi tất cả bài thi đã làm với thống kê tiến bộ

### Dashboard Tiến Độ
- **Thống kê tổng quan**: Hiển thị metrics quan trọng như số khóa học, điểm số, thời gian học
- **Biểu đồ trực quan**: Charts và graphs cho progress theo thời gian
- **Gợi ý thông minh**: AI đưa ra khuyến nghị học tập cá nhân hóa
- **Phân tích chi tiết**: Báo cáo hiệu quả học tập với insights sâu sắc

### Quản Trị Hệ Thống
- **Quản lý người dùng**: Admin có thể thay đổi role, theo dõi hoạt động người dùng
- **Kiểm soát khóa học**: Quản lý toàn bộ nội dung khóa học trong hệ thống
- **Thống kê hệ thống**: Dashboard admin với metrics và báo cáo quan trọng

## Công Nghệ Sử Dụng

### Framework Frontend
- **React 18**: Framework UI hiện đại với Concurrent Features và Hooks
- **TypeScript**: Đảm bảo type safety và trải nghiệm phát triển tốt hơn
- **Vite**: Build tool siêu nhanh với HMR và ES modules

### UI/UX
- **Tailwind CSS**: Framework CSS utility-first cho styling nhanh chóng
- **Headless UI**: Components UI accessible và không có styling
- **Lucide React**: Thư viện icon SVG đẹp và nhất quán
- **Framer Motion**: Thư viện animation mạnh mẽ cho React

### Quản Lý State
- **Zustand**: State management đơn giản, nhẹ và hiệu quả
- **React Hook Form**: Xử lý form với validation mạnh mẽ
- **Axios**: HTTP client với interceptors và error handling

### Quốc Tế Hóa
- **React i18next**: Hỗ trợ đa ngôn ngữ hoàn chỉnh với namespace
- **Language Detection**: Tự động phát hiện và lưu trữ ngôn ngữ người dùng

### Development Tools
- **ESLint**: Kiểm tra và đảm bảo chất lượng code
- **Prettier**: Định dạng code tự động
- **TypeScript**: Kiểm tra kiểu tĩnh và IntelliSense

## Cài Đặt Và Chạy

### Yêu Cầu Hệ Thống
- Node.js 18 trở lên
- npm hoặc yarn
- Backend API đang chạy (xem thư mục BEDB)

### Hướng Dẫn Cài Đặt

1. **Sao chép repository**
   ```bash
   git clone <repository-url>
   cd LEARNING-AI/learning-app-fe
   ```

2. **Cài đặt dependencies**
   ```bash
   npm install
   ```

3. **Cấu hình biến môi trường**
   ```bash
   cp .env.example .env
   ```
   
   Chỉnh sửa file `.env`:
   ```env
   VITE_API_URL=http://localhost:8000
   VITE_APP_NAME=Nền Tảng Học Tập AI
   ```

4. **Chạy development server**
   ```bash
   npm run dev
   ```

   Ứng dụng sẽ chạy tại: http://localhost:3000

### Build Cho Production

```bash
npm run build
```

### Xem trước Production

```bash
npm run preview
```

## Cấu Trúc Dự Án

```
learning-app-fe/
├── public/                 # File tĩnh
├── src/
│   ├── components/         # React components
│   │   ├── ui/            # UI components tái sử dụng
│   │   ├── layout/        # Layout components
│   │   └── enrollment/    # Components hệ thống ghi danh
│   ├── pages/             # Page components
│   │   ├── auth/          # Trang xác thực
│   │   ├── courses/       # Trang khóa học
│   │   ├── enrollment/    # Trang ghi danh (sinh viên & giảng viên)
│   │   ├── chat/          # Trang chat AI
│   │   ├── quiz/          # Trang quiz
│   │   ├── admin/         # Trang quản trị
│   │   └── dashboard/     # Trang dashboard
│   ├── services/          # Dịch vụ API
│   ├── stores/            # Zustand stores quản lý state
│   ├── contexts/          # React contexts
│   ├── hooks/             # Custom hooks
│   ├── types/             # Định nghĩa TypeScript types
│   ├── i18n/              # Quốc tế hóa
│   │   └── locales/       # File ngôn ngữ (vi.json, en.json)
│   ├── lib/               # Hàm tiện ích
│   └── styles/            # Global styles
├── .env.example           # Template biến môi trường
├── tailwind.config.js     # Cấu hình Tailwind CSS
├── tsconfig.json          # Cấu hình TypeScript
└── vite.config.ts         # Cấu hình Vite
```

## Hệ Thống Thiết Kế

### Bảng Màu
- **Primary**: #2563EB (Xanh dương)
- **Secondary**: #FACC15 (Vàng)
- **Accent**: #10B981 (Xanh lá)
- **Grayscale**: Từ Gray-50 đến Gray-900

### Typography
- **Font chính**: Inter (Google Fonts)
- **Kích thước**: Responsive typography scale
- **Trọng lượng**: 400, 500, 600, 700

### Components
- **Buttons**: Nhiều variants (Primary, Secondary, Ghost, Outline)
- **Cards**: Bo góc 16px với shadow mềm mại
- **Inputs**: Border focus với hiệu ứng ring
- **Layout**: Hệ thống grid responsive

## Đa Ngôn Ngữ

Ứng dụng hỗ trợ:
- Tiếng Việt (mặc định)
- English

### Thêm Ngôn Ngữ Mới

1. Tạo file JSON mới trong `src/i18n/locales/`
2. Import và cấu hình trong `src/i18n/index.ts`
3. Cập nhật component `LanguageToggle`

## Hiệu Ứng Animation

### Framer Motion Components
- **AnimatedPage**: Chuyển tiếp trang mượt mà
- **FadeIn**: Hiệu ứng fade in với direction
- **StaggerContainer**: Hiệu ứng stagger cho list
- **FloatingButton**: Nút có hiệu ứng hover 3D
- **ProgressRing**: Vòng tròn tiến độ animated

### Sử Dụng Animations

```tsx
import { FadeIn } from '@/components/ui/FadeIn';

<FadeIn direction="up" delay={0.1}>
  <Card>Nội dung hiển thị với hiệu ứng</Card>
</FadeIn>
```

## Tích Hợp API

### Các Service
- **authService**: Xác thực và quản lý người dùng
- **courseService**: Thao tác CRUD khóa học
- **enrollmentService**: Ghi danh sinh viên/giảng viên
- **uploadService**: Tải lên và quản lý file
- **chatService**: Chức năng chat AI
- **quizService**: Tạo và nộp quiz
- **dashboardService**: Theo dõi tiến độ
- **adminService**: Các thao tác quản trị

### Base URL API
Tất cả API calls sử dụng đường dẫn cơ sở: `/api/v1/`

### Xử Lý Lỗi
- Toast thông báo lỗi tự động
- Xử lý refresh token
- Khôi phục lỗi mạng
- Hiển thị lỗi validation

## Xác Thực

### JWT Tokens
- Access token cho API calls
- Refresh token để gia hạn
- Tự động refresh token
- Lưu trữ trạng thái đăng nhập

### Protected Routes
- Bảo vệ route dựa trên xác thực
- Kiểm soát truy cập theo vai trò
- Xử lý redirect

## Thiết Kế Responsive

### Điểm Ngắt (Breakpoints)
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px  
- **Desktop**: > 1024px
- **Large**: > 1440px

### Tính Năng Mobile
- Sidebar thu gọn được
- Tương tác thân thiện với touch
- Layout tối ưu
- Cử chỉ vuốt

## Testing

### Unit Tests
```bash
npm run test
```

### Linting
```bash
npm run lint
```

## Triển Khai

### Vercel (Khuyến nghị)
1. Kết nối repository với Vercel
2. Thiết lập biến môi trường
3. Triển khai tự động

### Netlify
1. Lệnh build: `npm run build`
2. Thư mục publish: `dist`
3. Thiết lập biến môi trường

## Khắc Phục Sự Cố

### Lỗi Thường Gặp

1. **Lỗi kết nối API**
   - Kiểm tra VITE_API_URL trong .env
   - Đảm bảo backend đang chạy

2. **Lỗi Build**
   - Xóa node_modules và cài đặt lại
   - Kiểm tra lỗi TypeScript

3. **Thiếu Translation**
   - Kiểm tra key trong file ngôn ngữ
   - Khởi động lại dev server

## Đóng Góp

### Quy Trình Phát Triển
1. Fork repository
2. Tạo feature branch
3. Thực hiện thay đổi
4. Thêm tests
5. Gửi pull request

### Code Style
- Sử dụng Prettier cho định dạng
- Tuân thủ ESLint rules
- TypeScript strict mode
- Tên component: PascalCase

## Giấy Phép

MIT License - xem file LICENSE để biết chi tiết.

## Hỗ Trợ

Để được hỗ trợ:
- Tạo issue trong repository
- Kiểm tra tài liệu tại `/docs` của backend
- Xem code examples trong components


