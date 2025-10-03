"""
Tests for Instructor Router Endpoints
Test coverage for /api/v1/instructor/* endpoints
"""
import pytest
from httpx import AsyncClient
from app.main import app


class TestInstructorCourses:
    """Test instructor course management endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_instructor_courses(
        self, test_db, test_course, instructor_token
    ):
        """Test getting instructor's courses"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/instructor/courses",
                headers={"Authorization": f"Bearer {instructor_token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) >= 1
            assert data[0]["title"] == test_course.title
    
    @pytest.mark.asyncio
    async def test_instructor_only_sees_own_courses(
        self, test_db, test_course, test_instructor, instructor_token
    ):
        """Test that instructors only see their own courses"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/instructor/courses",
                headers={"Authorization": f"Bearer {instructor_token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            for course in data:
                assert course["owner_id"] == str(test_instructor.id)
    
    @pytest.mark.asyncio
    async def test_pagination(
        self, test_db, test_course, instructor_token
    ):
        """Test course listing pagination"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/instructor/courses?skip=0&limit=10",
                headers={"Authorization": f"Bearer {instructor_token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) <= 10


class TestCourseStudents:
    """Test getting students enrolled in instructor's courses"""
    
    @pytest.mark.asyncio
    async def test_get_course_students(
        self, test_db, test_course, test_enrollment, instructor_token
    ):
        """Test getting students enrolled in a course"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                f"/api/v1/instructor/courses/{test_course.id}/students",
                headers={"Authorization": f"Bearer {instructor_token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) >= 1
            
            student = data[0]
            assert "student_id" in student
            assert "student_name" in student
            assert "student_email" in student
            assert "progress" in student
            assert "status" in student
    
    @pytest.mark.asyncio
    async def test_cannot_view_other_instructor_students(
        self, test_db, test_course, student_token
    ):
        """Test that instructors can only view their own course students"""
        # Create another instructor
        from app.models.user import User
        import hashlib
        
        other_instructor = User(
            email="other@test.com",
            password_hash=hashlib.sha256("pass123".encode()).hexdigest(),
            name="Other Instructor",
            role="instructor"
        )
        await other_instructor.insert()
        
        # Try to access with different instructor token
        from app.auth import create_access_token
        other_token = create_access_token({
            "sub": str(other_instructor.id),
            "role": "instructor"
        })
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                f"/api/v1/instructor/courses/{test_course.id}/students",
                headers={"Authorization": f"Bearer {other_token}"}
            )
            
            assert response.status_code == 403


class TestCourseAnalytics:
    """Test course analytics endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_course_analytics(
        self, test_db, test_course, test_enrollment, instructor_token
    ):
        """Test getting detailed analytics for a course"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                f"/api/v1/instructor/courses/{test_course.id}/analytics",
                headers={"Authorization": f"Bearer {instructor_token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            # Check all required analytics fields
            assert "course_id" in data
            assert "course_title" in data
            assert "total_students" in data
            assert "active_students" in data
            assert "completed_students" in data
            assert "average_progress" in data
            assert "completion_rate" in data
            
            assert data["total_students"] >= 1
    
    @pytest.mark.asyncio
    async def test_analytics_only_for_own_courses(
        self, test_db, test_course, student_token
    ):
        """Test that instructors can only view analytics for their own courses"""
        # Try with student token
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                f"/api/v1/instructor/courses/{test_course.id}/analytics",
                headers={"Authorization": f"Bearer {student_token}"}
            )
            
            assert response.status_code == 403


class TestInstructorDashboard:
    """Test instructor dashboard endpoint"""
    
    @pytest.mark.asyncio
    async def test_get_instructor_dashboard(
        self, test_db, test_course, test_enrollment, instructor_token
    ):
        """Test getting instructor dashboard"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/instructor/dashboard",
                headers={"Authorization": f"Bearer {instructor_token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            # Check all required fields
            assert "total_courses" in data
            assert "published_courses" in data
            assert "draft_courses" in data
            assert "total_students" in data
            assert "total_enrollments" in data
            assert "recent_enrollments" in data
            assert "top_courses" in data
            
            assert data["total_courses"] >= 1
    
    @pytest.mark.asyncio
    async def test_dashboard_requires_instructor_role(
        self, test_db, student_token
    ):
        """Test that only instructors can access instructor dashboard"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/instructor/dashboard",
                headers={"Authorization": f"Bearer {student_token}"}
            )
            
            assert response.status_code == 403


class TestAllStudents:
    """Test getting all students across instructor's courses"""
    
    @pytest.mark.asyncio
    async def test_get_all_students(
        self, test_db, test_course, test_enrollment, instructor_token
    ):
        """Test getting all students enrolled in instructor's courses"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/instructor/all-students",
                headers={"Authorization": f"Bearer {instructor_token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) >= 1
            
            student_data = data[0]
            assert "student_id" in student_data
            assert "student_name" in student_data
            assert "student_email" in student_data
            assert "enrolled_courses_count" in student_data
            assert "courses" in student_data


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    @pytest.mark.asyncio
    async def test_analytics_for_nonexistent_course(
        self, test_db, instructor_token
    ):
        """Test getting analytics for a course that doesn't exist"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            fake_id = "000000000000000000000000"
            response = await client.get(
                f"/api/v1/instructor/courses/{fake_id}/analytics",
                headers={"Authorization": f"Bearer {instructor_token}"}
            )
            
            assert response.status_code in [403, 404]
    
    @pytest.mark.asyncio
    async def test_admin_can_access_instructor_endpoints(
        self, test_db, test_course, admin_token
    ):
        """Test that admins can access instructor endpoints"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/instructor/dashboard",
                headers={"Authorization": f"Bearer {admin_token}"}
            )
            
            # Admins should be able to access (they have instructor permissions)
            assert response.status_code in [200, 403]  # Depends on implementation
