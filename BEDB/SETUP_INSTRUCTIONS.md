# Backend Setup Instructions

## Prerequisites

1. **Python 3.11+** - Make sure Python is installed and accessible
2. **MongoDB** - Install and run MongoDB locally
3. **pip** - Python package installer

## Installation Steps

### 1. Install Python Dependencies

```bash
# Navigate to the BEDB directory
cd BEDB

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup MongoDB

Make sure MongoDB is running on your local machine:

```bash
# Start MongoDB service (Windows)
net start MongoDB

# Or if using MongoDB Community Server
mongod

# Verify MongoDB is running
mongosh
```

### 3. Configure Environment Variables

Create a `.env` file in the BEDB directory:

```env
# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_learning_app

# JWT
SECRET_KEY=your-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google GenAI (Optional)
GOOGLE_API_KEY=your-google-api-key-here

# Application
DEBUG=true
HOST=0.0.0.0
PORT=8000

# File Upload
MAX_FILE_SIZE=10485760
UPLOAD_DIR=uploads

# CORS
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:3001"]
```

### 4. Test the Setup

Run the comprehensive test script to verify everything is working:

```bash
# Run all tests (recommended)
python run_tests.py

# Or run individual tests
python test_setup.py          # Database and models test
python test_api.py           # API endpoints test (requires server running)
```

If the tests pass, you should see:
```
✅ Backend setup verification completed successfully!
🚀 You can now start the server with: python -m uvicorn app.main:app --reload
```

### 5. Start the Development Server

```bash
python -m uvicorn app.main:app --reload
```

The server will be available at:
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

The API includes the following main endpoints:

- **Authentication**: `/api/v1/auth/*`
- **Users**: `/api/v1/users/*`
- **Courses**: `/api/v1/courses/*`
- **Uploads**: `/api/v1/uploads/*`
- **Quizzes**: `/api/v1/quiz/*`
- **Chat**: `/api/v1/chat/*`
- **Dashboard**: `/api/v1/dashboard/*`
- **Search**: `/api/v1/search/*`
- **Admin**: `/api/v1/admin/*`
- **Leaderboard**: `/api/v1/leaderboard/*`

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Make sure MongoDB is running
   - Check the MONGODB_URL in your .env file
   - Verify MongoDB is accessible on port 27017

2. **Import Errors**
   - Make sure you're in the BEDB directory
   - Check that all dependencies are installed
   - Verify Python path is correct

3. **Port Already in Use**
   - Change the PORT in your .env file
   - Or stop the process using port 8000

4. **ObjectId/String Conversion Errors**
   - The API now properly handles ObjectId to string conversion
   - All schemas include proper JSON encoders for ObjectId
   - Use the utility functions in `app/utils.py` for safe conversions

5. **API Data Validation Errors**
   - Check that all required fields are provided
   - Verify data types match the schema definitions
   - Use the test scripts to verify API endpoints

### Getting Help

If you encounter issues:

1. Check the error messages in the console
2. Verify all prerequisites are installed
3. Make sure MongoDB is running
4. Check the `.env` file configuration
5. Run the test script to identify specific issues

## Production Deployment

For production deployment:

1. Set `DEBUG=false` in your .env file
2. Use a strong `SECRET_KEY`
3. Configure proper CORS origins
4. Use a production MongoDB instance
5. Set up proper logging and monitoring
