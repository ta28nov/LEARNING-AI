import { apiClient } from './api';
import { User, AuthTokens, LoginForm, RegisterForm } from '@/types';

export const authService = {
  // Authentication
  async login(credentials: LoginForm): Promise<AuthTokens> {
    return apiClient.post('/api/v1/auth/login', credentials);
  },

  async register(userData: RegisterForm): Promise<User> {
    return apiClient.post('/api/v1/auth/register', userData);
  },

  async logout(): Promise<void> {
    return apiClient.post('/api/v1/auth/logout');
  },

  async refreshToken(): Promise<AuthTokens> {
    return apiClient.post('/api/v1/auth/refresh');
  },

  // User profile
  async getCurrentUser(): Promise<User> {
    return apiClient.get('/api/v1/auth/me');
  },

  async updateProfile(userData: Partial<User>): Promise<User> {
    return apiClient.patch('/api/v1/users/me', userData);
  },

  async changePassword(data: { current_password: string; new_password: string }): Promise<void> {
    return apiClient.patch('/api/v1/users/me/password', data);
  },

  // Email verification
  async verifyEmail(data: { email: string; otp: string }): Promise<void> {
    return apiClient.post('/api/v1/auth/verify-email', data);
  },

  async forgotPassword(email: string): Promise<void> {
    return apiClient.post('/api/v1/auth/forgot-password', { email });
  },

  async resetPassword(data: { token: string; new_password: string }): Promise<void> {
    return apiClient.post('/api/v1/auth/reset-password', data);
  },
};
