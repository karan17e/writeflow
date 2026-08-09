import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 45000,
});

export const postApi = {
  generatePost: async (payload) => {
    console.log('2. Request sent to backend (/generate):', payload);
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
  }
};
