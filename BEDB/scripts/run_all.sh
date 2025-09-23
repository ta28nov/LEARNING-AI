#!/bin/bash
# Complete Database Setup Script for AI Learning Platform

set -e

echo "🚀 AI Learning Platform - Complete Database Setup"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}🐍 Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Install requirements
echo -e "${BLUE}📥 Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Check MongoDB connection
echo -e "${BLUE}🔗 Checking MongoDB connection...${NC}"
if [ -z "$MONGODB_URL" ]; then
    echo -e "${YELLOW}⚠️  MONGODB_URL not set. Using default local MongoDB${NC}"
    export MONGODB_URL="mongodb://localhost:27017"
fi

echo "MongoDB URL: $MONGODB_URL"

# Check Google GenAI API key
if [ -z "$GOOGLE_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  GOOGLE_API_KEY not set. Vector embeddings will use dummy data${NC}"
else
    echo -e "${GREEN}✅ Google GenAI API key configured${NC}"
fi

# Run database initialization
echo -e "${BLUE}🏗️  Initializing database...${NC}"
python3 scripts/init_database.py

# Check if initialization was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Database initialization completed successfully!${NC}"
else
    echo -e "${RED}❌ Database initialization failed!${NC}"
    exit 1
fi

# Ask user if they want to run vector processing
echo ""
read -p "🔮 Do you want to process vectors for existing content? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}🔮 Running vector processing...${NC}"
    python3 scripts/vector_chunking.py
fi

# Show connection info
echo ""
echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
echo ""
echo -e "${BLUE}📋 Connection Information:${NC}"
echo "Database: $MONGODB_URL"
echo "Database Name: ai_learning_platform"
echo ""
echo -e "${BLUE}🔐 Default Admin Credentials:${NC}"
echo "Email: admin@ailearning.com"
echo "Password: admin123456"
echo ""
echo -e "${BLUE}🚀 Next Steps:${NC}"
echo "1. Start your FastAPI backend: uvicorn app.main:app --reload"
echo "2. Start your React frontend: npm run dev"
echo "3. Visit: http://localhost:3000"
echo ""
echo -e "${YELLOW}⚠️  Important Notes:${NC}"
echo "- Change admin password after first login"
echo "- Configure Google GenAI API key for full functionality"
echo "- Create vector search index in MongoDB Atlas for production"
echo ""
echo -e "${GREEN}Happy Learning! 🎓✨${NC}"
