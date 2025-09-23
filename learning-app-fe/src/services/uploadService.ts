import { apiClient } from './api';
import { Upload } from '@/types';

export const uploadService = {
  async uploadFile(file: File): Promise<Upload> {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient.upload('/api/v1/uploads', formData);
  },

  async getUploads(params?: { skip?: number; limit?: number }): Promise<Upload[]> {
    return apiClient.get('/api/v1/uploads', { params });
  },

  async getUpload(uploadId: string): Promise<Upload> {
    return apiClient.get(`/api/v1/uploads/${uploadId}`);
  },

  async deleteUpload(uploadId: string): Promise<void> {
    return apiClient.delete(`/api/v1/uploads/${uploadId}`);
  },

  async getUploadStatus(uploadId: string): Promise<{ status: string }> {
    return apiClient.get(`/api/v1/uploads/${uploadId}/status`);
  },

  async reprocessUpload(uploadId: string): Promise<Upload> {
    return apiClient.post(`/api/v1/uploads/${uploadId}/reprocess`);
  },
};
