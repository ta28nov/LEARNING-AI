import { create } from 'zustand';
import { Upload } from '@/types';
import { uploadService } from '@/services/uploadService';
import toast from 'react-hot-toast';

interface UploadState {
  uploads: Upload[];
  currentUpload: Upload | null;
  isUploading: boolean;
  uploadProgress: number;
  
  // Actions
  fetchUploads: (params?: { skip?: number; limit?: number }) => Promise<void>;
  uploadFile: (file: File, onProgress?: (progress: number) => void) => Promise<Upload>;
  getUpload: (uploadId: string) => Promise<void>;
  deleteUpload: (uploadId: string) => Promise<void>;
  reprocessUpload: (uploadId: string) => Promise<void>;
  checkUploadStatus: (uploadId: string) => Promise<string>;
}

export const useUploadStore = create<UploadState>((set, get) => ({
  uploads: [],
  currentUpload: null,
  isUploading: false,
  uploadProgress: 0,

  fetchUploads: async (params) => {
    try {
      const uploads = await uploadService.getUploads(params);
      set({ uploads });
    } catch (error) {
      console.error('Failed to fetch uploads:', error);
    }
  },

  uploadFile: async (file: File, onProgress) => {
    try {
      set({ isUploading: true, uploadProgress: 0 });
      
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        set(state => {
          const newProgress = Math.min(state.uploadProgress + 10, 90);
          onProgress?.(newProgress);
          return { uploadProgress: newProgress };
        });
      }, 200);

      const upload = await uploadService.uploadFile(file);
      
      clearInterval(progressInterval);
      set({ uploadProgress: 100 });
      
      set(state => ({ 
        uploads: [upload, ...state.uploads],
        currentUpload: upload 
      }));
      
      toast.success('File uploaded successfully!');
      return upload;
    } catch (error) {
      toast.error('Failed to upload file');
      throw error;
    } finally {
      set({ isUploading: false, uploadProgress: 0 });
    }
  },

  getUpload: async (uploadId: string) => {
    try {
      const upload = await uploadService.getUpload(uploadId);
      set({ currentUpload: upload });
    } catch (error) {
      console.error('Failed to fetch upload:', error);
    }
  },

  deleteUpload: async (uploadId: string) => {
    try {
      await uploadService.deleteUpload(uploadId);
      set(state => ({
        uploads: state.uploads.filter(u => u.id !== uploadId),
        currentUpload: state.currentUpload?.id === uploadId ? null : state.currentUpload
      }));
      toast.success('File deleted successfully!');
    } catch (error) {
      throw error;
    }
  },

  reprocessUpload: async (uploadId: string) => {
    try {
      const upload = await uploadService.reprocessUpload(uploadId);
      set(state => ({
        uploads: state.uploads.map(u => u.id === uploadId ? upload : u),
        currentUpload: state.currentUpload?.id === uploadId ? upload : state.currentUpload
      }));
      toast.success('File reprocessed successfully!');
    } catch (error) {
      throw error;
    }
  },

  checkUploadStatus: async (uploadId: string) => {
    try {
      const result = await uploadService.getUploadStatus(uploadId);
      return result.status;
    } catch (error) {
      throw error;
    }
  },
}));
