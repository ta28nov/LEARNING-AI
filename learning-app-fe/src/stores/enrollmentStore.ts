/**
 * Enrollment Store
 * Zustand store for managing student enrollments and instructor course management
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { enrollmentService } from '@/services/enrollmentService';
import { toast } from 'react-hot-toast';
import type {
  EnrolledCourseInfo,
  StudentDashboardResponse,
  StudentEnrollmentInfo,
  CourseAnalytics,
  InstructorDashboardResponse,
} from '@/types';

interface EnrollmentState {
  // Student state
  enrolledCourses: EnrolledCourseInfo[];
  studentDashboard: StudentDashboardResponse | null;
  
  // Instructor state
  instructorDashboard: InstructorDashboardResponse | null;
  courseStudents: Record<string, StudentEnrollmentInfo[]>; // courseId -> students
  courseAnalytics: Record<string, CourseAnalytics>; // courseId -> analytics
  
  // Loading states
  isLoadingEnrollments: boolean;
  isLoadingDashboard: boolean;
  isLoadingStudents: boolean;
  isLoadingAnalytics: boolean;
  
  // Student actions
  enrollInCourse: (courseId: string) => Promise<void>;
  unenrollFromCourse: (courseId: string) => Promise<void>;
  fetchEnrolledCourses: (params?: { status?: string }) => Promise<void>;
  fetchStudentDashboard: () => Promise<void>;
  checkEnrollmentStatus: (courseId: string) => Promise<boolean>;
  
  // Instructor actions
  fetchInstructorDashboard: () => Promise<void>;
  fetchCourseStudents: (courseId: string, statusFilter?: string) => Promise<void>;
  fetchCourseAnalytics: (courseId: string) => Promise<void>;
  
  // Reset
  reset: () => void;
}

export const useEnrollmentStore = create<EnrollmentState>()(
  persist(
    (set, get) => ({
      // Initial state
      enrolledCourses: [],
      studentDashboard: null,
      instructorDashboard: null,
      courseStudents: {},
      courseAnalytics: {},
      isLoadingEnrollments: false,
      isLoadingDashboard: false,
      isLoadingStudents: false,
      isLoadingAnalytics: false,

      // ==================== STUDENT ACTIONS ====================
      
      enrollInCourse: async (courseId: string) => {
        try {
          await enrollmentService.enrollInCourse(courseId);
          toast.success('Đã đăng ký khóa học thành công!');
          
          // Refresh enrolled courses and dashboard
          await get().fetchEnrolledCourses();
          await get().fetchStudentDashboard();
        } catch (error: any) {
          const message = error.response?.data?.detail || 'Không thể đăng ký khóa học';
          toast.error(message);
          throw error;
        }
      },

      unenrollFromCourse: async (courseId: string) => {
        try {
          await enrollmentService.unenrollFromCourse(courseId);
          toast.success('Đã hủy đăng ký khóa học');
          
          // Refresh enrolled courses and dashboard
          await get().fetchEnrolledCourses();
          await get().fetchStudentDashboard();
        } catch (error: any) {
          const message = error.response?.data?.detail || 'Không thể hủy đăng ký';
          toast.error(message);
          throw error;
        }
      },

      fetchEnrolledCourses: async (params?: { status?: string }) => {
        set({ isLoadingEnrollments: true });
        try {
          const courses = await enrollmentService.getEnrolledCourses({
            status: params?.status as any,
            limit: 100,
          });
          set({ enrolledCourses: courses, isLoadingEnrollments: false });
        } catch (error) {
          set({ isLoadingEnrollments: false });
          toast.error('Không thể tải danh sách khóa học đã đăng ký');
        }
      },

      fetchStudentDashboard: async () => {
        set({ isLoadingDashboard: true });
        try {
          const dashboard = await enrollmentService.getStudentDashboard();
          set({ studentDashboard: dashboard, isLoadingDashboard: false });
        } catch (error) {
          set({ isLoadingDashboard: false });
          toast.error('Không thể tải dashboard');
        }
      },

      checkEnrollmentStatus: async (courseId: string) => {
        try {
          return await enrollmentService.checkEnrollment(courseId);
        } catch (error) {
          return false;
        }
      },

      // ==================== INSTRUCTOR ACTIONS ====================
      
      fetchInstructorDashboard: async () => {
        set({ isLoadingDashboard: true });
        try {
          const dashboard = await enrollmentService.getInstructorDashboard();
          set({ instructorDashboard: dashboard, isLoadingDashboard: false });
        } catch (error) {
          set({ isLoadingDashboard: false });
          toast.error('Không thể tải instructor dashboard');
        }
      },

      fetchCourseStudents: async (courseId: string, statusFilter?: string) => {
        set({ isLoadingStudents: true });
        try {
          const students = await enrollmentService.getCourseStudents(
            courseId,
            statusFilter as any
          );
          set((state) => ({
            courseStudents: {
              ...state.courseStudents,
              [courseId]: students,
            },
            isLoadingStudents: false,
          }));
        } catch (error) {
          set({ isLoadingStudents: false });
          toast.error('Không thể tải danh sách học viên');
        }
      },

      fetchCourseAnalytics: async (courseId: string) => {
        set({ isLoadingAnalytics: true });
        try {
          const analytics = await enrollmentService.getCourseAnalytics(courseId);
          set((state) => ({
            courseAnalytics: {
              ...state.courseAnalytics,
              [courseId]: analytics,
            },
            isLoadingAnalytics: false,
          }));
        } catch (error) {
          set({ isLoadingAnalytics: false });
          toast.error('Không thể tải analytics');
        }
      },

      // ==================== RESET ====================
      
      reset: () => {
        set({
          enrolledCourses: [],
          studentDashboard: null,
          instructorDashboard: null,
          courseStudents: {},
          courseAnalytics: {},
          isLoadingEnrollments: false,
          isLoadingDashboard: false,
          isLoadingStudents: false,
          isLoadingAnalytics: false,
        });
      },
    }),
    {
      name: 'enrollment-storage',
      partialize: (state) => ({
        enrolledCourses: state.enrolledCourses,
        studentDashboard: state.studentDashboard,
        instructorDashboard: state.instructorDashboard,
      }),
    }
  )
);
