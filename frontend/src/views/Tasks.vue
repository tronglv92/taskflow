<script setup>
import { onMounted } from 'vue'
import { useTaskStore } from '@/stores/tasks'
import TaskList from '@/components/TaskList.vue'
import TaskForm from '@/components/TaskForm.vue'

const taskStore = useTaskStore()

onMounted(() => {
  taskStore.fetchTasks()
})
</script>

<template>
  <div class="tasks">
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6 space-y-6">
        <h2 class="text-2xl font-bold text-gray-900">Tasks</h2>
        <TaskForm @created="taskStore.fetchTasks" />
        <TaskList />
      </div>
    </div>
  </div>
</template>
