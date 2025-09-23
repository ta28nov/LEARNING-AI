import { apiClient } from './api';
import { DashboardStats, Progress } from '@/types';

export const dashboardService = {
  // Dashboard overview
  async getOverview(): Promise<DashboardStats> {
    return apiClient.get('/api/v1/dashboard/overview');
  },

  // Progress tracking
  async getCourseProgress(courseId: string): Promise<Progress> {
    return apiClient.get(`/api/v1/dashboard/progress/${courseId}`);
  },

  async updateCourseProgress(courseId: string, data: {
    progress_percentage: number;
    time_spent_minutes: number;
    completed_sections?: string[];
    notes?: string;
  }): Promise<{ message: string }> {
    return apiClient.post(`/api/v1/dashboard/progress/${courseId}`, data);
  },

  async getCourseStats(courseId: string): Promise<{
    total_time_spent: number;
    completion_percentage: number;
    quiz_scores: number[];
    last_accessed: string;
    sections_completed: number;
    total_sections: number;
  }> {
    return apiClient.get(`/api/v1/dashboard/course-stats/${courseId}`);
  },

  // Recommendations
  async getRecommendations(): Promise<Array<{
    type: 'continue_course' | 'review_quiz' | 'new_topic' | 'practice_more';
    title: string;
    description: string;
    course_id?: string;
    priority: 'high' | 'medium' | 'low';
    action_url?: string;
  }>> {
    return apiClient.get('/api/v1/dashboard/recommendations');
  },

  // Legacy methods for compatibility
  async getStats(): Promise<DashboardStats> {
    return this.getOverview();
  },

  async getProgress(params?: { course_id?: string }): Promise<Progress[]> {
    if (params?.course_id) {
      const progress = await this.getCourseProgress(params.course_id);
      return [progress];
    }
    // Return empty array if no specific course
    return [];
  },

  async updateProgress(data: {
    course_id: string;
    chapter_id?: string;
    status: 'not_started' | 'in_progress' | 'completed';
    progress: number;
    time_spent: number;
  }): Promise<{ message: string }> {
    return this.updateCourseProgress(data.course_id, {
      progress_percentage: data.progress,
      time_spent_minutes: data.time_spent,
    });
  },
};
