import axios from 'axios';

const rawUrl = import.meta.env.VITE_API_URL || import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
const API_BASE_URL = rawUrl.endsWith('/api') ? rawUrl : `${rawUrl.replace(/\/$/, '')}/api`;

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 45000,
});

export const postApi = {
  generatePost: async (payload) => {
    console.log('Request sent to backend (/generate):', payload);
    const { data } = await client.post('/generate', payload);
    return data;
  },

  analyzeQuality: async (payload) => {
    const { data } = await client.post('/analyze', payload);
    return data;
  },

  analyzeStyle: async (payload) => {
    const { data } = await client.post('/analyze-style', payload);
    return data;
  },

  rewritePost: async (payload) => {
    const { data } = await client.post('/rewrite', payload);
    return data;
  },

  improveHook: async (payload) => {
    const { data } = await client.post('/improve-hook', payload);
    return data;
  },

  humanizePost: async (payload) => {
    const { data } = await client.post('/humanize', payload);
    return data;
  },

  shortenPost: async (payload) => {
    const { data } = await client.post('/shorten', payload);
    return data;
  },

  checkHealth: async () => {
    const { data } = await client.get('/health');
    return data;
  },

  // Persistent History APIs
  listHistory: async (params = {}) => {
    const { data } = await client.get('/history', { params });
    return data;
  },

  getHistoryItem: async (id) => {
    const { data } = await client.get(`/history/${id}`);
    return data;
  },

  deleteHistoryItem: async (id) => {
    const { data } = await client.delete(`/history/${id}`);
    return data;
  },

  clearAllHistory: async () => {
    const { data } = await client.delete('/history');
    return data;
  },

  exportHistoryExcel: async () => {
    const response = await client.get('/history/export', {
      responseType: 'blob',
    });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;

    const now = new Date();
    const pad = (n) => String(n).padStart(2, '0');
    const defaultTs = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}_${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`;
    let filename = `writeflow_history_export_${defaultTs}.xlsx`;

    const cdHeader = response.headers['content-disposition'];
    if (cdHeader) {
      const match = cdHeader.match(/filename="?([^";]+)"?/);
      if (match && match[1]) {
        filename = match[1];
      }
    }

    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  },



  // Backward compatibility aliases
  listPosts: async (skip = 0, limit = 50) => {
    const { data } = await client.get('/history', { params: { skip, limit } });
    return data;
  },

  deletePost: async (id) => {
    const { data } = await client.delete(`/history/${id}`);
    return data;
  }
};
