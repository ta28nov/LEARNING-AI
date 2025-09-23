# 🎓 AI Learning Platform - Frontend

Nền tảng học tập thông minh được hỗ trợ bởi AI với giao diện người dùng hiện đại, responsive và đa ngôn ngữ.

## 🌟 Tính năng chính

### 🎨 Giao diện người dùng
- **Dark/Light Mode**: Chuyển đổi liền mạch giữa chế độ sáng và tối
- **Đa ngôn ngữ**: Hỗ trợ Tiếng Việt và English
- **Responsive Design**: Tối ưu cho mọi thiết bị (Desktop, Tablet, Mobile)
- **Animations mượt mà**: Sử dụng Framer Motion cho trải nghiệm tương tác tuyệt vời

### 📚 Quản lý khóa học
- **Danh sách khóa học**: Xem và tìm kiếm khóa học với bộ lọc thông minh
- **Tạo khóa học**: Tạo khóa học thủ công hoặc bằng AI
- **Chi tiết khóa học**: Xem nội dung chi tiết, chương học và tiến độ
- **Học tương tác**: Giao diện học tập trực quan với navigation dễ dàng

### 📁 Quản lý tệp tin
- **Drag & Drop**: Kéo thả tệp tin dễ dàng
- **Multi-format**: Hỗ trợ PDF, DOCX, TXT
- **Theo dõi trạng thái**: Xem trạng thái xử lý real-time
- **Quản lý tệp**: Xóa, tái xử lý tệp tin

### 💬 Chat với AI
- **Chat thông minh**: Trò chuyện với AI tutor 24/7
- **Chế độ Strict/Hybrid**: Tùy chọn chế độ chat phù hợp
- **Lịch sử chat**: Lưu trữ và quản lý cuộc trò chuyện
- **Chat theo ngữ cảnh**: Chat dựa trên nội dung khóa học

### 🧠 Hệ thống Quiz
- **Tạo quiz AI**: Sinh quiz tự động từ nội dung
- **Làm bài trực tuyến**: Giao diện làm bài thân thiện
- **Kết quả chi tiết**: Xem đáp án và giải thích
- **Lịch sử bài thi**: Theo dõi tiến độ qua thời gian

### 📊 Theo dõi tiến độ
- **Dashboard tổng quan**: Xem thống kê học tập tổng thể
- **Biểu đồ tiến độ**: Visualize tiến độ bằng charts
- **Gợi ý học tập**: AI đưa ra gợi ý cá nhân hóa
- **Thống kê chi tiết**: Phân tích hiệu quả học tập

### 👨‍💼 Quản trị hệ thống
- **Quản lý người dùng**: Thay đổi role, theo dõi hoạt động
- **Quản lý khóa học**: Kiểm soát nội dung toàn hệ thống
- **Thống kê hệ thống**: Dashboard admin với metrics quan trọng

## 🚀 Công nghệ sử dụng

### Frontend Framework
- **React 18**: Framework UI hiện đại với Hooks
- **TypeScript**: Type safety và developer experience tốt hơn
- **Vite**: Build tool nhanh và hiệu quả

### UI/UX
- **Tailwind CSS**: Utility-first CSS framework
- **Headless UI**: Accessible UI components
- **Lucide React**: Icon library đẹp và nhất quán
- **Framer Motion**: Animation library mạnh mẽ

### State Management
- **Zustand**: State management đơn giản và mạnh mẽ
- **React Query**: Data fetching và caching
- **React Hook Form**: Form handling với validation

### Internationalization
- **React i18next**: Hỗ trợ đa ngôn ngữ hoàn chỉnh
- **Language Detection**: Tự động phát hiện ngôn ngữ

### Development Tools
- **ESLint**: Code linting
- **Prettier**: Code formatting
- **TypeScript**: Static type checking

## 🛠 Cài đặt và chạy

### Yêu cầu hệ thống
- Node.js 18+ 
- npm hoặc yarn
- Backend API đang chạy (xem BEDB folder)

### Cài đặt

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd learning-app-fe
   ```

2. **Cài đặt dependencies**
   ```bash
   npm install
   # hoặc
   yarn install
   ```

3. **Cấu hình environment**
   ```bash
   cp .env.example .env
   ```
   
   Chỉnh sửa file `.env`:
   ```env
   VITE_API_URL=http://localhost:8000
   ```

4. **Chạy development server**
   ```bash
   npm run dev
   # hoặc
   yarn dev
   ```

   Ứng dụng sẽ chạy tại: http://localhost:3000

### Build cho production

```bash
npm run build
# hoặc
yarn build
```

### Preview production build

```bash
npm run preview
# hoặc
yarn preview
```

## 📁 Cấu trúc dự án

```
learning-app-fe/
├── public/                 # Static files
├── src/
│   ├── components/         # React components
│   │   ├── ui/            # Reusable UI components
│   │   └── layout/        # Layout components
│   ├── pages/             # Page components
│   │   ├── auth/          # Authentication pages
│   │   ├── courses/       # Course pages
│   │   ├── chat/          # Chat pages
│   │   ├── quiz/          # Quiz pages
│   │   └── admin/         # Admin pages
│   ├── services/          # API services
│   ├── stores/            # Zustand stores
│   ├── contexts/          # React contexts
│   ├── hooks/             # Custom hooks
│   ├── types/             # TypeScript types
│   ├── i18n/              # Internationalization
│   │   └── locales/       # Language files
│   ├── lib/               # Utility functions
│   └── styles/            # Global styles
├── .env.example           # Environment template
├── tailwind.config.js     # Tailwind configuration
├── tsconfig.json          # TypeScript configuration
└── vite.config.ts         # Vite configuration
```

## 🎨 Design System

### Colors
- **Primary**: #2563EB (Blue)
- **Secondary**: #FACC15 (Yellow)
- **Grayscale**: Gray-50 đến Gray-900

### Typography
- **Font**: Inter (Google Fonts)
- **Sizes**: Responsive typography scale

### Components
- **Buttons**: 3 variants (Primary, Secondary, Ghost)
- **Cards**: Rounded-2xl với shadow-md
- **Inputs**: Border gray-300, focus ring blue
- **Layout**: 12-column grid system

## 🌍 Đa ngôn ngữ

Ứng dụng hỗ trợ:
- 🇻🇳 Tiếng Việt (mặc định)
- 🇺🇸 English

### Thêm ngôn ngữ mới

1. Tạo file ngôn ngữ mới trong `src/i18n/locales/`
2. Import và thêm vào `src/i18n/index.ts`
3. Cập nhật `LanguageToggle` component

## 🎭 Animations

### Framer Motion Components
- **AnimatedPage**: Page transitions
- **FadeIn**: Fade in animations
- **StaggerContainer**: Stagger animations
- **FloatingButton**: Hover effects
- **ProgressRing**: Animated progress rings

### Sử dụng animations

```tsx
import { FadeIn, StaggerContainer, StaggerItem } from '@/components/ui';

<StaggerContainer>
  <StaggerItem>
    <FadeIn direction="up" delay={0.1}>
      <Card>Content</Card>
    </FadeIn>
  </StaggerItem>
</StaggerContainer>
```

## 🔌 API Integration

### Services
- **authService**: Authentication và user management
- **courseService**: Course CRUD operations
- **uploadService**: File upload và management
- **chatService**: AI chat functionality
- **quizService**: Quiz generation và submission
- **dashboardService**: Progress tracking
- **adminService**: Admin operations

### API Base URL
Tất cả API calls sử dụng base path: `/api/v1/`

### Error Handling
- Automatic error toasts
- Token refresh handling
- Network error recovery
- Validation error display

## 🔐 Authentication

### JWT Tokens
- Access token cho API calls
- Refresh token cho token renewal
- Automatic token refresh
- Persistent login state

### Protected Routes
- Route protection dựa trên authentication
- Role-based access control
- Redirect handling

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px  
- **Desktop**: > 1024px
- **Large**: > 1440px

### Mobile Features
- Collapsible sidebar
- Touch-friendly interactions
- Optimized layouts
- Swipe gestures

## 🧪 Testing

### Unit Tests
```bash
npm run test
```

### E2E Tests
```bash
npm run test:e2e
```

### Linting
```bash
npm run lint
```

## 🚀 Deployment

### Vercel (Recommended)
1. Connect repository to Vercel
2. Set environment variables
3. Deploy automatically

### Netlify
1. Build command: `npm run build`
2. Publish directory: `dist`
3. Set environment variables

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Error**
   - Kiểm tra VITE_API_URL trong .env
   - Đảm bảo backend đang chạy

2. **Build Errors**
   - Xóa node_modules và reinstall
   - Kiểm tra TypeScript errors

3. **Translation Missing**
   - Kiểm tra key trong translation files
   - Restart dev server

### Debug Mode
```bash
VITE_DEBUG=true npm run dev
```

## 🤝 Contributing

### Development Workflow
1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

### Code Style
- Sử dụng Prettier cho formatting
- Follow ESLint rules
- TypeScript strict mode
- Component naming: PascalCase

## 📄 License

MIT License - xem file LICENSE để biết chi tiết.

## 🙋‍♂️ Hỗ trợ

### Tài liệu
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Framer Motion](https://framer.com/motion)
- [Zustand](https://zustand-demo.pmnd.rs)

### Liên hệ
- 📧 Email: support@ailearning.com
- 💬 Discord: [AI Learning Community]
- 🐛 Issues: [GitHub Issues]

---

**🎉 Chúc bạn có trải nghiệm tuyệt vời với AI Learning Platform!**
