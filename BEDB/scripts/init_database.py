#!/usr/bin/env python3
"""
MongoDB Database Initialization Script for AI Learning Platform
Tạo database, collections, indexes và sample data
"""

import asyncio
import os
import sys
from datetime import datetime
from typing import List, Dict, Any
import hashlib

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING, DESCENDING, TEXT
import google.generativeai as genai
from app.config import settings

# MongoDB Atlas connection string template
ATLAS_CONNECTION_TEMPLATE = """
mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority
"""

class DatabaseInitializer:
    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string or settings.mongodb_url
        self.database_name = settings.database_name
        self.client = None
        self.db = None
        
    async def connect(self):
        """Kết nối đến MongoDB"""
        print(f"🔗 Connecting to MongoDB: {self.database_name}")
        self.client = AsyncIOMotorClient(self.connection_string)
        self.db = self.client[self.database_name]
        
        # Test connection
        await self.client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!")
        
    async def create_collections(self):
        """Tạo các collections cần thiết"""
        collections = [
            'users', 'courses', 'uploads', 'quizzes', 'quiz_history',
            'chat_sessions', 'chat_messages', 'dashboard_progress',
            'embeddings', 'chapters', 'system_stats'
        ]
        
        existing_collections = await self.db.list_collection_names()
        
        for collection in collections:
            if collection not in existing_collections:
                await self.db.create_collection(collection)
                print(f"✅ Created collection: {collection}")
            else:
                print(f"ℹ️  Collection exists: {collection}")
                
    async def create_indexes(self):
        """Tạo indexes để tối ưu performance"""
        print("🔍 Creating database indexes...")
        
        # Users indexes
        await self.db.users.create_indexes([
            IndexModel([("email", ASCENDING)], unique=True),
            IndexModel([("role", ASCENDING)]),
            IndexModel([("created_at", DESCENDING)]),
            IndexModel([("is_active", ASCENDING)])
        ])
        
        # Courses indexes
        await self.db.courses.create_indexes([
            IndexModel([("owner_id", ASCENDING)]),
            IndexModel([("title", TEXT), ("description", TEXT)]),
            IndexModel([("level", ASCENDING)]),
            IndexModel([("tags", ASCENDING)]),
            IndexModel([("is_public", ASCENDING)]),
            IndexModel([("source", ASCENDING)]),
            IndexModel([("created_at", DESCENDING)])
        ])
        
        # Uploads indexes
        await self.db.uploads.create_indexes([
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("status", ASCENDING)]),
            IndexModel([("file_type", ASCENDING)]),
            IndexModel([("created_at", DESCENDING)])
        ])
        
        # Quiz indexes
        await self.db.quizzes.create_indexes([
            IndexModel([("course_id", ASCENDING)]),
            IndexModel([("upload_id", ASCENDING)]),
            IndexModel([("created_by", ASCENDING)]),
            IndexModel([("created_at", DESCENDING)])
        ])
        
        # Quiz history indexes
        await self.db.quiz_history.create_indexes([
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("quiz_id", ASCENDING)]),
            IndexModel([("score", DESCENDING)]),
            IndexModel([("completed_at", DESCENDING)])
        ])
        
        # Chat sessions indexes
        await self.db.chat_sessions.create_indexes([
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("course_id", ASCENDING)]),
            IndexModel([("upload_id", ASCENDING)]),
            IndexModel([("status", ASCENDING)]),
            IndexModel([("created_at", DESCENDING)])
        ])
        
        # Chat messages indexes
        await self.db.chat_messages.create_indexes([
            IndexModel([("session_id", ASCENDING)]),
            IndexModel([("sender", ASCENDING)]),
            IndexModel([("created_at", ASCENDING)])
        ])
        
        # Dashboard progress indexes
        await self.db.dashboard_progress.create_indexes([
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("course_id", ASCENDING)]),
            IndexModel([("user_id", ASCENDING), ("course_id", ASCENDING)], unique=True),
            IndexModel([("last_accessed", DESCENDING)])
        ])
        
        # Embeddings indexes (for vector search)
        await self.db.embeddings.create_indexes([
            IndexModel([("source_id", ASCENDING)]),
            IndexModel([("source_type", ASCENDING)]),
            IndexModel([("chunk_index", ASCENDING)]),
            IndexModel([("source_id", ASCENDING), ("chunk_index", ASCENDING)]),
            IndexModel([("created_at", DESCENDING)])
        ])
        
        print("✅ All indexes created successfully!")
        
    async def create_vector_search_index(self):
        """Tạo vector search index cho MongoDB Atlas"""
        print("🔍 Creating vector search index...")
        
        try:
            # Vector search index definition
            vector_index = {
                "name": "vector_index",
                "definition": {
                    "fields": [
                        {
                            "type": "vector",
                            "path": "embedding",
                            "numDimensions": 768,  # Google GenAI embedding dimension
                            "similarity": "cosine"
                        },
                        {
                            "type": "filter",
                            "path": "source_type"
                        },
                        {
                            "type": "filter", 
                            "path": "source_id"
                        }
                    ]
                }
            }
            
            # Note: Vector search indexes need to be created via Atlas UI or Atlas CLI
            # This is a placeholder for the index structure
            print("ℹ️  Vector search index structure defined")
            print("⚠️  Please create vector search index manually in MongoDB Atlas:")
            print(f"   Collection: {self.database_name}.embeddings")
            print("   Index name: vector_index")
            print("   Vector field: embedding")
            print("   Dimensions: 768")
            print("   Similarity: cosine")
            
        except Exception as e:
            print(f"⚠️  Vector search index creation: {e}")
            
    async def create_sample_admin_user(self):
        """Tạo admin user mẫu"""
        print("👤 Creating sample admin user...")
        
        admin_email = "admin@ailearning.com"
        admin_password = "admin123456"
        
        # Check if admin exists
        existing_admin = await self.db.users.find_one({"email": admin_email})
        if existing_admin:
            print("ℹ️  Admin user already exists")
            return
            
        # Hash password
        password_hash = hashlib.sha256(admin_password.encode()).hexdigest()
        
        admin_user = {
            "email": admin_email,
            "password_hash": password_hash,
            "name": "System Administrator",
            "role": "admin",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await self.db.users.insert_one(admin_user)
        print(f"✅ Admin user created: {admin_email} / {admin_password}")
        print(f"   User ID: {result.inserted_id}")
        
    async def create_sample_courses(self):
        """Tạo sample courses cho demo"""
        print("📚 Creating sample courses...")
        
        sample_courses = [
            {
                "title": "Introduction to Machine Learning",
                "description": "Learn the fundamentals of machine learning with practical examples and hands-on exercises.",
                "outline": """
                Chapter 1: What is Machine Learning?
                Chapter 2: Types of Machine Learning
                Chapter 3: Supervised Learning
                Chapter 4: Unsupervised Learning  
                Chapter 5: Model Evaluation
                """,
                "level": "beginner",
                "tags": ["machine-learning", "ai", "python", "data-science"],
                "source": "system",
                "is_public": True,
                "created_at": datetime.utcnow()
            },
            {
                "title": "Web Development with React",
                "description": "Build modern web applications with React, TypeScript, and modern tools.",
                "outline": """
                Chapter 1: React Fundamentals
                Chapter 2: Components and Props
                Chapter 3: State Management
                Chapter 4: Hooks and Context
                Chapter 5: Building Real Applications
                """,
                "level": "intermediate",
                "tags": ["react", "javascript", "web-development", "frontend"],
                "source": "system", 
                "is_public": True,
                "created_at": datetime.utcnow()
            },
            {
                "title": "Python Programming Basics",
                "description": "Master Python programming from basics to advanced concepts.",
                "outline": """
                Chapter 1: Python Syntax and Variables
                Chapter 2: Control Structures
                Chapter 3: Functions and Modules
                Chapter 4: Object-Oriented Programming
                Chapter 5: File Handling and APIs
                """,
                "level": "beginner",
                "tags": ["python", "programming", "basics", "coding"],
                "source": "system",
                "is_public": True,
                "created_at": datetime.utcnow()
            }
        ]
        
        for course in sample_courses:
            existing = await self.db.courses.find_one({"title": course["title"]})
            if not existing:
                result = await self.db.courses.insert_one(course)
                print(f"✅ Created course: {course['title']}")
            else:
                print(f"ℹ️  Course exists: {course['title']}")
                
    async def create_sample_quizzes(self):
        """Tạo sample quizzes"""
        print("🧠 Creating sample quizzes...")
        
        # Get a sample course
        course = await self.db.courses.find_one({"title": "Python Programming Basics"})
        if not course:
            print("⚠️  No course found for quiz creation")
            return
            
        sample_quiz = {
            "title": "Python Basics Quiz",
            "course_id": course["_id"],
            "questions": [
                {
                    "question": "What is the correct way to create a list in Python?",
                    "options": [
                        "list = []",
                        "list = {}",
                        "list = ()",
                        "list = <>"
                    ],
                    "correct_answer": 0,
                    "explanation": "Square brackets [] are used to create lists in Python."
                },
                {
                    "question": "Which keyword is used to define a function in Python?",
                    "options": [
                        "function",
                        "def",
                        "func",
                        "define"
                    ],
                    "correct_answer": 1,
                    "explanation": "The 'def' keyword is used to define functions in Python."
                }
            ],
            "created_at": datetime.utcnow()
        }
        
        existing = await self.db.quizzes.find_one({"title": sample_quiz["title"]})
        if not existing:
            result = await self.db.quizzes.insert_one(sample_quiz)
            print(f"✅ Created quiz: {sample_quiz['title']}")
        else:
            print(f"ℹ️  Quiz exists: {sample_quiz['title']}")
            
    async def setup_embedding_system(self):
        """Setup embedding system cho vector search"""
        print("🔮 Setting up embedding system...")
        
        # Sample embedding document structure
        sample_embedding = {
            "source_id": "sample_course_id",
            "source_type": "course",
            "chunk_index": 0,
            "text": "This is a sample text chunk for embedding",
            "embedding": [0.1] * 768,  # Placeholder embedding vector
            "metadata": {
                "title": "Sample Course",
                "chapter": "Introduction",
                "word_count": 10
            },
            "created_at": datetime.utcnow()
        }
        
        # Insert sample if not exists
        existing = await self.db.embeddings.find_one({"source_id": "sample_course_id"})
        if not existing:
            await self.db.embeddings.insert_one(sample_embedding)
            print("✅ Sample embedding document created")
        else:
            print("ℹ️  Sample embedding already exists")
            
        print("📋 Embedding system structure:")
        print("   - Text chunking: 1000 characters with 200 overlap")
        print("   - Vector dimensions: 768 (Google GenAI)")
        print("   - Similarity: Cosine similarity")
        print("   - Metadata: Source info, chapter, word count")
        
    async def create_system_stats(self):
        """Tạo system statistics collection"""
        print("📊 Setting up system statistics...")
        
        stats_doc = {
            "total_users": 0,
            "total_courses": 0,
            "total_uploads": 0,
            "total_quizzes": 0,
            "total_chat_sessions": 0,
            "total_embeddings": 0,
            "last_updated": datetime.utcnow()
        }
        
        existing = await self.db.system_stats.find_one({})
        if not existing:
            await self.db.system_stats.insert_one(stats_doc)
            print("✅ System stats document created")
        else:
            print("ℹ️  System stats already exists")
            
    async def run_health_check(self):
        """Kiểm tra sức khỏe database"""
        print("🏥 Running database health check...")
        
        # Check collections
        collections = await self.db.list_collection_names()
        print(f"📁 Collections: {len(collections)}")
        
        # Check indexes
        for collection_name in ['users', 'courses', 'embeddings']:
            if collection_name in collections:
                indexes = await self.db[collection_name].list_indexes().to_list(None)
                print(f"🔍 {collection_name} indexes: {len(indexes)}")
                
        # Check sample data
        user_count = await self.db.users.count_documents({})
        course_count = await self.db.courses.count_documents({})
        print(f"👥 Users: {user_count}")
        print(f"📚 Courses: {course_count}")
        
        print("✅ Database health check completed!")
        
    async def close(self):
        """Đóng kết nối database"""
        if self.client:
            self.client.close()
            print("🔒 Database connection closed")

async def main():
    """Main function để chạy database initialization"""
    print("🚀 AI Learning Platform Database Initialization")
    print("=" * 50)
    
    # Kiểm tra connection string
    connection_string = os.getenv('MONGODB_URL') or settings.mongodb_url
    
    if 'localhost' in connection_string:
        print("⚠️  Using local MongoDB. For production, use MongoDB Atlas:")
        print(ATLAS_CONNECTION_TEMPLATE)
        print()
    
    db_init = DatabaseInitializer(connection_string)
    
    try:
        # Initialize database
        await db_init.connect()
        await db_init.create_collections()
        await db_init.create_indexes()
        await db_init.create_vector_search_index()
        
        # Create sample data
        await db_init.create_sample_admin_user()
        await db_init.create_sample_courses()
        await db_init.create_sample_quizzes()
        await db_init.setup_embedding_system()
        await db_init.create_system_stats()
        
        # Health check
        await db_init.run_health_check()
        
        print("\n🎉 Database initialization completed successfully!")
        print("\n📋 Next steps:")
        print("1. Create vector search index in MongoDB Atlas UI")
        print("2. Set up Google GenAI API key")
        print("3. Configure environment variables")
        print("4. Start the FastAPI backend")
        print("\n🔐 Default admin credentials:")
        print("   Email: admin@ailearning.com")
        print("   Password: admin123456")
        
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        raise
    finally:
        await db_init.close()

if __name__ == "__main__":
    asyncio.run(main())
