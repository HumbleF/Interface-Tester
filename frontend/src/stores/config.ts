import { defineStore } from 'pinia'
import { ref } from 'vue'
import { loadConfig, saveConfig, type UserConfig } from '@/api/config'

export const useConfigStore = defineStore('config', () => {
  const serverHost = ref('121.36.244.219')
  const serverPort = ref(14354)
  const areaid = ref('5016')
  const userIds = ref<string[]>(['300231159'])

  const activeNumid = ref('300231159')
  const activeAreaid = ref('5016')
  const activeService = ref('')
  const activeMethod = ref('')

  const server = () => ({ host: serverHost.value, port: serverPort.value })

  async function load() {
    const data = await loadConfig()
    serverHost.value = data.server_host
    serverPort.value = data.server_port
    areaid.value = data.areaid
    userIds.value = data.user_ids
    if (!activeNumid.value) {
      activeNumid.value = data.user_ids[0] || ''
    }
    if (!activeAreaid.value) {
      activeAreaid.value = data.areaid
    }
  }

  async function save() {
    await saveConfig({
      server_host: serverHost.value,
      server_port: serverPort.value,
      areaid: areaid.value,
      user_ids: userIds.value,
    })
  }

  return { serverHost, serverPort, areaid, userIds, activeNumid, activeAreaid, activeService, activeMethod, server, load, save }
})
