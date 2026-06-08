<template>
  <div class="debug-view">
    <el-card shadow="never">
      <template #header>
        <span>接口调试</span>
      </template>
      <el-form label-width="100px" :model="form">
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="Service">
              <el-input v-model="activeService" placeholder="如: LuckyTurn" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Method">
              <el-input v-model="activeMethod" placeholder="如: LuckyTurnReward" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="numid">
              <el-input v-model="activeNumid" placeholder="用户 ID" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="areaid">
              <el-input v-model="activeAreaid" placeholder="区服 ID" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="请求体">
          <el-input
            v-model="form.body"
            type="textarea"
            :rows="6"
            placeholder='JSON 格式，如: {"current_count": 1}'
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSend">发送请求</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <ResponsePanel
      v-if="response"
      title="响应结果"
      :body="response.body"
      :elapsed-ms="response.elapsed_ms"
    />
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { sendSingle, type SingleResponse } from '@/api/request'
import { useConfigStore } from '@/stores/config'
import { useHistoryStore } from '@/stores/history'
import { ElMessage } from 'element-plus'
import ResponsePanel from '@/components/ResponsePanel.vue'

const configStore = useConfigStore()
const { activeNumid, activeAreaid, activeService, activeMethod } = storeToRefs(configStore)
const historyStore = useHistoryStore()

const form = reactive({
  body: '',
})

const loading = ref(false)
const response = ref<SingleResponse | null>(null)

onMounted(() => { configStore.load() })

async function handleSend() {
  if (!activeService.value || !activeMethod.value) {
    ElMessage.warning('请填写 Service 和 Method')
    return
  }

  let bodyObj: Record<string, any> = {}
  if (form.body.trim()) {
    try {
      bodyObj = JSON.parse(form.body)
    } catch {
      ElMessage.error('请求体 JSON 格式错误')
      return
    }
  }

  loading.value = true
  try {
    response.value = await sendSingle({
      server: configStore.server(),
      service: activeService.value,
      method: activeMethod.value,
      headers: { numid: activeNumid.value, areaid: activeAreaid.value },
      body: bodyObj,
    })
    historyStore.add({
      service: activeService.value,
      method: activeMethod.value,
      statusCode: response.value.status_code,
      elapsedMs: response.value.elapsed_ms,
    })
  } catch (e: any) {
    ElMessage.error(e.message || '请求失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.debug-view {
  max-width: 900px;
}
</style>
