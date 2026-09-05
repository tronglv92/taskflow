/**
 * Axios API client.
 *
 * baseURL comes from VITE_API_URL (baked in at build time) and otherwise uses
 * the current browser origin. Callers provide their explicit ``/api/...``
 * paths, which Vite proxies to FastAPI without duplicating that prefix. A
 * request interceptor attaches the auth token; a response
 * interceptor clears it and redirects to /login on a 401.
 */

import axios from 'axios'

const apiClient = axios.create({
  // Keep the browser on the current origin in the Academy service tab.
  // Each store already requests /api/...; adding /api here would send the
  // backend the invalid /api/api/... path.
  baseURL: import.meta.env.VITE_API_URL || '',
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
