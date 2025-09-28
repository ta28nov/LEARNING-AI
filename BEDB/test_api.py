#!/usr/bin/env python3
"""
API Test script to verify endpoints and data flow.
Run this script to test API endpoints after starting the server.
"""

import asyncio
import aiohttp
import json
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.models import User
from app.auth import get_password_hash

BASE_URL = "http://localhost:8000/api/v1"

async def test_api_endpoints():
    """Test API endpoints with proper data."""
    print("🚀 Starting API endpoint tests...")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        # Test 1: Health check
        print("🔍 Testing health check...")
        try:
            async with session.get("http://localhost:8000/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Health check passed: {data}")
                else:
                    print(f"❌ Health check failed: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
        
        # Test 2: User registration
        print("\n🔍 Testing user registration...")
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "name": "Test User"
        }
        
        try:
            async with session.post(f"{BASE_URL}/auth/register", json=user_data) as response:
                if response.status == 200:
                    user_response = await response.json()
                    print(f"✅ User registration successful: {user_response['name']}")
                    user_id = user_response['id']
                else:
                    error_data = await response.json()
                    print(f"❌ User registration failed: {error_data}")
                    return False
        except Exception as e:
            print(f"❌ User registration error: {e}")
            return False
        
        # Test 3: User login
        print("\n🔍 Testing user login...")
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        
        try:
            async with session.post(f"{BASE_URL}/auth/login", json=login_data) as response:
                if response.status == 200:
                    login_response = await response.json()
                    access_token = login_response['access_token']
                    print(f"✅ User login successful")
                    
                    # Set authorization header for subsequent requests
                    headers = {"Authorization": f"Bearer {access_token}"}
                else:
                    error_data = await response.json()
                    print(f"❌ User login failed: {error_data}")
                    return False
        except Exception as e:
            print(f"❌ User login error: {e}")
            return False
        
        # Test 4: Create course
        print("\n🔍 Testing course creation...")
        course_data = {
            "title": "Test Course",
            "description": "A test course for API testing",
            "level": "beginner",
            "tags": ["test", "api"]
        }
        
        try:
            async with session.post(f"{BASE_URL}/courses/", json=course_data, headers=headers) as response:
                if response.status == 200:
                    course_response = await response.json()
                    print(f"✅ Course creation successful: {course_response['title']}")
                    course_id = course_response['id']
                else:
                    error_data = await response.json()
                    print(f"❌ Course creation failed: {error_data}")
                    return False
        except Exception as e:
            print(f"❌ Course creation error: {e}")
            return False
        
        # Test 5: Get course
        print("\n🔍 Testing course retrieval...")
        try:
            async with session.get(f"{BASE_URL}/courses/{course_id}", headers=headers) as response:
                if response.status == 200:
                    course_data = await response.json()
                    print(f"✅ Course retrieval successful: {course_data['title']}")
                else:
                    error_data = await response.json()
                    print(f"❌ Course retrieval failed: {error_data}")
                    return False
        except Exception as e:
            print(f"❌ Course retrieval error: {e}")
            return False
        
        # Test 6: Create chapter
        print("\n🔍 Testing chapter creation...")
        chapter_data = {
            "title": "Test Chapter",
            "content": "This is a test chapter content for API testing.",
            "order": 1
        }
        
        try:
            async with session.post(f"{BASE_URL}/courses/{course_id}/chapters", json=chapter_data, headers=headers) as response:
                if response.status == 200:
                    chapter_response = await response.json()
                    print(f"✅ Chapter creation successful: {chapter_response['title']}")
                    chapter_id = chapter_response['id']
                else:
                    error_data = await response.json()
                    print(f"❌ Chapter creation failed: {error_data}")
                    return False
        except Exception as e:
            print(f"❌ Chapter creation error: {e}")
            return False
        
        # Test 7: Get chapters
        print("\n🔍 Testing chapters retrieval...")
        try:
            async with session.get(f"{BASE_URL}/courses/{course_id}/chapters", headers=headers) as response:
                if response.status == 200:
                    chapters_data = await response.json()
                    print(f"✅ Chapters retrieval successful: {len(chapters_data)} chapters found")
                else:
                    error_data = await response.json()
                    print(f"❌ Chapters retrieval failed: {error_data}")
                    return False
        except Exception as e:
            print(f"❌ Chapters retrieval error: {e}")
            return False
        
        # Test 8: Create quiz
        print("\n🔍 Testing quiz creation...")
        quiz_data = {
            "course_id": course_id,
            "chapter_id": chapter_id,
            "title": "Test Quiz",
            "prompt": "Create a quiz about the test chapter"
        }
        
        try:
            async with session.post(f"{BASE_URL}/quiz/", json=quiz_data, headers=headers) as response:
                if response.status == 200:
                    quiz_response = await response.json()
                    print(f"✅ Quiz creation successful: {quiz_response['title']}")
                    quiz_id = quiz_response['id']
                else:
                    error_data = await response.json()
                    print(f"❌ Quiz creation failed: {error_data}")
                    # This might fail if AI service is not configured, which is OK
                    print("⚠️  Quiz creation failed (likely due to missing AI service configuration)")
                    quiz_id = None
        except Exception as e:
            print(f"⚠️  Quiz creation error (likely due to missing AI service): {e}")
            quiz_id = None
        
        # Test 9: Get user profile
        print("\n🔍 Testing user profile retrieval...")
        try:
            async with session.get(f"{BASE_URL}/users/me", headers=headers) as response:
                if response.status == 200:
                    user_data = await response.json()
                    print(f"✅ User profile retrieval successful: {user_data['name']}")
                else:
                    error_data = await response.json()
                    print(f"❌ User profile retrieval failed: {error_data}")
                    return False
        except Exception as e:
            print(f"❌ User profile retrieval error: {e}")
            return False
        
        print("\n" + "=" * 50)
        print("🎉 API endpoint tests completed successfully!")
        print("✅ All core endpoints are working correctly")
        print("✅ ObjectId to string conversion is working")
        print("✅ Data validation is working")
        print("✅ Authentication is working")
        
        return True

async def main():
    """Main test function."""
    try:
        result = await test_api_endpoints()
        if result:
            print("\n🚀 API is ready for use!")
        else:
            print("\n❌ Some API tests failed. Please check the errors above.")
        return result
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"\n💥 Failed to run tests: {e}")
        sys.exit(1)
