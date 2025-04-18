import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const authAPI = {
  login: async (email: string, password: string) => {
    const formData = new FormData();
    formData.append('username', email); // FastAPI OAuth expects 'username'
    formData.append('password', password);
    
    const response = await apiClient.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },
  
  register: async (userData: { email: string; username: string; password: string }) => {
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  },
  
  getCurrentUser: async () => {
    const response = await apiClient.get('/users/me');
    return response.data;
  },
};

export const audioAPI = {
  uploadAudio: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await apiClient.post('/audio/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },
  
  getUserAudioFiles: async () => {
    const response = await apiClient.get('/audio/files');
    return response.data;
  },
  
  getAudioFile: async (fileId: string) => {
    const response = await apiClient.get(`/audio/files/${fileId}`);
    return response.data;
  },
  
  analyzeAudio: async (fileId: string, analysisType: string = 'general', aiService?: string) => {
    const params: Record<string, string> = {};
    if (aiService) {
      params.ai_service = aiService;
    }
    
    const response = await apiClient.post(`/audio/analyze/${fileId}`, {
      analysis_type: analysisType,
      ai_service: aiService
    });
    
    return response.data;
  },
  
  analyzeMusicTheory: async (fileId: string, aiService?: string) => {
    const params: Record<string, string> = {};
    if (aiService) {
      params.ai_service = aiService;
    }
    
    const response = await apiClient.post(`/audio/analyze/music-theory/${fileId}`, {}, {
      params
    });
    
    return response.data;
  },
  
  analyzeProduction: async (fileId: string, aiService?: string) => {
    const params: Record<string, string> = {};
    if (aiService) {
      params.ai_service = aiService;
    }
    
    const response = await apiClient.post(`/audio/analyze/production/${fileId}`, {}, {
      params
    });
    
    return response.data;
  },
  
  analyzeArrangement: async (fileId: string, aiService?: string) => {
    const params: Record<string, string> = {};
    if (aiService) {
      params.ai_service = aiService;
    }
    
    const response = await apiClient.post(`/audio/analyze/arrangement/${fileId}`, {}, {
      params
    });
    
    return response.data;
  },
  
  getAnalysisResults: async (fileId: string) => {
    const response = await apiClient.get(`/audio/analysis/${fileId}`);
    return response.data;
  },
  
  deleteAudioFile: async (fileId: string) => {
    await apiClient.delete(`/audio/files/${fileId}`);
    return true;
  },
};

export default apiClient;
