# Hướng Dẫn Triển Khai - Nền Tảng Học Tập AI

Tài liệu này hướng dẫn chi tiết cách triển khai Nền Tảng Học Tập AI lên môi trường production với các nền tảng phổ biến.

## Tổng Quan Triển Khai

### Các Môi Trường

1. **Development** - Máy local developer
2. **Staging** - Môi trường test giống production
3. **Production** - Môi trường thực tế phục vụ người dùng

### Kiến Trúc Production

```
Internet
    ↓
Load Balancer/CDN
    ↓
┌─────────────────┬─────────────────┐
│   Frontend      │   Backend API   │
│   (Static)      │   (Server)      │
└─────────────────┴─────────────────┘
                      ↓
                ┌─────────────────┐
                │   MongoDB       │
                │   Atlas         │
                └─────────────────┘
```

## Triển Khai Backend

### 1. Chuẩn Bị Production

#### Environment Variables Production

Tạo file `.env.production`:
```env
# Database
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/ai_learning_app?retryWrites=true&w=majority
DATABASE_NAME=ai_learning_app

# Security
SECRET_KEY=your-very-secure-production-secret-key-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google AI
GOOGLE_API_KEY=your-production-google-api-key

# Application
DEBUG=False
HOST=0.0.0.0
PORT=8000

# File Upload
MAX_FILE_SIZE=10485760
UPLOAD_DIR=/app/uploads

# CORS
ALLOWED_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]

# Additional Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

#### Production Dependencies

Cập nhật `requirements.txt`:
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
beanie==1.23.6
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
google-generativeai==0.3.0
pymongo==4.6.0
python-dotenv==1.0.0
aiofiles==23.2.1
PyPDF2==3.0.1
python-docx==1.1.0
python-magic==0.4.27
# Production additions
gunicorn==21.2.0
sentry-sdk[fastapi]==1.38.0
redis==5.0.1
celery==5.3.4
```

### 2. Docker Deployment

#### Dockerfile

```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libmagic1 \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create uploads directory
RUN mkdir -p uploads && chmod 755 uploads

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=${MONGODB_URL}
      - SECRET_KEY=${SECRET_KEY}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    restart: unless-stopped
    depends_on:
      - redis
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: unless-stopped
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  uploads:
  logs:
```

#### nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:8000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        # SSL configuration
        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # API proxy
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        # Health check
        location /health {
            proxy_pass http://api/health;
        }

        # File uploads
        location /uploads/ {
            client_max_body_size 10M;
            proxy_pass http://api;
        }
    }
}
```

### 3. Cloud Deployment Options

#### A. DigitalOcean Droplet

```bash
# 1. Tạo Droplet (Ubuntu 22.04, 2GB RAM, 1 vCPU)

# 2. Cài đặt Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker $USER

# 3. Cài đặt Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. Clone code và deploy
git clone your-repo
cd your-repo/BEDB
docker-compose up -d
```

#### B. AWS EC2

```bash
# 1. Launch EC2 instance (t3.medium, Ubuntu 22.04)
# 2. Configure Security Groups (80, 443, 22)
# 3. Install Docker và Docker Compose
# 4. Deploy với docker-compose

# Auto-scaling configuration
# Load Balancer setup
# RDS for MongoDB alternative
```

#### C. Google Cloud Platform

```bash
# 1. Create Compute Engine instance
# 2. Setup Cloud SQL for MongoDB
# 3. Configure Load Balancer
# 4. Setup Cloud CDN
```

#### D. Railway (Recommended for simplicity)

```bash
# 1. Connect GitHub repository
# 2. Set environment variables
# 3. Automatic deployment from main branch
```

### 4. Database Setup

#### MongoDB Atlas Production

1. **Tạo Cluster**
   - Chọn region gần users
   - M10 trở lên cho production
   - Enable backup

2. **Security Configuration**
   ```javascript
   // Database Users
   username: api-user
   password: secure-random-password
   roles: readWrite

   // Network Access
   0.0.0.0/0 (với VPC peering tốt hơn)
   ```

3. **Connection String**
   ```
   mongodb+srv://api-user:password@cluster.mongodb.net/ai_learning_app?retryWrites=true&w=majority
   ```

#### Database Migration

```bash
# Backup development data
mongodump --uri="mongodb://localhost:27017/ai_learning_app" --out=backup/

# Restore to production
mongorestore --uri="mongodb+srv://user:pass@cluster.mongodb.net/ai_learning_app" backup/ai_learning_app/
```

## Triển Khai Frontend

### 1. Build Production

#### Environment Variables

Tạo `.env.production`:
```env
VITE_API_URL=https://api.yourdomain.com
VITE_APP_NAME=Nền Tảng Học Tập AI
VITE_APP_VERSION=1.0.0
VITE_SENTRY_DSN=your-sentry-dsn
```

#### Build Commands

```bash
# Install dependencies
npm ci --only=production

# Build for production
npm run build

# Preview build locally
npm run preview
```

### 2. Vercel Deployment (Recommended)

#### vercel.json

```json
{
  "framework": "vite",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm ci",
  "functions": {
    "app/api/**/*.js": {
      "runtime": "nodejs18.x"
    }
  },
  "rewrites": [
    {
      "source": "/((?!api/.*).*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        }
      ]
    }
  ]
}
```

#### Deployment Steps

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod

# Set custom domain
vercel domains add yourdomain.com
```

### 3. Netlify Deployment

#### netlify.toml

```toml
[build]
  publish = "dist"
  command = "npm run build"

[build.environment]
  NODE_VERSION = "18"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "/static/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
```

#### Deployment Steps

```bash
# Connect repository to Netlify
# Set environment variables
# Deploy from main branch automatically
```

### 4. Static Hosting với CDN

#### AWS S3 + CloudFront

```bash
# 1. Create S3 bucket
aws s3 mb s3://your-app-frontend

# 2. Upload build files
aws s3 sync dist/ s3://your-app-frontend

# 3. Configure CloudFront distribution
# 4. Set up custom domain
```

## SSL/TLS Configuration

### 1. Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 2. CloudFlare (Recommended)

1. Add domain to CloudFlare
2. Update nameservers
3. Enable "Full (strict)" SSL
4. Enable additional security features

## Monitoring và Logging

### 1. Application Monitoring

#### Sentry Integration

**Backend:**
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,
)
```

**Frontend:**
```typescript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "your-sentry-dsn",
  integrations: [new Sentry.BrowserTracing()],
  tracesSampleRate: 0.1,
});
```

### 2. Server Monitoring

#### Basic Monitoring Script

```bash
#!/bin/bash
# monitor.sh

# Check API health
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "API is healthy"
else
    echo "API is down - restarting"
    docker-compose restart api
fi

# Check disk space
df -h | awk '$5 > 80 {print "Disk space warning: " $0}'

# Check memory usage
free -m | awk 'NR==2{printf "Memory Usage: %s/%sMB (%.2f%%)\n", $3,$2,$3*100/$2 }'
```

#### Cron job setup

```bash
# Add to crontab
*/5 * * * * /path/to/monitor.sh
```

## Backup và Recovery

### 1. Database Backup

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Create backup
mongodump --uri="$MONGODB_URL" --out="$BACKUP_DIR/$DATE"

# Compress backup
tar -czf "$BACKUP_DIR/$DATE.tar.gz" "$BACKUP_DIR/$DATE"
rm -rf "$BACKUP_DIR/$DATE"

# Upload to cloud storage (optional)
# aws s3 cp "$BACKUP_DIR/$DATE.tar.gz" s3://your-backup-bucket/

# Clean old backups (keep 7 days)
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete
```

### 2. Automated Backup

```bash
# Daily backup at 2 AM
0 2 * * * /path/to/backup.sh
```

## Performance Optimization

### 1. Backend Optimization

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# CORS optimization
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### 2. Frontend Optimization

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@headlessui/react', 'framer-motion'],
        },
      },
    },
    chunkSizeWarningLimit: 1000,
  },
});
```

## Security Checklist

### Production Security

- [ ] Environment variables không được commit
- [ ] HTTPS bắt buộc
- [ ] CORS configured chính xác
- [ ] Rate limiting enabled
- [ ] Input validation đầy đủ
- [ ] SQL injection protection
- [ ] XSS protection
- [ ] CSRF protection
- [ ] Security headers configured
- [ ] Regular security updates
- [ ] Monitoring và alerting
- [ ] Backup strategy
- [ ] Access logs
- [ ] Firewall rules
- [ ] VPN access cho admin

## Troubleshooting Production

### Common Issues

1. **API không accessible**
   - Kiểm tra firewall rules
   - Kiểm tra nginx configuration
   - Kiểm tra SSL certificates

2. **Database connection errors**
   - Kiểm tra MongoDB Atlas whitelist
   - Kiểm tra connection string
   - Kiểm tra network connectivity

3. **Frontend không load**
   - Kiểm tra CDN configuration
   - Kiểm tra DNS records
   - Kiểm tra build errors

4. **Performance issues**
   - Kiểm tra server resources
   - Optimize database queries
   - Enable caching
   - Check CDN performance

### Emergency Procedures

1. **Rollback deployment**
   ```bash
   # Docker rollback
   docker-compose down
   git checkout previous-version
   docker-compose up -d
   ```

2. **Database recovery**
   ```bash
   # Restore from backup
   mongorestore --uri="$MONGODB_URL" backup/latest/
   ```

3. **Scale up resources**
   ```bash
   # Increase server resources
   # Add more replicas
   docker-compose up -d --scale api=3
   ```


### Update Procedures

```bash
# 1. Backup current state
./backup.sh

# 2. Update code
git pull origin main

# 3. Update dependencies
pip install -r requirements.txt

# 4. Run migrations (if any)
python scripts/migrate.py

# 5. Restart services
docker-compose restart
```

Với tài liệu này, bạn có thể triển khai thành công Nền Tảng Học Tập AI lên môi trường production một cách an toàn và hiệu quả.