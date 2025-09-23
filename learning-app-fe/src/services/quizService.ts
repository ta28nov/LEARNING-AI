import { apiClient } from './api';
import { Quiz, QuizQuestion, QuizAnswer, QuizHistory } from '@/types';

export const quizService = {
  // Quiz generation
  async generateQuiz(data: { 
    source_type: 'course' | 'upload';
    source_id: string; 
    title: string; 
    num_questions: number;
    difficulty?: 'easy' | 'medium' | 'hard';
  }): Promise<Quiz> {
    return apiClient.post('/api/v1/quiz/generate', data);
  },

  // Manual quiz creation
  async createQuiz(data: { 
    title: string; 
    questions: Array<{
      question: string;
      options: string[];
      correct_answer: number;
      explanation?: string;
    }>;
  }): Promise<Quiz> {
    return apiClient.post('/api/v1/quiz/manual', data);
  },

  async getQuiz(quizId: string): Promise<Quiz> {
    return apiClient.get(`/api/v1/quiz/${quizId}`);
  },

  async updateQuiz(quizId: string, data: Partial<Quiz>): Promise<Quiz> {
    return apiClient.patch(`/api/v1/quiz/${quizId}`, data);
  },

  async deleteQuiz(quizId: string): Promise<void> {
    return apiClient.delete(`/api/v1/quiz/${quizId}`);
  },

  // Quiz submission and grading
  async submitQuiz(quizId: string, answers: Array<{
    question_index: number;
    selected_answer: number;
  }>): Promise<QuizHistory> {
    return apiClient.post(`/api/v1/quiz/${quizId}/submit`, { answers });
  },

  async gradeQuiz(quizId: string, answers: Array<{
    question_index: number;
    selected_answer: number;
  }>): Promise<{
    score: number;
    total_questions: number;
    correct_answers: number;
    results: Array<{
      question_index: number;
      correct: boolean;
      explanation?: string;
    }>;
  }> {
    return apiClient.post(`/api/v1/quiz/${quizId}/grade`, { answers });
  },

  async getQuizResults(quizId: string): Promise<QuizHistory[]> {
    return apiClient.get(`/api/v1/quiz/${quizId}/results`);
  },

  // Quiz history
  async getQuizHistory(params?: { skip?: number; limit?: number }): Promise<QuizHistory[]> {
    return apiClient.get('/api/v1/quiz/history', { params });
  },

  async getQuizHistoryDetail(historyId: string): Promise<QuizHistory> {
    return apiClient.get(`/api/v1/quiz/history/${historyId}`);
  },

  // Legacy methods for compatibility
  async getQuizQuestions(quizId: string): Promise<QuizQuestion[]> {
    const quiz = await this.getQuiz(quizId);
    // Convert quiz structure to questions array
    return [];
  },

  async createQuizFromCourse(courseId: string, data: { title: string; num_questions: number }): Promise<Quiz> {
    return this.generateQuiz({
      source_type: 'course',
      source_id: courseId,
      title: data.title,
      num_questions: data.num_questions,
    });
  },

  async createQuizFromUpload(uploadId: string, data: { title: string; num_questions: number }): Promise<Quiz> {
    return this.generateQuiz({
      source_type: 'upload',
      source_id: uploadId,
      title: data.title,
      num_questions: data.num_questions,
    });
  },
};
