"""
Tests for Enrollment Models
"""
import pytest
from datetime import datetime
from app.models.enrollment import (
    CourseEnrollment,
    ChapterProgress,
    EnrollmentStatus,
    ChapterProgressStatus
)


class TestCourseEnrollment:
    """Test CourseEnrollment model"""
    
    @pytest.mark.asyncio
    async def test_create_enrollment(self, test_db, test_student, test_course):
        """Test creating a course enrollment"""
        enrollment = CourseEnrollment(
            student_id=test_student.id,
            course_id=test_course.id,
            status=EnrollmentStatus.ACTIVE,
            progress=0.0
        )
        await enrollment.insert()
        
        assert enrollment.id is not None
        assert enrollment.student_id == test_student.id
        assert enrollment.course_id == test_course.id
        assert enrollment.status == EnrollmentStatus.ACTIVE
        assert enrollment.progress == 0.0
        assert enrollment.enrolled_at is not None
    
    @pytest.mark.asyncio
    async def test_unique_enrollment(self, test_db, test_enrollment, test_student, test_course):
        """Test that a student cannot enroll twice in the same course"""
        # Try to create duplicate enrollment
        with pytest.raises(Exception):  # Should raise duplicate key error
            duplicate = CourseEnrollment(
                student_id=test_student.id,
                course_id=test_course.id,
                status=EnrollmentStatus.ACTIVE
            )
            await duplicate.insert()
    
    @pytest.mark.asyncio
    async def test_enrollment_status_update(self, test_db, test_enrollment):
        """Test updating enrollment status"""
        test_enrollment.status = EnrollmentStatus.COMPLETED
        test_enrollment.progress = 100.0
        test_enrollment.completed_at = datetime.utcnow()
        await test_enrollment.save()
        
        # Fetch and verify
        updated = await CourseEnrollment.get(test_enrollment.id)
        assert updated.status == EnrollmentStatus.COMPLETED
        assert updated.progress == 100.0
        assert updated.completed_at is not None
    
    @pytest.mark.asyncio
    async def test_find_enrollments_by_student(self, test_db, test_enrollment, test_student):
        """Test finding all enrollments for a student"""
        enrollments = await CourseEnrollment.find(
            CourseEnrollment.student_id == test_student.id
        ).to_list()
        
        assert len(enrollments) >= 1
        assert enrollments[0].student_id == test_student.id
    
    @pytest.mark.asyncio
    async def test_find_enrollments_by_course(self, test_db, test_enrollment, test_course):
        """Test finding all enrollments for a course"""
        enrollments = await CourseEnrollment.find(
            CourseEnrollment.course_id == test_course.id
        ).to_list()
        
        assert len(enrollments) >= 1
        assert enrollments[0].course_id == test_course.id
    
    @pytest.mark.asyncio
    async def test_enrollment_progress_range(self, test_db, test_student, test_course):
        """Test that progress is within valid range"""
        enrollment = CourseEnrollment(
            student_id=test_student.id,
            course_id=test_course.id,
            progress=50.5
        )
        await enrollment.insert()
        
        assert 0 <= enrollment.progress <= 100
    
    @pytest.mark.asyncio
    async def test_delete_enrollment(self, test_db, test_enrollment):
        """Test deleting an enrollment"""
        enrollment_id = test_enrollment.id
        await test_enrollment.delete()
        
        # Verify deletion
        deleted = await CourseEnrollment.get(enrollment_id)
        assert deleted is None


class TestChapterProgress:
    """Test ChapterProgress model"""
    
    @pytest.mark.asyncio
    async def test_create_chapter_progress(self, test_db, test_student, test_course):
        """Test creating chapter progress"""
        # Create a dummy chapter_id
        from bson import ObjectId
        chapter_id = ObjectId()
        
        progress = ChapterProgress(
            user_id=test_student.id,
            course_id=test_course.id,
            chapter_id=chapter_id,
            status=ChapterProgressStatus.NOT_STARTED,
            time_spent=0
        )
        await progress.insert()
        
        assert progress.id is not None
        assert progress.user_id == test_student.id
        assert progress.course_id == test_course.id
        assert progress.chapter_id == chapter_id
        assert progress.status == ChapterProgressStatus.NOT_STARTED
        assert progress.time_spent == 0
    
    @pytest.mark.asyncio
    async def test_update_chapter_progress(self, test_db, test_student, test_course):
        """Test updating chapter progress"""
        from bson import ObjectId
        chapter_id = ObjectId()
        
        progress = ChapterProgress(
            user_id=test_student.id,
            course_id=test_course.id,
            chapter_id=chapter_id,
            status=ChapterProgressStatus.NOT_STARTED
        )
        await progress.insert()
        
        # Update progress
        progress.status = ChapterProgressStatus.IN_PROGRESS
        progress.time_spent = 30  # 30 minutes
        progress.last_accessed = datetime.utcnow()
        await progress.save()
        
        # Verify
        updated = await ChapterProgress.get(progress.id)
        assert updated.status == ChapterProgressStatus.IN_PROGRESS
        assert updated.time_spent == 30
        assert updated.last_accessed is not None
    
    @pytest.mark.asyncio
    async def test_complete_chapter(self, test_db, test_student, test_course):
        """Test completing a chapter"""
        from bson import ObjectId
        chapter_id = ObjectId()
        
        progress = ChapterProgress(
            user_id=test_student.id,
            course_id=test_course.id,
            chapter_id=chapter_id,
            status=ChapterProgressStatus.IN_PROGRESS,
            time_spent=45
        )
        await progress.insert()
        
        # Complete chapter
        progress.status = ChapterProgressStatus.COMPLETED
        progress.completed_at = datetime.utcnow()
        await progress.save()
        
        # Verify
        completed = await ChapterProgress.get(progress.id)
        assert completed.status == ChapterProgressStatus.COMPLETED
        assert completed.completed_at is not None
    
    @pytest.mark.asyncio
    async def test_find_chapter_progress_by_user(self, test_db, test_student, test_course):
        """Test finding all chapter progress for a user"""
        from bson import ObjectId
        
        # Create multiple chapter progress records
        for i in range(3):
            progress = ChapterProgress(
                user_id=test_student.id,
                course_id=test_course.id,
                chapter_id=ObjectId(),
                status=ChapterProgressStatus.NOT_STARTED
            )
            await progress.insert()
        
        # Find all
        all_progress = await ChapterProgress.find(
            ChapterProgress.user_id == test_student.id
        ).to_list()
        
        assert len(all_progress) >= 3
    
    @pytest.mark.asyncio
    async def test_chapter_progress_by_course(self, test_db, test_student, test_course):
        """Test finding chapter progress for a specific course"""
        from bson import ObjectId
        
        # Create progress for this course
        progress = ChapterProgress(
            user_id=test_student.id,
            course_id=test_course.id,
            chapter_id=ObjectId()
        )
        await progress.insert()
        
        # Find by course
        course_progress = await ChapterProgress.find(
            ChapterProgress.course_id == test_course.id,
            ChapterProgress.user_id == test_student.id
        ).to_list()
        
        assert len(course_progress) >= 1
        assert course_progress[0].course_id == test_course.id
