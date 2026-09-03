/**
 * Pinia task store: the task list plus loading/error state and CRUD actions.
 * All API calls go through the shared axios client.
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient from '@/api/client'

export const useTaskStore = defineStore('tasks', () => {
  const tasks = ref([])
  const loading = ref(false)
  const error = ref(null)

  const completedTasks = computed(() =>
    tasks.value.filter((task) => task.is_completed)
  )

  async function fetchTasks() {
    loading.value = true
    error.value = null
    try {
      const response = await apiClient.get('/api/v1/tasks/')
      tasks.value = response.data
    } catch (e) {
      error.value = e.response?.data?.detail || e.message
    } finally {
      loading.value = false
    }
  }

  async function createTask(payload) {
    const response = await apiClient.post('/api/v1/tasks/', payload)
    tasks.value.push(response.data)
    return response.data
  }

  async function updateTask(id, updates) {
    const response = await apiClient.put(`/api/v1/tasks/${id}`, updates)
    const index = tasks.value.findIndex((t) => t.id === id)
    if (index !== -1) tasks.value[index] = response.data
    return response.data
  }

  async function deleteTask(id) {
    await apiClient.delete(`/api/v1/tasks/${id}`)
    tasks.value = tasks.value.filter((t) => t.id !== id)
  }

  return {
    tasks,
    loading,
    error,
    completedTasks,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask
  }
})
