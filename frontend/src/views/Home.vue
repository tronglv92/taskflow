<template>
  <div class="home">
    <!-- Hero Section -->
    <div class="bg-white">
      <div class="max-w-7xl mx-auto py-16 px-4 sm:py-24 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1 class="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight lg:text-6xl">
            Welcome to TaskFlow
          </h1>
          <p class="mt-4 max-w-2xl mx-auto text-xl text-gray-500">
            A modern task management platform built throughout the Platform Engineering Bootcamp
          </p>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="py-12 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h2 class="text-3xl font-extrabold text-gray-900">
            Built with Modern Technologies
          </h2>
          <p class="mt-4 text-lg text-gray-500">
            Learn platform engineering by building a real application
          </p>
        </div>

        <div class="mt-10">
          <div class="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            <!-- Feature 1 -->
            <div class="bg-white overflow-hidden shadow rounded-lg">
              <div class="p-6">
                <h3 class="text-lg font-medium text-gray-900">FastAPI Backend</h3>
                <p class="mt-2 text-sm text-gray-500">
                  Modern Python backend with automatic API documentation
                </p>
              </div>
            </div>

            <!-- Feature 2 -->
            <div class="bg-white overflow-hidden shadow rounded-lg">
              <div class="p-6">
                <h3 class="text-lg font-medium text-gray-900">Vue.js Frontend</h3>
                <p class="mt-2 text-sm text-gray-500">
                  Reactive frontend with Pinia state management
                </p>
              </div>
            </div>

            <!-- Feature 3 -->
            <div class="bg-white overflow-hidden shadow rounded-lg">
              <div class="p-6">
                <h3 class="text-lg font-medium text-gray-900">Cloud Native</h3>
                <p class="mt-2 text-sm text-gray-500">
                  Containerized and ready for Kubernetes deployment
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- API Status Section -->
    <div class="bg-white py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h2 class="text-2xl font-bold text-gray-900 mb-8">API Status</h2>

          <div v-if="apiStatus" class="inline-block bg-gray-50 rounded-lg p-6 text-left">
            <div class="space-y-2">
              <p>
                <span class="font-semibold">Status:</span>
                <span class="ml-2 text-green-600">{{ apiStatus.status }}</span>
              </p>
              <p>
                <span class="font-semibold">API Version:</span>
                <span class="ml-2">{{ apiStatus.api_version }}</span>
              </p>
              <p>
                <span class="font-semibold">Environment:</span>
                <span class="ml-2">{{ apiStatus.environment }}</span>
              </p>
            </div>
          </div>

          <p v-else-if="error" class="text-red-600">
            {{ error }}
          </p>

          <p v-else class="text-gray-500">Loading API status...</p>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="bg-blue-600">
      <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8 lg:flex lg:items-center lg:justify-between">
        <h2 class="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
          <span class="block">Ready to get started?</span>
          <span class="block text-blue-200">View your tasks now.</span>
        </h2>
        <div class="mt-8 flex lg:mt-0 lg:flex-shrink-0">
          <div class="inline-flex rounded-md shadow">
            <router-link
              to="/tasks"
              class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-blue-600 bg-white hover:bg-blue-50"
            >
              View Tasks
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/client'

const apiStatus = ref(null)
const error = ref(null)

// Use the shared client so this request follows Vite's /api development proxy
// and receives the same auth/error behavior as every other frontend request.
onMounted(async () => {
  try {
    const response = await apiClient.get('/api/v1/status')
    apiStatus.value = response.data
  } catch (err) {
    error.value = 'Unable to connect to the backend API. Confirm the Backend Server terminal is still running.'
    console.error('API Error:', err)
  }
})
</script>
