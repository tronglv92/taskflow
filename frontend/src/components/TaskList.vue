<script setup>
import { ref, computed } from 'vue'
import { useTaskStore } from '@/stores/tasks'
import TaskCard from '@/components/TaskCard.vue'

const taskStore = useTaskStore()
const filter = ref('all')

const filteredTasks = computed(() => {
  if (filter.value === 'completed') {
    return taskStore.tasks.filter((t) => t.is_completed)
  }
  if (filter.value === 'active') {
    return taskStore.tasks.filter((t) => !t.is_completed)
  }
  return taskStore.tasks
})
</script>

<template>
  <div class="space-y-3">
    <div class="flex items-center gap-2">
      <label class="text-sm text-gray-600">Show</label>
      <select v-model="filter" class="border border-gray-300 rounded-md px-2 py-1 text-sm">
        <option value="all">All</option>
        <option value="active">Active</option>
        <option value="completed">Completed</option>
      </select>
    </div>

    <p v-if="taskStore.loading" class="text-gray-500">Loading tasks...</p>
    <p v-else-if="taskStore.error" class="text-red-600">{{ taskStore.error }}</p>
    <p v-else-if="filteredTasks.length === 0" class="text-gray-500">No tasks yet.</p>

    <TaskCard
      v-for="task in filteredTasks"
      :key="task.id"
      :task="task"
      @updated="taskStore.fetchTasks"
      @deleted="taskStore.fetchTasks"
    />
  </div>
</template>
