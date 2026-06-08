<template>
  <div class="task-cmd-view">
    <el-card shadow="never">
      <template #header><span>任务推进</span></template>
      <el-form label-width="100px" :model="form">
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
        <el-form-item label="操作类型">
          <el-radio-group v-model="form.cmd">
            <el-radio value="finish">完成任务 (finish)</el-radio>
            <el-radio value="clear_data">清除数据 (clear_data)</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="任务 ID">
          <el-input
            v-model="form.taskIdsText"
            placeholder="多个 ID 用逗号分隔，如: 240,241,242"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleExecute">执行</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <ResponsePanel
      v-if="response"
      title="执行结果"
      :body="response.body"
      :elapsed-ms="response.elapsed_ms"
    />
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { taskCmd } from '@/api/mock'
import { useConfigStore } from '@/stores/config'
import { ElMessage } from 'element-plus'
import ResponsePanel from '@/components/ResponsePanel.vue'

const configStore = useConfigStore()
const { activeNumid, activeAreaid } = storeToRefs(configStore)

const form = reactive({
  cmd: 'finish',
  taskIdsText: '',
})

const loading = ref(false)
const response = ref<any>(null)

onMounted(() => { configStore.load() })

async function handleExecute() {
  if (!activeNumid.value) {
    ElMessage.warning('请填写用户 ID')
    return
  }

  const taskIds = form.taskIdsText
    .split(/[,，\s]+/)
    .map(s => parseInt(s.trim()))
    .filter(n => !isNaN(n))

  if (taskIds.length === 0) {
    ElMessage.warning('请输入至少一个任务 ID')
    return
  }

  loading.value = true
  try {
    response.value = await taskCmd({
      server: configStore.server(),
      numid: activeNumid.value,
      areaid: activeAreaid.value,
      cmd: form.cmd,
      task_id: taskIds,
    })
  } catch (e: any) {
    ElMessage.error(e.message || '请求失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.task-cmd-view {
  max-width: 800px;
}
</style>
