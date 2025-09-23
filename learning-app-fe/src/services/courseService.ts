import { apiClient } from './api';
import { Course, Chapter, CourseForm, ChapterForm } from '@/types';

export const courseService = {
  // Courses
  async getCourses(params?: { skip?: number; limit?: number; owner?: string }): Promise<Course[]> {
    return apiClient.get('/api/v1/courses', { params });
  },

  async getCourse(courseId: string): Promise<Course> {
    return apiClient.get(`/api/v1/courses/${courseId}`);
  },

  async createCourse(courseData: CourseForm): Promise<Course> {
    return apiClient.post('/api/v1/courses', courseData);
  },

  async createCourseFromPrompt(data: { topic: string; level: string }): Promise<Course> {
    return apiClient.post('/api/v1/courses/from-prompt', data);
  },

  async updateCourse(courseId: string, courseData: Partial<CourseForm>): Promise<Course> {
    return apiClient.patch(`/api/v1/courses/${courseId}`, courseData);
  },

  async deleteCourse(courseId: string): Promise<void> {
    return apiClient.delete(`/api/v1/courses/${courseId}`);
  },

  // Chapters - Note: Backend doesn't have chapter endpoints, they're part of course
  async getChapters(courseId: string): Promise<Chapter[]> {
    // This will be handled by getting course details and extracting chapters
    const course = await this.getCourse(courseId);
    return []; // Backend stores chapters differently
  },

  async getChapter(courseId: string, chapterId: string): Promise<Chapter> {
    // This will need to be implemented differently based on backend structure
    throw new Error('Chapter endpoints not implemented in backend');
  },

  async createChapter(courseId: string, chapterData: ChapterForm): Promise<Chapter> {
    // This will need to be implemented differently based on backend structure
    throw new Error('Chapter endpoints not implemented in backend');
  },

  async updateChapter(courseId: string, chapterId: string, chapterData: Partial<ChapterForm>): Promise<Chapter> {
    // This will need to be implemented differently based on backend structure
    throw new Error('Chapter endpoints not implemented in backend');
  },

  async deleteChapter(courseId: string, chapterId: string): Promise<void> {
    // This will need to be implemented differently based on backend structure
    throw new Error('Chapter endpoints not implemented in backend');
  },

  // AI Features
  async generateOutline(courseId: string, data: { topic: string; level: string }): Promise<{ outline: string }> {
    return apiClient.post(`/api/v1/courses/${courseId}/generate-outline`, data);
  },

  async chatWithCourse(courseId: string, data: { message: string; mode: 'strict' | 'hybrid' }): Promise<{ message: string; answer: string }> {
    return apiClient.post(`/api/v1/courses/${courseId}/chat`, data);
  },

  async summarizeChapter(courseId: string, data: { content: string }): Promise<{ summary: string }> {
    return apiClient.post(`/api/v1/courses/${courseId}/summarize`, data);
  },

  async generateFlashcards(courseId: string, data: { content: string }): Promise<{ flashcards: Array<{ question: string; answer: string }> }> {
    return apiClient.post(`/api/v1/courses/${courseId}/flashcards`, data);
  },
};
