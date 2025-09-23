import { apiClient } from './api';
import { ChatSession, ChatMessage } from '@/types';

export const chatService = {
  // Freestyle chat (main endpoint)
  async freestyleChat(data: { message: string; mode?: 'strict' | 'hybrid' }): Promise<{ message: string; answer: string }> {
    return apiClient.post('/api/v1/chat', data);
  },

  // Chat sessions
  async getSessions(params?: { skip?: number; limit?: number }): Promise<ChatSession[]> {
    return apiClient.get('/api/v1/chat/sessions', { params });
  },

  async getSession(sessionId: string): Promise<ChatSession> {
    return apiClient.get(`/api/v1/chat/sessions/${sessionId}`);
  },

  async getMessages(sessionId: string, params?: { skip?: number; limit?: number }): Promise<ChatMessage[]> {
    return apiClient.get(`/api/v1/chat/sessions/${sessionId}/messages`, { params });
  },

  async saveAsCourse(sessionId: string, data: { title: string; description: string }): Promise<{ course_id: string }> {
    return apiClient.post(`/api/v1/chat/sessions/${sessionId}/save-as-course`, data);
  },

  // Chat history
  async getChatHistory(params?: { skip?: number; limit?: number }): Promise<ChatMessage[]> {
    return apiClient.get('/api/v1/chat/history', { params });
  },

  async saveChatHistory(data: { title: string; description: string }): Promise<{ course_id: string }> {
    return apiClient.post('/api/v1/chat/save', data);
  },

  // Legacy methods for compatibility
  async createSession(data: { course_id?: string; upload_id?: string; title: string; mode: 'strict' | 'hybrid' }): Promise<ChatSession> {
    // Create a simple session object since backend doesn't have this endpoint
    return {
      id: Date.now().toString(),
      user_id: 'current-user',
      title: data.title,
      mode: data.mode,
      status: 'active',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      course_id: data.course_id,
      upload_id: data.upload_id,
    };
  },

  async sendMessage(sessionId: string, message: string): Promise<{ message: string; answer: string }> {
    // Use freestyle chat for now
    return this.freestyleChat({ message });
  },

  async deleteSession(sessionId: string): Promise<void> {
    // Not implemented in backend
    return Promise.resolve();
  },
};
