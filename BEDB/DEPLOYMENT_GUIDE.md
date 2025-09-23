# Deployment Guide

## Overview

This guide covers deploying the AI Learning Application backend to various platforms and environments. The application is built with FastAPI and can be deployed using Docker, cloud platforms, or traditional server setups.

## Prerequisites

- Python 3.11+
- MongoDB (local or Atlas)
- Google API key for GenAI
- Domain name (for production)
- SSL certificate (for production)

## Environment Setup

### 1. Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_learning_app

# JWT Configuration
SECRET_KEY=your-very-secure-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google GenAI Configuration
GOOGLE_API_KEY=your-google-api-key-here

# Application Configuration
DEBUG=False
HOST=0.0.0.0
PORT=8000

# File Upload Configuration
MAX_FILE_SIZE=10485760  # 10MB
UPLOAD_DIR=uploads

# CORS Configuration
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 2. Security Considerations

- Use a strong, random secret key for JWT
- Enable HTTPS in production
- Set up proper CORS origins
- Use environment variables for sensitive data
- Implement rate limiting
- Set up monitoring and logging

## Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongodb:27017
      - DATABASE_NAME=ai_learning_app
      - SECRET_KEY=your-secret-key
      - GOOGLE_API_KEY=your-google-api-key
      - DEBUG=False
    volumes:
      - ./uploads:/app/uploads
    depends_on:
      - mongodb
    restart: unless-stopped

  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password
    volumes:
      - mongodb_data:/data/db
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped

volumes:
  mongodb_data:
```

### 3. Create nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    upstream app {
        server app:8000;
    }

    server {
        listen 80;
        server_name yourdomain.com www.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        client_max_body_size 10M;

        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /health {
            proxy_pass http://app/health;
            access_log off;
        }
    }
}
```

### 4. Deploy with Docker

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

## Cloud Deployment

### AWS Deployment

#### 1. Using AWS App Runner

```yaml
# apprunner.yaml
version: 1.0
runtime: python3
build:
  commands:
    build:
      - echo "Installing dependencies..."
      - pip install -r requirements.txt
run:
  runtime-version: 3.11.0
  command: uvicorn app.main:app --host 0.0.0.0 --port 8000
  network:
    port: 8000
    env: PORT
  env:
    - name: MONGODB_URL
      value: "mongodb+srv://username:password@cluster.mongodb.net/"
    - name: SECRET_KEY
      value: "your-secret-key"
    - name: GOOGLE_API_KEY
      value: "your-google-api-key"
```

#### 2. Using AWS ECS with Fargate

```yaml
# task-definition.json
{
  "family": "ai-learning-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "ai-learning-app",
      "image": "your-account.dkr.ecr.region.amazonaws.com/ai-learning-app:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "MONGODB_URL",
          "value": "mongodb+srv://username:password@cluster.mongodb.net/"
        },
        {
          "name": "SECRET_KEY",
          "value": "your-secret-key"
        },
        {
          "name": "GOOGLE_API_KEY",
          "value": "your-google-api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/ai-learning-app",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Google Cloud Platform

#### 1. Using Cloud Run

```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/ai-learning-app', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/ai-learning-app']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: [
      'run', 'deploy', 'ai-learning-app',
      '--image', 'gcr.io/$PROJECT_ID/ai-learning-app',
      '--region', 'us-central1',
      '--platform', 'managed',
      '--allow-unauthenticated',
      '--set-env-vars', 'MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/',
      '--set-env-vars', 'SECRET_KEY=your-secret-key',
      '--set-env-vars', 'GOOGLE_API_KEY=your-google-api-key'
    ]
```

#### 2. Deploy to Cloud Run

```bash
# Build and deploy
gcloud builds submit --config cloudbuild.yaml

# Or deploy directly
gcloud run deploy ai-learning-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/ \
  --set-env-vars SECRET_KEY=your-secret-key \
  --set-env-vars GOOGLE_API_KEY=your-google-api-key
```

### Azure Deployment

#### 1. Using Azure Container Instances

```yaml
# azure-deploy.yaml
apiVersion: 2018-10-01
location: eastus
name: ai-learning-app
properties:
  containers:
  - name: ai-learning-app
    properties:
      image: your-registry.azurecr.io/ai-learning-app:latest
      resources:
        requests:
          cpu: 1
          memoryInGb: 2
      ports:
      - port: 8000
      environmentVariables:
      - name: MONGODB_URL
        value: mongodb+srv://username:password@cluster.mongodb.net/
      - name: SECRET_KEY
        value: your-secret-key
      - name: GOOGLE_API_KEY
        value: your-google-api-key
  osType: Linux
  ipAddress:
    type: Public
    ports:
    - protocol: tcp
      port: 8000
  restartPolicy: Always
type: Microsoft.ContainerInstance/containerGroups
```

## Traditional Server Deployment

### 1. Ubuntu/Debian Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-dev -y

# Install system dependencies
sudo apt install gcc g++ libmagic1 -y

# Create application user
sudo useradd -m -s /bin/bash appuser
sudo mkdir -p /opt/ai-learning-app
sudo chown appuser:appuser /opt/ai-learning-app

# Switch to application user
sudo su - appuser

# Create virtual environment
cd /opt/ai-learning-app
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create uploads directory
mkdir -p uploads

# Create systemd service
sudo tee /etc/systemd/system/ai-learning-app.service > /dev/null <<EOF
[Unit]
Description=AI Learning Application
After=network.target

[Service]
Type=exec
User=appuser
Group=appuser
WorkingDirectory=/opt/ai-learning-app
Environment=PATH=/opt/ai-learning-app/venv/bin
ExecStart=/opt/ai-learning-app/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable ai-learning-app
sudo systemctl start ai-learning-app
```

### 2. Nginx Configuration

```nginx
# /etc/nginx/sites-available/ai-learning-app
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        access_log off;
    }
}
```

### 3. SSL Certificate with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

## Database Setup

### MongoDB Atlas

1. Create a MongoDB Atlas account
2. Create a new cluster
3. Create a database user
4. Whitelist your IP addresses
5. Get the connection string
6. Update your environment variables

### Local MongoDB

```bash
# Install MongoDB
sudo apt install mongodb -y

# Start MongoDB service
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Create database and user
mongo
use ai_learning_app
db.createUser({
  user: "appuser",
  pwd: "password",
  roles: [{ role: "readWrite", db: "ai_learning_app" }]
})
```

## Monitoring and Logging

### 1. Application Logs

```python
# Add to app/main.py
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('logs/app.log', maxBytes=10485760, backupCount=5),
        logging.StreamHandler()
    ]
)
```

### 2. Health Checks

```python
# Add to app/main.py
@app.get("/health")
async def health_check():
    try:
        # Check database connection
        await init_db()
        return {"status": "healthy", "timestamp": datetime.utcnow()}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

### 3. Prometheus Metrics

```python
# Add to requirements.txt
prometheus-client==0.19.0

# Add to app/main.py
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.middleware("http")
async def add_prometheus_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_DURATION.observe(time.time() - start_time)
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

## Backup and Recovery

### 1. Database Backup

```bash
# MongoDB backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups"
mkdir -p $BACKUP_DIR

# Backup MongoDB
mongodump --uri="mongodb://username:password@localhost:27017/ai_learning_app" \
  --out="$BACKUP_DIR/mongodb_backup_$DATE"

# Compress backup
tar -czf "$BACKUP_DIR/mongodb_backup_$DATE.tar.gz" "$BACKUP_DIR/mongodb_backup_$DATE"
rm -rf "$BACKUP_DIR/mongodb_backup_$DATE"

# Keep only last 7 days of backups
find $BACKUP_DIR -name "mongodb_backup_*.tar.gz" -mtime +7 -delete
```

### 2. File Backup

```bash
# File backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups"
UPLOAD_DIR="/opt/ai-learning-app/uploads"

# Backup uploads
tar -czf "$BACKUP_DIR/uploads_backup_$DATE.tar.gz" "$UPLOAD_DIR"

# Keep only last 7 days of backups
find $BACKUP_DIR -name "uploads_backup_*.tar.gz" -mtime +7 -delete
```

## Performance Optimization

### 1. Database Indexing

```python
# Add to app/database.py
async def create_indexes():
    """Create database indexes for better performance."""
    # User indexes
    await User.create_index("email")
    await User.create_index("created_at")
    
    # Course indexes
    await Course.create_index("owner_id")
    await Course.create_index("title")
    await Course.create_index("level")
    await Course.create_index("tags")
    
    # Quiz indexes
    await Quiz.create_index("course_id")
    await Quiz.create_index("created_at")
    
    # Chat indexes
    await ChatSession.create_index("user_id")
    await ChatSession.create_index("created_at")
    await ChatMessage.create_index("session_id")
    await ChatMessage.create_index("created_at")
```

### 2. Caching

```python
# Add to requirements.txt
redis==5.0.1

# Add to app/main.py
from redis import Redis
import json

redis_client = Redis(host='localhost', port=6379, db=0)

@app.middleware("http")
async def cache_middleware(request: Request, call_next):
    # Cache GET requests for 5 minutes
    if request.method == "GET" and request.url.path.startswith("/courses/"):
        cache_key = f"cache:{request.url.path}"
        cached_response = redis_client.get(cache_key)
        if cached_response:
            return Response(
                content=cached_response,
                media_type="application/json"
            )
    
    response = await call_next(request)
    
    # Cache successful GET responses
    if request.method == "GET" and response.status_code == 200:
        redis_client.setex(cache_key, 300, response.body)
    
    return response
```

## Security Hardening

### 1. Rate Limiting

```python
# Add to requirements.txt
slowapi==0.1.9

# Add to app/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/auth/login")
@limiter.limit("5/minute")
async def login(request: Request, user_credentials: UserLogin):
    # Login logic
    pass
```

### 2. Input Validation

```python
# Add to app/schemas/course.py
from pydantic import validator

class CourseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    
    @validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check MongoDB connection string
   - Verify network connectivity
   - Check authentication credentials

2. **File Upload Issues**
   - Verify file size limits
   - Check file permissions
   - Ensure upload directory exists

3. **AI Service Errors**
   - Verify Google API key
   - Check API quotas and limits
   - Monitor error logs

4. **Performance Issues**
   - Check database indexes
   - Monitor memory usage
   - Review query performance

### Log Analysis

```bash
# View application logs
sudo journalctl -u ai-learning-app -f

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# View system logs
sudo tail -f /var/log/syslog
```

## Maintenance

### 1. Regular Updates

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Python dependencies
pip install --upgrade -r requirements.txt

# Restart application
sudo systemctl restart ai-learning-app
```

### 2. Database Maintenance

```bash
# Check database status
mongo --eval "db.stats()"

# Repair database
mongod --repair

# Compact database
mongo --eval "db.runCommand({compact: 'collection_name'})"
```

### 3. Log Rotation

```bash
# Configure logrotate
sudo tee /etc/logrotate.d/ai-learning-app > /dev/null <<EOF
/opt/ai-learning-app/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 appuser appuser
    postrotate
        systemctl reload ai-learning-app
    endscript
}
EOF
```

This deployment guide provides comprehensive instructions for deploying the AI Learning Application to various platforms and environments. Choose the deployment method that best fits your needs and infrastructure requirements.
