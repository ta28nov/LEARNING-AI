# 👩‍💻 Hướng dẫn Development

## 🚀 Bắt đầu nhanh

### Prerequisites
```bash
# Kiểm tra version Node.js
node --version  # >= 18.0.0

# Kiểm tra npm
npm --version   # >= 8.0.0
```

### Setup dự án
```bash
# Clone và cài đặt
git clone <repository-url>
cd learning-app-fe
npm install

# Copy environment file
cp .env.example .env

# Chạy development server
npm run dev
```

## 📁 Cấu trúc thư mục chi tiết

```
src/
├── components/
│   ├── ui/                 # Base UI components
│   │   ├── Button.tsx      # Button variants
│   │   ├── Card.tsx        # Card layouts
│   │   ├── Input.tsx       # Form inputs
│   │   ├── Modal.tsx       # Modal dialogs
│   │   ├── ThemeToggle.tsx # Dark/Light toggle
│   │   └── ...
│   ├── layout/             # Layout components
│   │   ├── DashboardLayout.tsx
│   │   └── ProtectedRoute.tsx
│   └── features/           # Feature-specific components
├── pages/                  # Route pages
│   ├── auth/              # Authentication
│   ├── courses/           # Course management
│   ├── chat/              # AI Chat
│   ├── quiz/              # Quiz system
│   └── admin/             # Admin panel
├── services/              # API integration
├── stores/                # Zustand state stores
├── hooks/                 # Custom React hooks
├── contexts/              # React contexts
├── types/                 # TypeScript definitions
├── i18n/                  # Internationalization
└── lib/                   # Utility functions
```

## 🎨 Component Development

### Base UI Components

#### Button Component
```tsx
import { Button } from '@/components/ui/Button';

// Variants
<Button variant="primary">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="outline">Outline</Button>

// Sizes
<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>

// States
<Button isLoading>Loading...</Button>
<Button disabled>Disabled</Button>
```

#### Card Component
```tsx
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';

<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>
    Content here
  </CardContent>
</Card>
```

#### Input Component
```tsx
import { Input } from '@/components/ui/Input';
import { Mail } from 'lucide-react';

<Input 
  label="Email"
  type="email"
  icon={<Mail className="h-4 w-4" />}
  error="Email is required"
/>
```

### Animation Components

#### FadeIn Animation
```tsx
import { FadeIn } from '@/components/ui/FadeIn';

<FadeIn direction="up" delay={0.2}>
  <div>Animated content</div>
</FadeIn>
```

#### Stagger Animations
```tsx
import { StaggerContainer, StaggerItem } from '@/components/ui/StaggerContainer';

<StaggerContainer>
  {items.map((item, index) => (
    <StaggerItem key={index}>
      <Card>{item.content}</Card>
    </StaggerItem>
  ))}
</StaggerContainer>
```

## 🌍 Internationalization (i18n)

### Sử dụng translations
```tsx
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation();
  
  return (
    <div>
      <h1>{t('common.welcome')}</h1>
      <p>{t('dashboard.subtitle')}</p>
    </div>
  );
}
```

### Thêm translation keys
```json
// src/i18n/locales/vi.json
{
  "common": {
    "welcome": "Chào mừng",
    "loading": "Đang tải..."
  },
  "dashboard": {
    "title": "Bảng điều khiển",
    "subtitle": "Tổng quan học tập của bạn"
  }
}
```

### Pluralization
```tsx
// Translation với số lượng
{t('courses.count', { count: courseCount })}

// Trong translation file:
{
  "courses": {
    "count_zero": "Không có khóa học nào",
    "count_one": "{{count}} khóa học",
    "count_other": "{{count}} khóa học"
  }
}
```

## 🎭 Theme System

### Sử dụng Theme Context
```tsx
import { useTheme } from '@/contexts/ThemeContext';

function MyComponent() {
  const { theme, actualTheme, setTheme, toggleTheme } = useTheme();
  
  return (
    <div>
      <p>Current theme: {actualTheme}</p>
      <button onClick={toggleTheme}>
        Toggle Theme
      </button>
    </div>
  );
}
```

### Dark Mode Classes
```tsx
// Tailwind dark mode classes
<div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white">
  Content adapts to theme
</div>
```

## 📊 State Management

### Zustand Stores

#### Creating a Store
```tsx
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface MyState {
  count: number;
  increment: () => void;
  decrement: () => void;
}

export const useMyStore = create<MyState>()(
  persist(
    (set) => ({
      count: 0,
      increment: () => set((state) => ({ count: state.count + 1 })),
      decrement: () => set((state) => ({ count: state.count - 1 })),
    }),
    {
      name: 'my-storage',
    }
  )
);
```

#### Using Store in Component
```tsx
import { useMyStore } from '@/stores/myStore';

function Counter() {
  const { count, increment, decrement } = useMyStore();
  
  return (
    <div>
      <span>{count}</span>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
}
```

### Auth Store Example
```tsx
const { user, isAuthenticated, login, logout } = useAuthStore();

// Conditional rendering
{isAuthenticated ? (
  <DashboardLayout />
) : (
  <LoginPage />
)}
```

## 🔌 API Integration

### Service Pattern
```tsx
// services/myService.ts
import { apiClient } from './api';

export const myService = {
  async getItems(): Promise<Item[]> {
    return apiClient.get('/api/v1/items');
  },
  
  async createItem(data: CreateItemData): Promise<Item> {
    return apiClient.post('/api/v1/items', data);
  },
  
  async updateItem(id: string, data: UpdateItemData): Promise<Item> {
    return apiClient.patch(`/api/v1/items/${id}`, data);
  },
  
  async deleteItem(id: string): Promise<void> {
    return apiClient.delete(`/api/v1/items/${id}`);
  },
};
```

### Error Handling
```tsx
// Trong component
try {
  await myService.createItem(data);
  toast.success('Item created successfully!');
} catch (error) {
  // Error được handle tự động bởi API client
  console.error('Failed to create item:', error);
}
```

### Loading States
```tsx
function MyComponent() {
  const [isLoading, setIsLoading] = useState(false);
  
  const handleSubmit = async (data) => {
    setIsLoading(true);
    try {
      await myService.createItem(data);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <Button isLoading={isLoading} onClick={handleSubmit}>
      Submit
    </Button>
  );
}
```

## 🛡️ TypeScript Best Practices

### Component Props
```tsx
interface MyComponentProps {
  title: string;
  count?: number;
  onSubmit: (data: FormData) => void;
  children?: React.ReactNode;
}

function MyComponent({ title, count = 0, onSubmit, children }: MyComponentProps) {
  // Component implementation
}
```

### API Types
```tsx
// types/index.ts
export interface User {
  id: string;
  name: string;
  email: string;
  role: 'student' | 'instructor' | 'admin';
  created_at: string;
}

export interface CreateUserRequest {
  name: string;
  email: string;
  password: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
}
```

### Generic Components
```tsx
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <div>
      {items.map((item, index) => (
        <div key={keyExtractor(item)}>
          {renderItem(item, index)}
        </div>
      ))}
    </div>
  );
}
```

## 🎨 Styling Guidelines

### Tailwind CSS Best Practices
```tsx
// Component-specific styles
const cardStyles = "bg-white dark:bg-gray-800 rounded-2xl shadow-md p-6";
const buttonStyles = "px-4 py-2 rounded-lg font-medium transition-colors";

// Conditional classes
const buttonVariant = variant === 'primary' 
  ? 'bg-primary-600 text-white hover:bg-primary-700'
  : 'bg-gray-200 text-gray-900 hover:bg-gray-300';
```

### Responsive Design
```tsx
<div className="
  grid 
  grid-cols-1 
  md:grid-cols-2 
  lg:grid-cols-3 
  gap-4 
  md:gap-6 
  lg:gap-8
">
  {/* Responsive grid */}
</div>
```

### Custom CSS Classes
```css
/* src/index.css */
@layer components {
  .btn-primary {
    @apply bg-primary-600 text-white px-4 py-2 rounded-lg font-medium;
    @apply hover:bg-primary-700 active:bg-primary-800;
    @apply focus:outline-none focus:ring-2 focus:ring-primary-500;
  }
}
```

## 🧪 Testing

### Component Testing
```tsx
import { render, screen } from '@testing-library/react';
import { Button } from '@/components/ui/Button';

describe('Button Component', () => {
  test('renders button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
  
  test('shows loading state', () => {
    render(<Button isLoading>Loading</Button>);
    expect(screen.getByText('Loading')).toBeInTheDocument();
  });
});
```

### Store Testing
```tsx
import { renderHook, act } from '@testing-library/react';
import { useMyStore } from '@/stores/myStore';

describe('MyStore', () => {
  test('increments count', () => {
    const { result } = renderHook(() => useMyStore());
    
    act(() => {
      result.current.increment();
    });
    
    expect(result.current.count).toBe(1);
  });
});
```

## 🚀 Performance Optimization

### Code Splitting
```tsx
import { lazy, Suspense } from 'react';

const AdminPage = lazy(() => import('@/pages/admin/AdminPage'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <AdminPage />
    </Suspense>
  );
}
```

### Memoization
```tsx
import { memo, useMemo, useCallback } from 'react';

const ExpensiveComponent = memo(({ data, onUpdate }) => {
  const processedData = useMemo(() => {
    return data.map(item => ({ ...item, processed: true }));
  }, [data]);
  
  const handleClick = useCallback((id) => {
    onUpdate(id);
  }, [onUpdate]);
  
  return (
    <div>
      {processedData.map(item => (
        <div key={item.id} onClick={() => handleClick(item.id)}>
          {item.name}
        </div>
      ))}
    </div>
  );
});
```

## 🐛 Debugging

### Development Tools
```tsx
// Debug component renders
console.log('Component rendered:', { props, state });

// Debug API calls
console.log('API request:', { url, data });
console.log('API response:', response);
```

### Error Boundaries
```tsx
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert">
      <h2>Something went wrong:</h2>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary FallbackComponent={ErrorFallback}>
      <MyComponent />
    </ErrorBoundary>
  );
}
```

## 📦 Build & Deployment

### Environment Variables
```bash
# .env.local (development)
VITE_API_URL=http://localhost:8000
VITE_DEBUG=true

# .env.production
VITE_API_URL=https://api.production.com
VITE_DEBUG=false
```

### Build Optimization
```bash
# Analyze bundle size
npm run build -- --analyze

# Build with specific environment
NODE_ENV=production npm run build
```

### Deployment Checklist
- [ ] Environment variables configured
- [ ] API endpoints accessible
- [ ] Static assets optimized
- [ ] Error tracking setup
- [ ] Performance monitoring
- [ ] SEO meta tags
- [ ] PWA manifest (if needed)

## 🔧 Troubleshooting

### Common Issues

1. **Hot reload not working**
   ```bash
   # Clear cache and restart
   rm -rf node_modules/.vite
   npm run dev
   ```

2. **TypeScript errors**
   ```bash
   # Check TypeScript
   npx tsc --noEmit
   ```

3. **Build failures**
   ```bash
   # Clear and reinstall
   rm -rf node_modules package-lock.json
   npm install
   ```

### Debug Mode
```bash
# Enable debug logging
VITE_DEBUG=true npm run dev

# Verbose logging
DEBUG=* npm run dev
```

---

**Happy coding! 🎉**
