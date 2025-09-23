#!/usr/bin/env python3
"""
MongoDB Atlas Setup Script for AI Learning Platform
Hướng dẫn setup MongoDB Atlas với Vector Search
"""

import os
import json
from typing import Dict, Any

# Atlas cluster configuration template
ATLAS_CONFIG = {
    "cluster_name": "ai-learning-cluster",
    "provider": "AWS",
    "region": "US_EAST_1",
    "instance_size": "M10",  # Minimum for Vector Search
    "mongodb_version": "7.0",
    "backup_enabled": True,
    "vector_search_enabled": True
}

# Database configuration
DATABASE_CONFIG = {
    "database_name": "ai_learning_platform",
    "collections": [
        "users", "courses", "uploads", "quizzes", "quiz_history",
        "chat_sessions", "chat_messages", "dashboard_progress", 
        "embeddings", "chapters", "system_stats"
    ]
}

# Vector Search Index configuration
VECTOR_INDEX_CONFIG = {
    "name": "vector_index",
    "database": "ai_learning_platform",
    "collection": "embeddings",
    "definition": {
        "fields": [
            {
                "type": "vector",
                "path": "embedding",
                "numDimensions": 768,
                "similarity": "cosine"
            },
            {
                "type": "filter",
                "path": "source_type"
            },
            {
                "type": "filter",
                "path": "source_id"
            },
            {
                "type": "filter",
                "path": "metadata.course_id"
            },
            {
                "type": "filter",
                "path": "metadata.user_id"
            }
        ]
    }
}

def generate_atlas_cli_commands():
    """Generate Atlas CLI commands for setup"""
    
    print("🚀 MongoDB Atlas Setup Commands")
    print("=" * 50)
    
    print("\n📋 Prerequisites:")
    print("1. Install Atlas CLI: https://www.mongodb.com/docs/atlas/cli/")
    print("2. Login to Atlas: atlas auth login")
    print("3. Create/Select project: atlas projects create 'AI Learning Platform'")
    
    print("\n🏗️  1. Create Cluster:")
    print(f"""
atlas clusters create {ATLAS_CONFIG['cluster_name']} \\
    --provider {ATLAS_CONFIG['provider']} \\
    --region {ATLAS_CONFIG['region']} \\
    --tier {ATLAS_CONFIG['instance_size']} \\
    --mdbVersion {ATLAS_CONFIG['mongodb_version']} \\
    --diskSizeGB 10 \\
    --backup
""")

    print("\n🔐 2. Create Database User:")
    print("""
atlas dbusers create \\
    --username ai_learning_user \\
    --password <STRONG_PASSWORD> \\
    --role readWriteAnyDatabase
""")

    print("\n🌐 3. Configure Network Access:")
    print("""
# Allow access from your IP
atlas accessLists create --type ipAddress --value <YOUR_IP>/32

# For development (NOT recommended for production)
atlas accessLists create --type ipAddress --value 0.0.0.0/0
""")

    print("\n📊 4. Get Connection String:")
    print(f"""
atlas clusters connectionStrings describe {ATLAS_CONFIG['cluster_name']}
""")

def generate_vector_index_commands():
    """Generate commands to create vector search index"""
    
    print("\n🔍 Vector Search Index Setup")
    print("=" * 40)
    
    print("\n📝 Create vector search index file (vector_index.json):")
    with open('vector_index.json', 'w') as f:
        json.dump(VECTOR_INDEX_CONFIG, f, indent=2)
    
    print("✅ Created vector_index.json")
    
    print("\n🔧 Create Vector Search Index:")
    print(f"""
atlas clusters search indexes create \\
    --clusterName {ATLAS_CONFIG['cluster_name']} \\
    --file vector_index.json
""")

    print("\n📋 Alternative: Manual Setup via Atlas UI")
    print("1. Go to Atlas Dashboard > Database > Search")
    print("2. Click 'Create Search Index'")
    print("3. Choose 'Vector Search'")
    print("4. Select database: ai_learning_platform")
    print("5. Select collection: embeddings")
    print("6. Use this configuration:")
    print(json.dumps(VECTOR_INDEX_CONFIG["definition"], indent=2))

def generate_environment_config():
    """Generate environment configuration"""
    
    print("\n⚙️  Environment Configuration")
    print("=" * 40)
    
    env_template = """
# MongoDB Atlas Configuration
MONGODB_URL=mongodb+srv://ai_learning_user:<PASSWORD>@ai-learning-cluster.xxxxx.mongodb.net/ai_learning_platform?retryWrites=true&w=majority
DATABASE_NAME=ai_learning_platform

# Google GenAI Configuration
GOOGLE_API_KEY=your_google_genai_api_key_here

# JWT Configuration
SECRET_KEY=your_super_secret_jwt_key_here_at_least_32_characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=False
HOST=0.0.0.0
PORT=8000

# File Upload Configuration
MAX_FILE_SIZE=10485760
UPLOAD_DIR=uploads

# CORS Configuration
ALLOWED_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]

# Email Configuration (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Redis Configuration (Optional - for caching)
REDIS_URL=redis://localhost:6379/0
"""

    with open('.env.production', 'w') as f:
        f.write(env_template.strip())
    
    print("✅ Created .env.production template")
    print("\n📋 Don't forget to:")
    print("1. Replace <PASSWORD> with your database user password")
    print("2. Replace xxxxx with your actual cluster identifier")
    print("3. Set your Google GenAI API key")
    print("4. Generate a strong JWT secret key")
    print("5. Update ALLOWED_ORIGINS with your frontend domains")

def generate_docker_config():
    """Generate Docker configuration for production"""
    
    print("\n🐳 Docker Production Configuration")
    print("=" * 40)
    
    # Production Dockerfile
    dockerfile_prod = """
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app ./app
COPY ./scripts ./scripts

# Create uploads directory
RUN mkdir -p uploads && chmod 755 uploads

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && \\
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run with Gunicorn for production
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
"""

    with open('Dockerfile.prod', 'w') as f:
        f.write(dockerfile_prod.strip())
    
    # Production docker-compose
    docker_compose_prod = """
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.prod
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=${MONGODB_URL}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=False
    volumes:
      - ./uploads:/app/uploads
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.prod.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: unless-stopped

volumes:
  uploads:
"""

    with open('docker-compose.prod.yml', 'w') as f:
        f.write(docker_compose_prod.strip())
    
    # Production nginx config
    nginx_prod = """
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
        
        # Redirect to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com www.yourdomain.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

        # API proxy
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /health {
            proxy_pass http://api;
        }

        # File uploads
        location /uploads/ {
            client_max_body_size 10M;
            proxy_pass http://api;
            proxy_request_buffering off;
        }
    }
}
"""

    with open('nginx.prod.conf', 'w') as f:
        f.write(nginx_prod.strip())
    
    print("✅ Created production Docker files:")
    print("   - Dockerfile.prod")
    print("   - docker-compose.prod.yml") 
    print("   - nginx.prod.conf")

def generate_deployment_script():
    """Generate deployment script"""
    
    print("\n🚀 Deployment Script")
    print("=" * 40)
    
    deploy_script = """#!/bin/bash
# AI Learning Platform Deployment Script

set -e

echo "🚀 Deploying AI Learning Platform..."

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ .env.production file not found!"
    echo "Please create it using the template"
    exit 1
fi

# Load environment variables
export $(cat .env.production | xargs)

# Build and deploy
echo "🏗️  Building Docker images..."
docker-compose -f docker-compose.prod.yml build

echo "🔄 Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down

echo "🚀 Starting new containers..."
docker-compose -f docker-compose.prod.yml up -d

echo "⏳ Waiting for services to start..."
sleep 30

echo "🏥 Running health check..."
if curl -f http://localhost:8000/health; then
    echo "✅ Deployment successful!"
    echo "🌐 API is running at http://localhost:8000"
    echo "📚 API docs at http://localhost:8000/docs"
else
    echo "❌ Health check failed!"
    echo "🔍 Checking logs..."
    docker-compose -f docker-compose.prod.yml logs api
    exit 1
fi

echo "🎉 Deployment completed successfully!"
"""

    with open('deploy.sh', 'w') as f:
        f.write(deploy_script.strip())
    
    # Make executable
    os.chmod('deploy.sh', 0o755)
    
    print("✅ Created deploy.sh script")

def main():
    """Main function"""
    print("🏗️  MongoDB Atlas Setup Generator for AI Learning Platform")
    print("=" * 60)
    
    # Generate all configuration files
    generate_atlas_cli_commands()
    generate_vector_index_commands()
    generate_environment_config()
    generate_docker_config()
    generate_deployment_script()
    
    print("\n🎉 Setup files generated successfully!")
    print("\n📋 Next Steps:")
    print("1. Follow the Atlas CLI commands to create your cluster")
    print("2. Create the vector search index")
    print("3. Configure your .env.production file")
    print("4. Run: python scripts/init_database.py")
    print("5. Run: python scripts/vector_chunking.py")
    print("6. Deploy with: ./deploy.sh")
    
    print("\n⚠️  Important Notes:")
    print("- Vector Search requires M10+ cluster (minimum $57/month)")
    print("- Make sure to whitelist your IP addresses")
    print("- Use strong passwords and keep credentials secure")
    print("- Test everything in development first")
    
    print("\n📞 Support:")
    print("- MongoDB Atlas Docs: https://docs.atlas.mongodb.com/")
    print("- Vector Search Guide: https://docs.atlas.mongodb.com/atlas-vector-search/")

if __name__ == "__main__":
    main()
