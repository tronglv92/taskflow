<script setup>
import { ref } from 'vue'
import { useTaskStore } from '@/stores/tasks'

const props = defineProps({
  task: { type: Object, required: true }
})
const emit = defineEmits(['updated', 'deleted'])

const taskStore = useTaskStore()
const isUpdating = ref(false)

const toggleComplete = async () => {
  isUpdating.value = true
  try {
    await taskStore.updateTask(props.task.id, {
      is_completed: !props.task.is_completed
    })
    emit('updated')
  } catch (error) {
    console.error('Failed to update task:', error)
  } finally {
    isUpdating.value = false
  }
}

const remove = async () => {
  isUpdating.value = true
  try {
    await taskStore.deleteTask(props.task.id)
    emit('deleted')
  } catch (error) {
    console.error('Failed to delete task:', error)
  } finally {
    isUpdating.value = false
  }
}
</script>

<template>
  <div
    class="flex items-center justify-between border border-gray-200 rounded-lg px-4 py-3"
    :class="{ 'bg-gray-50': task.is_completed }"
  >
    <div>
      <p
        class="font-medium text-gray-900"
        :class="{ 'line-through text-gray-400': task.is_completed }"
      >
        {{ task.title }}
      </p>
      <p v-if="task.description" class="text-sm text-gray-500">
        {{ task.description }}
      </p>
      <span class="text-xs uppercase tracking-wide text-gray-400">
        {{ task.priority }}
      </span>
    </div>
    <div class="flex gap-2">
      <button
        class="text-sm px-3 py-1 rounded border border-gray-300 hover:bg-gray-100"
        :disabled="isUpdating"
        @click="toggleComplete"
      >
        {{ task.is_completed ? 'Reopen' : 'Complete' }}
      </button>
      <button
        class="text-sm px-3 py-1 rounded border border-red-200 text-red-600 hover:bg-red-50"
        :disabled="isUpdating"
        @click="remove"
      >
        Delete
      </button>
    </div>
  </div>
</template>
