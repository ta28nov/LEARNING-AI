import { apiClient } from './api';

export interface LeaderboardEntry {
  user_id: string;
  username: string;
  avatar?: string;
  total_score: number;
  quizzes_completed: number;
  courses_completed: number;
  rank: number;
  badges?: string[];
}

export interface LeaderboardResponse {
  entries: LeaderboardEntry[];
  user_rank?: number;
  total_users: number;
  period: 'all_time' | 'monthly' | 'weekly';
}

export const leaderboardService = {
  async getLeaderboard(params?: {
    period?: 'all_time' | 'monthly' | 'weekly';
    limit?: number;
    offset?: number;
  }): Promise<LeaderboardResponse> {
    return apiClient.get('/api/v1/leaderboard', { params });
  },
};
