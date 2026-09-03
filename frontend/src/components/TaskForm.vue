<script setup>
import { ref } from 'vue'
import { useTaskStore } from '@/stores/tasks'

const emit = defineEmits(['created'])

const taskStore = useTaskStore()
const title = ref('')
const priority = ref('medium')
const submitting = ref(false)
const formError = ref(null)

const submit = async () => {
  if (!title.value.trim()) {
    formError.value = 'Title is required'
    return
  }
  submitting.value = true
  formError.value = null
  try {
    await taskStore.createTask({ title: title.value.trim(), priority: priority.value })
    title.value = ''
    priority.value = 'medium'
    emit('created')
  } catch (error) {
    formError.value = error.response?.data?.detail || 'Could not create task'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <form class="flex flex-wrap items-end gap-3" @submit.prevent="submit">
    <div class="flex-1 min-w-[12rem]">
      <label class="block text-sm font-medium text-gray-700">Title</label>
      <input
        v-model="title"
        type="text"
        class="mt-1 w-full border border-gray-300 rounded-md px-3 py-2"
        placeholder="What needs doing?"
      />
    </div>
    <div>
      <label class="block text-sm font-medium text-gray-700">Priority</label>
      <select
        v-model="priority"
        class="mt-1 border border-gray-300 rounded-md px-3 py-2"
      >
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
    </div>
    <button
      type="submit"
      class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
      :disabled="submitting"
    >
      Add Task
    </button>
    <p v-if="formError" class="w-full text-sm text-red-600">{{ formError }}</p>
  </form>
</template>
