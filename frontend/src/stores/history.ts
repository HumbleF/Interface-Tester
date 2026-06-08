import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface HistoryItem {
  id: number
  time: string
  service: string
  method: string
  statusCode: number
  elapsedMs: number
}

export const useHistoryStore = defineStore('history', () => {
  const items = ref<HistoryItem[]>([])
  let nextId = 1

  function add(item: Omit<HistoryItem, 'id' | 'time'>) {
    items.value.unshift({
      ...item,
      id: nextId++,
      time: new Date().toLocaleTimeString('zh-CN'),
    })
    if (items.value.length > 50) items.value.pop()
  }

  function clear() {
    items.value = []
  }

  return { items, add, clear }
})
