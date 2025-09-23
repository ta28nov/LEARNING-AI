import { apiClient } from './api';

export interface SearchResult {
  id: string;
  title: string;
  content: string;
  source_type: 'course' | 'upload';
  source_id: string;
  relevance_score: number;
  metadata?: Record<string, any>;
}

export interface SearchResponse {
  results: SearchResult[];
  total: number;
  query: string;
  took_ms: number;
}

export const searchService = {
  // Vector search
  async search(data: {
    query: string;
    source_types?: ('course' | 'upload')[];
    limit?: number;
    min_relevance?: number;
  }): Promise<SearchResponse> {
    return apiClient.post('/api/v1/search', data);
  },

  // Reindex embeddings
  async reindexEmbeddings(data: {
    source_type?: 'course' | 'upload';
    source_ids?: string[];
  }): Promise<{ message: string; processed: number }> {
    return apiClient.post('/api/v1/embeddings', data);
  },

  // Reindex specific course
  async reindexCourse(courseId: string): Promise<{ message: string }> {
    return apiClient.post(`/api/v1/courses/${courseId}/reindex`);
  },
};
