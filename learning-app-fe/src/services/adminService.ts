import { apiClient } from './api';
import { User, Course } from '@/types';

export const adminService = {
  // User management
  async getUsers(params?: { skip?: number; limit?: number }): Promise<User[]> {
    return apiClient.get('/api/v1/admin/users', { params });
  },

  async updateUserRole(userId: string, role: 'student' | 'instructor' | 'admin'): Promise<User> {
    return apiClient.patch(`/api/v1/admin/users/${userId}/role`, { role });
  },

  // Course management
  async getAllCourses(params?: { skip?: number; limit?: number }): Promise<Course[]> {
    return apiClient.get('/api/v1/admin/courses', { params });
  },

  async createSampleCourse(): Promise<Course> {
    return apiClient.post('/api/v1/admin/courses');
  },

  async deleteCourse(courseId: string): Promise<void> {
    return apiClient.delete(`/api/v1/admin/courses/${courseId}`);
  },

  async importCourses(data: { courses: any[] }): Promise<{ imported: number; failed: number }> {
    return apiClient.post('/api/v1/admin/courses/import', data);
  },

  // System stats
  async getSystemStats(): Promise<{
    total_users: number;
    total_courses: number;
    total_uploads: number;
    total_quizzes: number;
    active_users_today: number;
    active_users_week: number;
    recent_activity: Array<{
      type: string;
      description: string;
      timestamp: string;
      user_id?: string;
    }>;
  }> {
    return apiClient.get('/api/v1/admin/stats');
  },
};
