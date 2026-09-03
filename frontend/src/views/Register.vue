<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const submitting = ref(false)

const submit = async () => {
  submitting.value = true
  try {
    await auth.register(email.value, password.value)
    router.push('/tasks')
  } catch (error) {
    // auth.error is set by the store
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="max-w-sm mx-auto bg-white shadow rounded-lg p-6 space-y-4">
    <h2 class="text-xl font-bold text-gray-900">Create an account</h2>
    <form class="space-y-3" @submit.prevent="submit">
      <input
        v-model="email"
        type="email"
        placeholder="Email"
        class="w-full border border-gray-300 rounded-md px-3 py-2"
      />
      <input
        v-model="password"
        type="password"
        placeholder="Password (min 8 characters)"
        class="w-full border border-gray-300 rounded-md px-3 py-2"
      />
      <button
        type="submit"
        class="w-full bg-blue-600 text-white rounded-md py-2 hover:bg-blue-700"
        :disabled="submitting"
      >
        Register
      </button>
      <p v-if="auth.error" class="text-sm text-red-600">{{ auth.error }}</p>
    </form>
    <p class="text-sm text-gray-500">
      Already have an account?
      <router-link to="/login" class="text-blue-600">Log in</router-link>
    </p>
  </div>
</template>
