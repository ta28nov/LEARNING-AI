# 🚀 Hướng dẫn Deploy

## 📋 Tổng quan

Tài liệu này hướng dẫn deploy AI Learning Platform Frontend lên các nền tảng phổ biến.

## 🔧 Chuẩn bị

### Build Requirements
- Node.js 18+
- npm hoặc yarn
- Backend API đang chạy và accessible

### Environment Variables
```bash
# Production environment
VITE_API_URL=https://your-api-domain.com
VITE_APP_NAME=AI Learning Platform
VITE_APP_VERSION=1.0.0
```

### Pre-deployment Checklist
- [ ] Backend API deployed và accessible
- [ ] Environment variables configured
- [ ] SSL certificates setup
- [ ] Domain name configured
- [ ] CDN setup (optional)
- [ ] Error monitoring configured

## 🌐 Vercel Deployment (Recommended)

### Automatic Deployment

1. **Connect Repository**
   ```bash
   # Push code to GitHub/GitLab
   git push origin main
   ```

2. **Import Project**
   - Đăng nhập [Vercel](https://vercel.com)
   - Click "New Project"
   - Import repository
   - Configure settings:
     - Framework: Vite
     - Build Command: `npm run build`
     - Output Directory: `dist`

3. **Environment Variables**
   ```
   VITE_API_URL = https://your-api-domain.com
   ```

4. **Deploy**
   - Click "Deploy"
   - Vercel sẽ tự động build và deploy

### Manual Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

### Custom Domain
```bash
# Add custom domain
vercel domains add yourdomain.com
vercel alias your-project.vercel.app yourdomain.com
```

## 📦 Netlify Deployment

### Git-based Deployment

1. **Connect Repository**
   - Đăng nhập [Netlify](https://netlify.com)
   - Click "New site from Git"
   - Choose repository

2. **Build Settings**
   ```
   Build command: npm run build
   Publish directory: dist
   ```

3. **Environment Variables**
   ```
   VITE_API_URL = https://your-api-domain.com
   ```

### Manual Deployment

```bash
# Build project
npm run build

# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir=dist
```

### Custom Domain & SSL
```bash
# Add custom domain
netlify domains:add yourdomain.com

# SSL is automatically configured
```

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### nginx.conf
```nginx
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    
    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;
        
        # Handle client-side routing
        location / {
            try_files $uri $uri/ /index.html;
        }
        
        # Gzip compression
        gzip on;
        gzip_types text/css application/javascript application/json;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### Docker Commands
```bash
# Build image
docker build -t ai-learning-frontend .

# Run container
docker run -p 80:80 ai-learning-frontend

# With environment variables
docker run -p 80:80 -e VITE_API_URL=https://api.example.com ai-learning-frontend
```

### Docker Compose
```yaml
version: '3.8'

services:
  frontend:
    build: .
    ports:
      - "80:80"
    environment:
      - VITE_API_URL=https://api.example.com
    restart: unless-stopped
    
  # Optional: Add backend service
  backend:
    image: ai-learning-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mongodb://mongo:27017/ai_learning
    depends_on:
      - mongo
      
  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
      
volumes:
  mongo_data:
```

## ☁️ AWS Deployment

### S3 + CloudFront

1. **Build Project**
   ```bash
   npm run build
   ```

2. **Create S3 Bucket**
   ```bash
   aws s3 mb s3://your-app-bucket
   aws s3 website s3://your-app-bucket --index-document index.html --error-document index.html
   ```

3. **Upload Files**
   ```bash
   aws s3 sync dist/ s3://your-app-bucket --delete
   ```

4. **Create CloudFront Distribution**
   ```json
   {
     "Origins": [{
       "DomainName": "your-app-bucket.s3.amazonaws.com",
       "Id": "S3-your-app-bucket",
       "S3OriginConfig": {
         "OriginAccessIdentity": ""
       }
     }],
     "DefaultCacheBehavior": {
       "TargetOriginId": "S3-your-app-bucket",
       "ViewerProtocolPolicy": "redirect-to-https"
     }
   }
   ```

### EC2 Deployment

```bash
# Connect to EC2
ssh -i your-key.pem ec2-user@your-instance-ip

# Install Node.js
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18

# Install nginx
sudo yum update -y
sudo yum install -y nginx

# Clone and build
git clone your-repo
cd learning-app-fe
npm install
npm run build

# Copy files to nginx
sudo cp -r dist/* /var/www/html/

# Configure nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

## 🌊 DigitalOcean App Platform

### app.yaml
```yaml
name: ai-learning-frontend
services:
- name: web
  source_dir: /
  github:
    repo: your-username/learning-app-fe
    branch: main
  run_command: npm start
  environment_slug: node-js
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: VITE_API_URL
    value: https://your-api-domain.com
  http_port: 3000
  routes:
  - path: /
```

### Deploy
```bash
# Install doctl
snap install doctl

# Login
doctl auth init

# Create app
doctl apps create --spec app.yaml

# Update app
doctl apps update your-app-id --spec app.yaml
```

## 🏗️ GitHub Pages

### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Build
      run: npm run build
      env:
        VITE_API_URL: ${{ secrets.VITE_API_URL }}
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./dist
```

## 🔍 Monitoring & Analytics

### Error Tracking (Sentry)
```tsx
// src/main.tsx
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "YOUR_SENTRY_DSN",
  environment: import.meta.env.MODE,
});
```

### Performance Monitoring
```tsx
// Web Vitals
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getFCP(console.log);
getLCP(console.log);
getTTFB(console.log);
```

### Analytics (Google Analytics)
```tsx
// src/lib/analytics.ts
import { gtag } from 'ga-gtag';

gtag('config', 'GA_MEASUREMENT_ID', {
  page_title: document.title,
  page_location: window.location.href,
});
```

## 🔒 Security Best Practices

### Content Security Policy
```html
<!-- index.html -->
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src 'self' 'unsafe-inline';
  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
  font-src 'self' https://fonts.gstatic.com;
  img-src 'self' data: https:;
  connect-src 'self' https://your-api-domain.com;
">
```

### Environment Security
```bash
# Không commit sensitive data
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
echo ".env.production" >> .gitignore
```

### HTTPS Enforcement
```nginx
# nginx.conf
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # ... rest of config
}
```

## 🚨 Troubleshooting

### Common Deployment Issues

1. **Build Failures**
   ```bash
   # Clear cache
   rm -rf node_modules package-lock.json
   npm install
   
   # Check TypeScript errors
   npx tsc --noEmit
   ```

2. **Environment Variables Not Working**
   ```bash
   # Verify variables start with VITE_
   echo $VITE_API_URL
   
   # Check build output
   grep -r "VITE_" dist/
   ```

3. **Routing Issues (404 on refresh)**
   ```nginx
   # nginx.conf - Add try_files
   location / {
       try_files $uri $uri/ /index.html;
   }
   ```

4. **CORS Errors**
   ```typescript
   // Verify API URL in production
   console.log('API URL:', import.meta.env.VITE_API_URL);
   ```

### Performance Issues

1. **Large Bundle Size**
   ```bash
   # Analyze bundle
   npm run build -- --analyze
   
   # Check for large dependencies
   npx webpack-bundle-analyzer dist/
   ```

2. **Slow Loading**
   ```typescript
   // Implement code splitting
   const LazyComponent = lazy(() => import('./Component'));
   ```

### Health Checks

```bash
# Check if app is running
curl -f http://your-domain.com/health || exit 1

# Check API connectivity
curl -f http://your-domain.com/api/health || exit 1
```

## 📊 Performance Optimization

### Build Optimization
```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@headlessui/react', 'framer-motion'],
        }
      }
    }
  }
});
```

### CDN Configuration
```html
<!-- Preload critical resources -->
<link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/api/v1/auth/me" as="fetch" crossorigin>
```

---

**🎉 Chúc mừng! Frontend của bạn đã sẵn sàng cho production! 🚀**
