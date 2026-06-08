<template>
  <el-card shadow="never" class="response-panel" :class="`is-${status}`">
    <template #header>
      <div class="panel-header">
        <span class="panel-title">{{ title }}</span>
        <div class="panel-meta">
          <el-tag :type="statusTagType" size="small" effect="dark">
            {{ statusLabel }}
          </el-tag>
          <el-tag v-if="elapsedMs != null" type="info" size="small">{{ elapsedMs }}ms</el-tag>
          <el-button size="small" text @click="handleCopy">
            <el-icon><DocumentCopy /></el-icon> 复制
          </el-button>
        </div>
      </div>
    </template>

    <!-- 摘要区域 -->
    <div v-if="summary" class="response-summary" :class="`summary-${status}`">
      <div v-if="body?.message" class="summary-row">
        <span class="summary-label">message:</span>
        <span class="summary-value">{{ body.message || '(空)' }}</span>
      </div>
      <div v-if="dataResult" class="summary-row summary-result">
        <span class="summary-label">result:</span>
        <span class="summary-value">{{ dataResult }}</span>
      </div>
      <div v-if="status === 'warning'" class="summary-row summary-hint">
        <span class="summary-value hint-text">code=0 但业务执行异常，请检查 result 内容</span>
      </div>
    </div>

    <!-- JSON 详情 -->
    <div class="json-container">
      <div class="json-toolbar">
        <el-button-group size="small">
          <el-button :type="expanded ? '' : 'primary'" text @click="expanded = false">收起</el-button>
          <el-button :type="expanded ? 'primary' : ''" text @click="expanded = true">展开</el-button>
        </el-button-group>
      </div>
      <pre class="json-body" :class="{ collapsed: !expanded }">{{ formattedJson }}</pre>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { DocumentCopy } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const props = withDefaults(defineProps<{
  title?: string
  body: any
  elapsedMs?: number | null
  summary?: boolean
}>(), {
  title: '响应结果',
  elapsedMs: null,
  summary: true,
})

const expanded = ref(true)

const bodyCode = computed(() => props.body?.code ?? '?')

const dataResult = computed(() => {
  const d = props.body?.data
  if (!d) return null
  if (typeof d.result === 'string') return d.result
  return null
})

const hasDataError = computed(() => {
  const r = dataResult.value
  if (!r) return false
  return r.includes('error') || r.includes('Error') || r.includes('未开启') || r.includes('失败')
})

const status = computed<'success' | 'warning' | 'error'>(() => {
  if (props.body?.code !== 0) return 'error'
  if (hasDataError.value) return 'warning'
  return 'success'
})

const statusTagType = computed(() => {
  if (status.value === 'success') return 'success'
  if (status.value === 'warning') return 'warning'
  return 'danger'
})

const statusLabel = computed(() => {
  if (status.value === 'success') return '执行成功'
  if (status.value === 'warning') return '业务异常'
  return `code: ${bodyCode.value}`
})

const formattedJson = computed(() => JSON.stringify(props.body, null, 2))

function handleCopy() {
  navigator.clipboard.writeText(formattedJson.value)
  ElMessage.success('已复制到剪贴板')
}
</script>

<style scoped>
.response-panel {
  margin-top: 16px;
  border-left: 3px solid var(--el-color-info-light-5);
}
.response-panel.is-success {
  border-left-color: var(--el-color-success);
}
.response-panel.is-warning {
  border-left-color: var(--el-color-warning);
}
.response-panel.is-error {
  border-left-color: var(--el-color-danger);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.panel-title {
  font-weight: 600;
}
.panel-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.response-summary {
  background: var(--el-fill-color-lighter);
  border-radius: 6px;
  padding: 12px 16px;
  margin-bottom: 12px;
  font-size: 13px;
}
.summary-row {
  display: flex;
  align-items: baseline;
  gap: 8px;
  line-height: 1.8;
}
.summary-label {
  color: var(--el-text-color-secondary);
  font-weight: 500;
  flex-shrink: 0;
}
.summary-value {
  color: var(--el-text-color-primary);
  word-break: break-all;
}
.summary-warning {
  border-left: 3px solid var(--el-color-warning);
  padding-left: 13px;
}
.summary-result .summary-value {
  font-family: 'Consolas', monospace;
  font-size: 12.5px;
}
.is-warning .summary-result .summary-value {
  color: var(--el-color-warning-dark-2);
  font-weight: 500;
}
.hint-text {
  color: var(--el-text-color-secondary);
  font-size: 12px;
  font-style: italic;
}

.json-container {
  position: relative;
}
.json-toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 4px;
}
.json-body {
  background: #1a1a2e;
  color: #e0e0e0;
  padding: 16px;
  border-radius: 8px;
  font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
  font-size: 12.5px;
  line-height: 1.6;
  overflow-x: auto;
  margin: 0;
  max-height: 500px;
  overflow-y: auto;
}
.json-body.collapsed {
  max-height: 120px;
  overflow-y: hidden;
  mask-image: linear-gradient(to bottom, black 60%, transparent 100%);
  -webkit-mask-image: linear-gradient(to bottom, black 60%, transparent 100%);
}
</style>
