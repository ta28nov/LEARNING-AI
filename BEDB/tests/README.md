# Testing Guide for AI Learning Platform

## 📋 Overview

This directory contains comprehensive test suites for the AI Learning Platform backend, specifically for the Phase 1 Enrollment System implementation.

## 🧪 Test Structure

```
tests/
├── __init__.py                    # Test package init
├── conftest.py                    # Pytest fixtures and configuration
├── test_enrollment.py             # Enrollment model tests
├── test_student_router.py         # Student endpoint tests
├── test_instructor_router.py      # Instructor endpoint tests
└── README.md                      # This file
```

## 🚀 Running Tests

### Prerequisites

Install test dependencies:
```bash
cd BEDB
pip install pytest pytest-asyncio httpx
```

### Run All Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=html

# Run specific test file
pytest tests/test_enrollment.py -v

# Run specific test class
pytest tests/test_enrollment.py::TestCourseEnrollment -v

# Run specific test function
pytest tests/test_enrollment.py::TestCourseEnrollment::test_create_enrollment -v
```

### Run Tests by Category

```bash
# Run only model tests
pytest tests/test_enrollment.py -v

# Run only router tests
pytest tests/test_student_router.py tests/test_instructor_router.py -v

# Run tests matching pattern
pytest tests/ -k "enrollment" -v
```

## 📝 Test Coverage

### test_enrollment.py - Model Tests

**CourseEnrollment Tests:**
- ✅ `test_create_enrollment` - Create new enrollment
- ✅ `test_unique_enrollment` - Prevent duplicate enrollments
- ✅ `test_enrollment_status_update` - Update enrollment status
- ✅ `test_find_enrollments_by_student` - Query by student
- ✅ `test_find_enrollments_by_course` - Query by course
- ✅ `test_enrollment_progress_range` - Validate progress range
- ✅ `test_delete_enrollment` - Delete enrollment

**ChapterProgress Tests:**
- ✅ `test_create_chapter_progress` - Create progress record
- ✅ `test_update_chapter_progress` - Update progress
- ✅ `test_complete_chapter` - Mark chapter complete
- ✅ `test_find_chapter_progress_by_user` - Query by user
- ✅ `test_chapter_progress_by_course` - Query by course

### test_student_router.py - Student Endpoint Tests

**Enrollment Tests:**
- ✅ `test_enroll_in_public_course` - Successful enrollment
- ✅ `test_cannot_enroll_in_draft_course` - Draft course rejection
- ✅ `test_cannot_enroll_twice` - Duplicate prevention
- ✅ `test_unenroll_from_course` - Unenrollment
- ✅ `test_enrollment_requires_student_role` - Role validation

**Course Listing Tests:**
- ✅ `test_get_enrolled_courses` - Get enrolled courses
- ✅ `test_filter_by_status` - Filter by enrollment status
- ✅ `test_pagination` - Pagination support

**Dashboard Tests:**
- ✅ `test_get_dashboard` - Get student dashboard
- ✅ `test_dashboard_requires_auth` - Authentication check

**Edge Cases:**
- ✅ `test_enroll_nonexistent_course` - 404 handling
- ✅ `test_unenroll_not_enrolled` - Unenroll validation

### test_instructor_router.py - Instructor Endpoint Tests

**Course Management Tests:**
- ✅ `test_get_instructor_courses` - List instructor's courses
- ✅ `test_instructor_only_sees_own_courses` - Ownership validation
- ✅ `test_pagination` - Pagination support

**Student Viewing Tests:**
- ✅ `test_get_course_students` - View enrolled students
- ✅ `test_cannot_view_other_instructor_students` - Authorization

**Analytics Tests:**
- ✅ `test_get_course_analytics` - Get course analytics
- ✅ `test_analytics_only_for_own_courses` - Ownership check

**Dashboard Tests:**
- ✅ `test_get_instructor_dashboard` - Get dashboard
- ✅ `test_dashboard_requires_instructor_role` - Role validation

**All Students Tests:**
- ✅ `test_get_all_students` - View all students

**Edge Cases:**
- ✅ `test_analytics_for_nonexistent_course` - 404 handling
- ✅ `test_admin_can_access_instructor_endpoints` - Admin access

## 🔧 Test Fixtures

Defined in `conftest.py`:

### Database Fixtures
- `test_db` - Test database connection with cleanup
- `event_loop` - Async event loop for tests

### User Fixtures
- `test_student` - Test student user
- `test_instructor` - Test instructor user
- `test_admin` - Test admin user

### Course Fixtures
- `test_course` - Public approved course
- `test_draft_course` - Draft course

### Enrollment Fixtures
- `test_enrollment` - Sample enrollment

### Token Fixtures
- `student_token` - JWT for student
- `instructor_token` - JWT for instructor
- `admin_token` - JWT for admin

## 📊 Test Database

Tests use a separate test database: `ai_learning_platform_test`

**Important:** Test database is cleaned after each test to ensure isolation.

## ✅ Best Practices

1. **Isolation**: Each test is independent and doesn't affect others
2. **Cleanup**: Database is cleaned after each test
3. **Async**: All database operations use async/await
4. **Fixtures**: Reusable test data via pytest fixtures
5. **Assertions**: Clear and specific assertions
6. **Coverage**: Tests cover success, failure, and edge cases

## 🔍 Debugging Tests

### Run with verbose output:
```bash
pytest tests/ -vv
```

### Stop on first failure:
```bash
pytest tests/ -x
```

### Run failed tests from last run:
```bash
pytest tests/ --lf
```

### Print statements in tests:
```bash
pytest tests/ -s
```

### Run with pdb debugger:
```bash
pytest tests/ --pdb
```

## 📈 Coverage Report

Generate HTML coverage report:
```bash
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html  # View in browser
```

Target coverage: **>80%** for all modules

## 🐛 Common Issues

### Issue 1: Test database connection failed
**Solution**: Check MONGODB_URL in environment variables

### Issue 2: Import errors
**Solution**: Ensure you're in BEDB directory and virtual environment is activated

### Issue 3: Async warnings
**Solution**: Use `@pytest.mark.asyncio` decorator for async tests

### Issue 4: Fixture not found
**Solution**: Check conftest.py is in tests/ directory

## 🚦 CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd BEDB
          pip install -r requirements.txt
          pip install pytest pytest-asyncio httpx pytest-cov
      
      - name: Run tests
        run: |
          cd BEDB
          pytest tests/ -v --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v2
        with:
          file: ./BEDB/coverage.xml
```

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [MongoDB Testing Best Practices](https://www.mongodb.com/docs/manual/core/testing/)

## 🎯 Next Steps

1. **Increase Coverage**: Add more edge case tests
2. **Integration Tests**: Test full user flows
3. **Performance Tests**: Add load testing
4. **Frontend Tests**: Create E2E tests with frontend
5. **Mock Tests**: Add tests with mocked AI services

---

**Last Updated**: October 3, 2025
**Maintainer**: AI Learning Platform Team
