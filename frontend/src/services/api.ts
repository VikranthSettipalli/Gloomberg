import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 501) {
      console.warn('Endpoint not implemented:', error.config.url);
    }
    return Promise.reject(error);
  }
);

export default api;
