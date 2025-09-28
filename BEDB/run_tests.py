#!/usr/bin/env python3
"""
Comprehensive test runner for the AI Learning Application.
This script runs all tests to verify the backend setup.
"""

import asyncio
import subprocess
import sys
import os
import time

def run_command(command, description):
    """Run a command and return success status."""
    print(f"\n🔍 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(f"📄 Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stderr:
                print(f"💥 Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"💥 {description} error: {e}")
        return False

async def run_async_test(test_function, description):
    """Run an async test function."""
    print(f"\n🔍 {description}...")
    try:
        result = await test_function()
        if result:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed")
            return False
    except Exception as e:
        print(f"💥 {description} error: {e}")
        return False

async def test_database_setup():
    """Test database setup."""
    try:
        # Import and run the database test
        from test_setup import test_database_connection
        return await test_database_connection()
    except Exception as e:
        print(f"Database test error: {e}")
        return False

async def test_api_endpoints():
    """Test API endpoints (requires server to be running)."""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/health", timeout=5) as response:
                if response.status == 200:
                    print("✅ API server is running")
                    # Run the full API test
                    from test_api import test_api_endpoints
                    return await test_api_endpoints()
                else:
                    print("❌ API server is not responding correctly")
                    return False
    except Exception as e:
        print(f"⚠️  API server is not running: {e}")
        print("💡 Start the server with: python -m uvicorn app.main:app --reload")
        return False

def main():
    """Main test runner."""
    print("🚀 Starting comprehensive backend tests...")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Database setup
    total_tests += 1
    if asyncio.run(test_database_setup()):
        tests_passed += 1
    
    # Test 2: Python syntax check
    total_tests += 1
    if run_command("python -m py_compile app/main.py", "Python syntax check"):
        tests_passed += 1
    
    # Test 3: Import check
    total_tests += 1
    if run_command("python -c 'import app.main; print(\"Import successful\")'", "Module import check"):
        tests_passed += 1
    
    # Test 4: API endpoints (if server is running)
    total_tests += 1
    if asyncio.run(test_api_endpoints()):
        tests_passed += 1
    
    # Results
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Backend is ready for use.")
        print("\n🚀 Next steps:")
        print("1. Start the server: python -m uvicorn app.main:app --reload")
        print("2. Open API docs: http://localhost:8000/docs")
        print("3. Start the frontend: cd ../learning-app-fe && npm run dev")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Common solutions:")
        print("1. Make sure MongoDB is running")
        print("2. Check Python dependencies: pip install -r requirements.txt")
        print("3. Verify .env file configuration")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)
