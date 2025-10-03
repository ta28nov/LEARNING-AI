import React from 'react';
import { useTranslation } from 'react-i18next';
import { Button } from './Button';
import { CheckCircle2, XCircle, Loader2, Lock, Users } from 'lucide-react';
import { useEnrollmentStore } from '@/stores/enrollmentStore';
import { useAuthStore } from '@/stores/authStore';
import type { Course } from '@/types';

interface EnrollButtonProps {
  course: Course;
  onEnrollmentChange?: () => void;
}

export const EnrollButton: React.FC<EnrollButtonProps> = ({ course, onEnrollmentChange }) => {
  const { t } = useTranslation();
  const { user } = useAuthStore();
  const { enrollInCourse, unenrollFromCourse, enrolledCourses, isLoadingEnrollments } = useEnrollmentStore();

  // Check if user is enrolled
  const enrollment = enrolledCourses.find(e => e.course_id === course.id);
  const isEnrolled = enrollment?.enrollment_status === 'active';
  const isCompleted = enrollment?.enrollment_status === 'completed';

  // Don't show button for instructor/admin or own courses
  if (!user || user.role !== 'student' || user.id === course.owner_id) {
    return null;
  }

  // Don't allow enrollment in DRAFT courses
  if (course.visibility === 'DRAFT') {
    return (
      <Button
        variant="outline"
        size="lg"
        disabled
        className="cursor-not-allowed"
      >
        <Lock className="mr-2 h-5 w-5" />
        {t('course.draft')}
      </Button>
    );
  }

  // Don't allow enrollment in PRIVATE courses (should not happen in UI)
  if (course.visibility === 'PRIVATE') {
    return (
      <Button
        variant="outline"
        size="lg"
        disabled
        className="cursor-not-allowed"
      >
        <Lock className="mr-2 h-5 w-5" />
        {t('course.private')}
      </Button>
    );
  }

  const handleEnroll = async () => {
    try {
      await enrollInCourse(course.id);
      onEnrollmentChange?.();
    } catch (error) {
      console.error('Enrollment failed:', error);
    }
  };

  const handleUnenroll = async () => {
    if (!window.confirm(t('course.confirmUnenroll'))) {
      return;
    }
    
    try {
      await unenrollFromCourse(course.id);
      onEnrollmentChange?.();
    } catch (error) {
      console.error('Unenrollment failed:', error);
    }
  };

  // If completed, show completed status
  if (isCompleted) {
    return (
      <Button
        variant="success"
        size="lg"
        disabled
      >
        <CheckCircle2 className="mr-2 h-5 w-5" />
        {t('course.completed')}
      </Button>
    );
  }

  // If enrolled, show unenroll button
  if (isEnrolled) {
    return (
      <Button
        variant="outline"
        size="lg"
        onClick={handleUnenroll}
        isLoading={isLoadingEnrollments}
        className="hover:border-error-500 hover:text-error-600 hover:bg-error-50 dark:hover:bg-error-900/20"
      >
        {!isLoadingEnrollments && <XCircle className="mr-2 h-5 w-5" />}
        {t('course.unenroll')}
      </Button>
    );
  }

  // Default: show enroll button
  return (
    <Button
      variant="primary"
      size="lg"
      onClick={handleEnroll}
      isLoading={isLoadingEnrollments}
    >
      {!isLoadingEnrollments && <Users className="mr-2 h-5 w-5" />}
      {t('course.enroll')}
    </Button>
  );
};
