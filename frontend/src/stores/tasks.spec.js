import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

vi.mock('@/api/client', () => ({
  default: {
    get: vi.fn(() =>
      Promise.resolve({
        data: [
          { id: 1, title: 'a', is_completed: false },
          { id: 2, title: 'b', is_completed: true }
        ]
      })
    )
  }
}))

import { useTaskStore } from '@/stores/tasks'

describe('task store', () => {
  beforeEach(() => setActivePinia(createPinia()))

  it('fetchTasks populates tasks and computes completedTasks', async () => {
    const store = useTaskStore()
    await store.fetchTasks()
    expect(store.tasks).toHaveLength(2)
    expect(store.completedTasks).toHaveLength(1)
    expect(store.loading).toBe(false)
  })
})
