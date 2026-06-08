<template>
  <div class="config-view">
    <el-card shadow="never">
      <template #header><span>系统配置</span></template>
      <el-form label-width="120px" :model="configStore">
        <el-form-item label="服务器地址">
          <el-input v-model="configStore.serverHost" placeholder="127.0.0.1" style="width: 200px" />
        </el-form-item>
        <el-form-item label="服务器端口">
          <el-input-number v-model="configStore.serverPort" :min="1" :max="65535" />
          <el-button
            :type="testResult === null ? 'info' : testResult ? 'success' : 'danger'"
            :loading="testing"
            style="margin-left: 12px"
            @click="handleTestConnection"
          >
            测试连接
          </el-button>
        </el-form-item>
        <el-form-item label="默认区服 ID">
          <el-input v-model="configStore.areaid" placeholder="5016" style="width: 200px" />
        </el-form-item>
        <el-form-item label="常用用户 ID">
          <div class="user-ids-area">
            <div v-for="(id, index) in configStore.userIds" :key="index" class="user-id-row">
              <el-input v-model="configStore.userIds[index]" size="small" style="width: 200px" />
              <el-button type="danger" size="small" text @click="removeUserId(index)">删除</el-button>
            </div>
            <el-button type="primary" size="small" text @click="addUserId">+ 添加用户 ID</el-button>
          </div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="saving" @click="handleSave">保存配置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useConfigStore } from '@/stores/config'
import { healthCheck } from '@/api/config'
import { ElMessage } from 'element-plus'

const configStore = useConfigStore()
const saving = ref(false)
const testing = ref(false)
const testResult = ref<boolean | null>(null)

onMounted(() => {
  configStore.load()
})

function addUserId() {
  configStore.userIds.push('')
}

function removeUserId(index: number) {
  configStore.userIds.splice(index, 1)
}

async function handleTestConnection() {
  testing.value = true
  testResult.value = null
  try {
    const res = await healthCheck(configStore.serverHost, configStore.serverPort)
    testResult.value = res.reachable
    if (res.reachable) {
      ElMessage.success('服务端连接正常')
    } else {
      ElMessage.error(`无法连接服务端: ${res.detail}`)
    }
  } catch (e: any) {
    testResult.value = false
    ElMessage.error(e.message || '测试请求失败')
  } finally {
    testing.value = false
  }
}

async function handleSave() {
  saving.value = true
  try {
    await configStore.save()
    ElMessage.success('配置已保存')
  } catch (e: any) {
    ElMessage.error(e.message || '保存失败')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.config-view {
  max-width: 600px;
}
.user-ids-area {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.user-id-row {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
