import { create } from 'zustand';
import { DashboardStats, Progress } from '@/types';
import { dashboardService } from '@/services/dashboardService';

interface DashboardState {
  stats: DashboardStats | null;
  progress: Progress[];
  recommendations: Array<{
    type: string;
    title: string;
    description: string;
    course_id?: string;
    priority: 'high' | 'medium' | 'low';
  }>;
  isLoading: boolean;
  
  // Actions
  fetchStats: () => Promise<void>;
  fetchProgress: (courseId?: string) => Promise<void>;
  updateProgress: (data: {
    course_id: string;
    chapter_id?: string;
    status: 'not_started' | 'in_progress' | 'completed';
    progress: number;
    time_spent: number;
  }) => Promise<void>;
  fetchRecommendations: () => Promise<void>;
}

export const useDashboardStore = create<DashboardState>((set, get) => ({
  stats: null,
  progress: [],
  recommendations: [],
  isLoading: false,

  fetchStats: async () => {
    try {
      set({ isLoading: true });
      const stats = await dashboardService.getStats();
      set({ stats });
    } catch (error) {
      console.error('Failed to fetch dashboard stats:', error);
    } finally {
      set({ isLoading: false });
    }
  },

  fetchProgress: async (courseId) => {
    try {
      const progress = await dashboardService.getProgress(courseId ? { course_id: courseId } : undefined);
      set({ progress });
    } catch (error) {
      console.error('Failed to fetch progress:', error);
    }
  },

  updateProgress: async (data) => {
    try {
      await dashboardService.updateProgress(data);
      // Refetch progress after update
      await get().fetchProgress();
    } catch (error) {
      throw error;
    }
  },

  fetchRecommendations: async () => {
    try {
      const recommendations = await dashboardService.getRecommendations();
      set({ recommendations });
    } catch (error) {
      console.error('Failed to fetch recommendations:', error);
    }
  },
}));
