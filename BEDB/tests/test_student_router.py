"""
Tests for Student Router Endpoints
Test coverage for /api/v1/student/* endpoints
"""
import pytest
from httpx import AsyncClient
from app.main import app
from app.models.enrollment import EnrollmentStatus


class TestStudentEnrollment:
    """Test student enrollment endpoints"""
    
    @pytest.mark.asyncio
    async def test_enroll_in_public_course(
        self, test_db, test_student, test_course, student_token
    ):
        """Test enrolling in a public approved course"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/v1/student/courses/{test_course.id}/enroll",
                headers={"Authorization": f"Bearer {student_token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["student_id"] == str(test_student.id)
            assert data["course_id"] == str(test_course.id)
            assert data["status"] == "active"
            assert data["progress"] == 0.0
    
    @pytest.mark.asyncio
    async def test_cannot_enroll_in_draft_course(
        self, test_db, test_student, test_draft_course, student_token
    ):
        """Test that students cannot enroll in draft courses"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/v1/student/courses/{test_draft_course.id}/enroll",
                headers={"Authorization": f"Bearer {student_token}"}
            )
            
            assert response.status_code == 400
            assert "non-public" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_cannot_enroll_twice(
        self, test_db, test_enrollment, test_course, student_token
    ):
        """Test that students cannot enroll twice in the same course"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/v1/student/courses/{test_course.id}/enroll",
                headers={"Authorization": f"Bearer {student_token}"}
            )
            
            assert response.status_code == 400
            assert "already enrolled" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_unenroll_from_course(
        self, test_db, test_enrollment, test_course, student_token
    ):
        """Test unenrolling from a course"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.delete(
                f"/api/v1/student/courses/{test_course.id}/enroll",
                headers={"Authorization": f"Bearer {student_token}"}
            )
            
            assert response.status_code == 200
            assert "unenrolled" in response.json()["message"].lower()
    
    @pytest.mark.asyncio
    async def test_enrollment_requires_student_role(
        self, test_db, test_course, instructor_token
    ):
        """Test that only students can enroll"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/v1/student/courses/{test_course.id}/enroll",
                headers={"Authorization": f"Bearer {instructor_token}"}
            )
            
            assert response.status_code == 403


class TestStudentCourses:
    """Test student course listing endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_enrolled_courses(
        self, test_db, test_enrollment, student_token
    ):
        """Test getting list of enrolled courses"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/student/enrolled-courses",
                headers={"Authorization": f"Bearer {student_token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) >= 1
            assert "course_details" in data[0]
    
    @pytest.mark.asyncio
    async def test_filter_by_status(
        self, test_db, test_enrollment, student_token
    ):
        """Test filtering enrolled courses by status"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/student/enrolled-courses?status=active",
                headers={"Authorization": f"Bearer {student_token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            for enrollment in data:
                assert enrollment["status"] == "active"
    
    @pytest.mark.asyncio
    async def test_pagination(
        self, test_db, test_enrollment, student_token
    ):
        """Test pagination of enrolled courses"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/student/enrolled-courses?skip=0&limit=5",
                headers={"Authorization": f"Bearer {student_token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) <= 5


class TestStudentDashboard:
    """Test student dashboard endpoint"""
    
    @pytest.mark.asyncio
    async def test_get_dashboard(
        self, test_db, test_enrollment, student_token
    ):
        """Test getting student dashboard"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/student/dashboard",
                headers={"Authorization": f"Bearer {student_token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            # Check all required fields
            assert "total_enrollments" in data
            assert "active_enrollments" in data
            assert "completed_courses" in data
            assert "total_progress" in data
            assert "recent_courses" in data
            assert "achievements" in data
            
            assert data["total_enrollments"] >= 1
    
    @pytest.mark.asyncio
    async def test_dashboard_requires_auth(self, test_db):
        """Test that dashboard requires authentication"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/v1/student/dashboard")
            
            assert response.status_code == 401


# Additional test cases for edge cases
class TestEdgeCases:
    """Test edge cases and error handling"""
    
    @pytest.mark.asyncio
    async def test_enroll_nonexistent_course(
        self, test_db, student_token
    ):
        """Test enrolling in a course that doesn't exist"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            fake_id = "000000000000000000000000"
            response = await client.post(
                f"/api/v1/student/courses/{fake_id}/enroll",
                headers={"Authorization": f"Bearer {student_token}"}
            )
            
            assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_unenroll_not_enrolled(
        self, test_db, test_course, student_token
    ):
        """Test unenrolling from a course student is not enrolled in"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.delete(
                f"/api/v1/student/courses/{test_course.id}/enroll",
                headers={"Authorization": f"Bearer {student_token}"}
            )
            
            assert response.status_code == 404
