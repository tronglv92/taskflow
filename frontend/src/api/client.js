/**
 * Axios API client.
 *
 * baseURL comes from VITE_API_URL (baked in at build time) and falls back to
 * the relative ``/api`` path in development. Vite proxies that path to the
 * FastAPI server, so the browser talks only to the Vite origin instead of its
 * own localhost. A request interceptor attaches the auth token; a response
 * interceptor clears it and redirects to /login on a 401.
 */

import axios from 'axios'

const apiClient = axios.create({
  // A relative fallback is essential when Vite is opened through the Academy
  // service tab: ``localhost`` there means the learner's browser, not the VM.
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token')
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient
