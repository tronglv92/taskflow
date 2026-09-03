/**
 * Pinia auth store: holds the current user and JWT token.
 * The token is persisted to localStorage so a page refresh keeps the session.
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient from '@/api/client'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('auth_token') || null)
  const user = ref(null)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  function setToken(value) {
    token.value = value
    if (value) {
      localStorage.setItem('auth_token', value)
    } else {
      localStorage.removeItem('auth_token')
    }
  }

  async function login(email, password) {
    error.value = null
    // OAuth2 password flow expects form-encoded username/password.
    const body = new URLSearchParams({ username: email, password })
    try {
      const response = await apiClient.post('/api/auth/token', body, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      })
      setToken(response.data.access_token)
      user.value = { email }
    } catch (e) {
      error.value = e.response?.data?.detail || 'Login failed'
      throw e
    }
  }

  async function register(email, password) {
    error.value = null
    try {
      await apiClient.post('/api/auth/register', { email, password })
      await login(email, password)
    } catch (e) {
      error.value = e.response?.data?.detail || 'Registration failed'
      throw e
    }
  }

  function logout() {
    setToken(null)
    user.value = null
  }

  return { token, user, error, isAuthenticated, login, register, logout }
})
