<template>
  <div class="concurrent-view">
    <el-card shadow="never">
      <template #header><span>并发测试</span></template>
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
        <el-form-item label="areaid">
          <el-input v-model="activeAreaid" placeholder="区服 ID" />
        </el-form-item>
        <el-form-item label="用户 ID">
          <el-input
            v-model="form.userIdsText"
            type="textarea"
            :rows="3"
            placeholder="每行一个用户 ID，或用逗号分隔"
          />
        </el-form-item>
        <el-form-item label="请求体">
          <el-input
            v-model="form.body"
            type="textarea"
            :rows="4"
            placeholder='JSON 格式，如: {"current_count": 1}'
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSend">并发发送</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card v-if="result" shadow="never" style="margin-top: 16px">
      <template #header>
        <div class="response-header">
          <span>并发结果</span>
          <span class="response-meta">
            <el-tag type="info" size="small">共 {{ result.total }} 个</el-tag>
            <el-tag type="success" size="small">成功 {{ successCount }}</el-tag>
            <el-tag v-if="failCount > 0" type="danger" size="small">失败 {{ failCount }}</el-tag>
            <el-tag type="info" size="small">总耗时 {{ result.total_elapsed_ms }}ms</el-tag>
          </span>
        </div>
      </template>
      <el-table :data="result.results" stripe size="small">
        <el-table-column prop="numid" label="用户 ID" width="120" />
        <el-table-column prop="status_code" label="状态码" width="80">
          <template #default="{ row }">
            <el-tag :type="row.body?.code === 0 ? 'success' : 'danger'" size="small">
              {{ row.body?.code ?? row.status_code }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="elapsed_ms" label="耗时(ms)" width="100" />
        <el-table-column label="响应/错误">
          <template #default="{ row }">
            <span v-if="row.error" class="error-text">{{ row.error }}</span>
            <span v-else>{{ JSON.stringify(row.body) }}</span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { sendConcurrent, type ConcurrentResponse } from '@/api/request'
import { useConfigStore } from '@/stores/config'
import { ElMessage } from 'element-plus'

const configStore = useConfigStore()
const { activeAreaid, activeService, activeMethod } = storeToRefs(configStore)

const form = reactive({
  userIdsText: '',
  body: '',
})

const loading = ref(false)
const result = ref<ConcurrentResponse | null>(null)

const successCount = computed(() => result.value?.results.filter(r => r.body?.code === 0).length ?? 0)
const failCount = computed(() => result.value?.results.filter(r => r.body?.code !== 0).length ?? 0)

onMounted(async () => {
  await configStore.load()
  form.userIdsText = configStore.userIds.join('\n')
})

async function handleSend() {
  if (!activeService.value || !activeMethod.value) {
    ElMessage.warning('请填写 Service 和 Method')
    return
  }

  const userIds = form.userIdsText
    .split(/[\n,]+/)
    .map(s => s.trim())
    .filter(Boolean)

  if (userIds.length === 0) {
    ElMessage.warning('请输入至少一个用户 ID')
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
    result.value = await sendConcurrent({
      server: configStore.server(),
      service: activeService.value,
      method: activeMethod.value,
      user_ids: userIds,
      areaid: activeAreaid.value,
      body: bodyObj,
    })
  } catch (e: any) {
    ElMessage.error(e.message || '请求失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.concurrent-view {
  max-width: 1000px;
}
.response-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.response-meta {
  display: flex;
  gap: 8px;
}
.error-text {
  color: #f56c6c;
  font-size: 12px;
}
</style>
