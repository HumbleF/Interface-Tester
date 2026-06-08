<template>
  <div class="mock-purchase-view">
    <el-card shadow="never">
      <template #header><span>模拟充值</span></template>
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
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="商品 ID">
              <el-input-number v-model="form.productId" :min="1" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="事件类型">
              <el-select v-model="form.event" style="width: 100%">
                <el-option :value="1" label="1 - 普通购买" />
                <el-option :value="2" label="2 - 订阅" />
                <el-option :value="3" label="3 - 促销" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handlePurchase">执行充值</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card v-if="result" shadow="never" style="margin-top: 16px">
      <template #header>
        <div class="response-header">
          <span>充值结果</span>
          <el-tag :type="result.success ? 'success' : 'danger'" size="small">
            {{ result.success ? '成功' : '失败' }}
          </el-tag>
        </div>
      </template>
      <el-descriptions :column="1" border size="small">
        <el-descriptions-item label="订单号">{{ result.pre_order_no || '-' }}</el-descriptions-item>
        <el-descriptions-item v-if="result.error" label="错误">
          <span class="error-text">{{ result.error }}</span>
        </el-descriptions-item>
      </el-descriptions>
      <el-collapse style="margin-top: 12px">
        <el-collapse-item title="RechargeCreate 响应">
          <pre class="json-body">{{ JSON.stringify(result.create_response, null, 2) }}</pre>
        </el-collapse-item>
        <el-collapse-item title="RechargeDelivery 响应">
          <pre class="json-body">{{ JSON.stringify(result.delivery_response, null, 2) }}</pre>
        </el-collapse-item>
      </el-collapse>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { mockPurchase, type MockPurchaseResponse } from '@/api/mock'
import { useConfigStore } from '@/stores/config'
import { ElMessage } from 'element-plus'

const configStore = useConfigStore()
const { activeNumid, activeAreaid } = storeToRefs(configStore)

const form = reactive({
  productId: 80001,
  event: 1,
})

const loading = ref(false)
const result = ref<MockPurchaseResponse | null>(null)

onMounted(() => { configStore.load() })

async function handlePurchase() {
  if (!activeNumid.value) {
    ElMessage.warning('请填写用户 ID')
    return
  }

  loading.value = true
  try {
    result.value = await mockPurchase({
      server: configStore.server(),
      numid: activeNumid.value,
      areaid: activeAreaid.value,
      product_id: form.productId,
      event: form.event,
    })
  } catch (e: any) {
    ElMessage.error(e.message || '请求失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.mock-purchase-view {
  max-width: 800px;
}
.response-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.error-text {
  color: #f56c6c;
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
  max-height: 400px;
  overflow-y: auto;
}
</style>
