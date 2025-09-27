# Local Development Setup Guide

## 🚀 Quick Start for Local Development

### 1. Setup MongoDB
- Ensure MongoDB is installed and running locally
- Default MongoDB URL: `mongodb://localhost:27017`
- Database will be created automatically by init scripts

### 2. Environment Setup

1. **Create and configure .env file**
```bash
# Copy example env file
cp env.example .env

# Edit .env with your configuration:
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_learning_app
SECRET_KEY=your-secret-key-here
GOOGLE_API_KEY=AIzaSyDSYWID4MeLXyhYezqVqbR2kNKXx5RmoFw
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:3001"]
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

### 3. Initialize Database

Run the database initialization script:
```bash
python scripts/init_database.py
```

This will:
- Create all necessary collections
- Set up required indexes
- Create sample admin user (admin@ailearning.com / admin123456)
- Add sample courses and quizzes
- Setup vector search structure

### 4. Start the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access the API

- Interactive API docs: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## 🔍 Default Credentials

```
Email: admin@ailearning.com
Password: admin123456
```

## 📋 Development Notes

1. **Database Scripts**
   - `scripts/init_database.py`: Initialize database with sample data
   - `scripts/vector_chunking.py`: Setup vector search
   - `scripts/optimize_database.py`: Performance optimization

2. **Testing the API**
   - Use Swagger UI at `/docs` for interactive testing
   - Default CORS allows localhost:3000 and localhost:3001
   - JWT authentication required for most endpoints

3. **File Upload Directory**
   - Ensure `uploads` directory exists
   - Default max file size: 10MB
   - Supported formats: PDF, DOCX, TXT

4. **AI Features**
   - Requires valid Google API key
   - Test AI features using the chat endpoints first
   - Vector search requires proper setup in MongoDB

5. **Development Best Practices**
   - Use `--reload` flag for auto-reload during development
   - Check logs for debugging
   - Run tests before making changes
   - Follow existing code style