/**
 * Enrollment Service
 * API integration for student enrollment and instructor course management
 */

import { apiClient } from './api';
import type {
  CourseEnrollment,
  EnrolledCourseInfo,
  StudentDashboardResponse,
  StudentEnrollmentInfo,
  CourseAnalytics,
  InstructorDashboardResponse,
} from '@/types';

export const enrollmentService = {
  // ==================== STUDENT ENDPOINTS ====================
  
  /**
   * Enroll in a course (students only)
   */
  enrollInCourse: async (courseId: string): Promise<CourseEnrollment> => {
    return apiClient.post(`/api/v1/student/courses/${courseId}/enroll`);
  },

  /**
   * Unenroll from a course (students only)
   */
  unenrollFromCourse: async (courseId: string): Promise<{ message: string }> => {
    return apiClient.delete(`/api/v1/student/courses/${courseId}/enroll`);
  },

  /**
   * Get list of enrolled courses
   */
  getEnrolledCourses: async (params?: {
    skip?: number;
    limit?: number;
    status?: 'active' | 'completed' | 'dropped';
  }): Promise<EnrolledCourseInfo[]> => {
    return apiClient.get('/api/v1/student/enrolled-courses', { params });
  },

  /**
   * Get student dashboard with statistics
   */
  getStudentDashboard: async (): Promise<StudentDashboardResponse> => {
    return apiClient.get('/api/v1/student/dashboard');
  },

  // ==================== INSTRUCTOR ENDPOINTS ====================
  
  /**
   * Get all courses created by instructor
   */
  getInstructorCourses: async (params?: {
    skip?: number;
    limit?: number;
  }): Promise<any[]> => {
    return apiClient.get('/api/v1/instructor/courses', { params });
  },

  /**
   * Get students enrolled in a specific course
   */
  getCourseStudents: async (
    courseId: string,
    statusFilter?: 'active' | 'completed' | 'dropped'
  ): Promise<StudentEnrollmentInfo[]> => {
    const params = statusFilter ? { status_filter: statusFilter } : {};
    return apiClient.get(`/api/v1/instructor/courses/${courseId}/students`, { params });
  },

  /**
   * Get detailed analytics for a course
   */
  getCourseAnalytics: async (courseId: string): Promise<CourseAnalytics> => {
    return apiClient.get(`/api/v1/instructor/courses/${courseId}/analytics`);
  },

  /**
   * Get instructor dashboard with overall statistics
   */
  getInstructorDashboard: async (): Promise<InstructorDashboardResponse> => {
    return apiClient.get('/api/v1/instructor/dashboard');
  },

  /**
   * Get all students across instructor's courses
   */
  getAllInstructorStudents: async (params?: {
    skip?: number;
    limit?: number;
  }): Promise<StudentEnrollmentInfo[]> => {
    return apiClient.get('/api/v1/instructor/students', { params });
  },

  // ==================== HELPER METHODS ====================
  
  /**
   * Check if user is enrolled in a course
   */
  checkEnrollment: async (courseId: string): Promise<boolean> => {
    try {
      const enrolledCourses = await enrollmentService.getEnrolledCourses({ limit: 100 });
      return enrolledCourses.some(course => course.course_id === courseId);
    } catch (error) {
      return false;
    }
  },

  /**
   * Get enrollment status for a course
   */
  getEnrollmentStatus: async (
    courseId: string
  ): Promise<'active' | 'completed' | 'dropped' | 'not_enrolled'> => {
    try {
      const enrolledCourses = await enrollmentService.getEnrolledCourses({ limit: 100 });
      const enrollment = enrolledCourses.find(course => course.course_id === courseId);
      return enrollment ? enrollment.enrollment_status as any : 'not_enrolled';
    } catch (error) {
      return 'not_enrolled';
    }
  },
};
