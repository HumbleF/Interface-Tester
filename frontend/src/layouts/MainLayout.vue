<template>
  <el-container class="layout-container">
    <el-aside width="180px" class="layout-aside">
      <div class="logo">接口测试工具</div>
      <el-menu
        :default-active="route.path"
        router
        class="layout-menu"
      >
        <el-menu-item index="/debug">
          <el-icon><Connection /></el-icon>
          <span>接口调试</span>
        </el-menu-item>
        <el-menu-item index="/concurrent">
          <el-icon><Operation /></el-icon>
          <span>并发测试</span>
        </el-menu-item>
        <el-menu-item index="/mock-purchase">
          <el-icon><ShoppingCart /></el-icon>
          <span>模拟充值</span>
        </el-menu-item>
        <el-menu-item index="/task-cmd">
          <el-icon><Finished /></el-icon>
          <span>任务推进</span>
        </el-menu-item>
        <el-menu-item index="/config">
          <el-icon><Setting /></el-icon>
          <span>系统配置</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main class="layout-main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { Connection, Operation, ShoppingCart, Finished, Setting } from '@element-plus/icons-vue'

const route = useRoute()
</script>

<style scoped>
.layout-container {
  height: 100vh;
}
.layout-aside {
  background: #304156;
  overflow: hidden;
}
.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  border-bottom: 1px solid #3d4a5a;
}
.layout-menu {
  border-right: none;
  background: #304156;
}
.layout-menu .el-menu-item {
  color: #bfcbd9;
}
.layout-menu .el-menu-item:hover,
.layout-menu .el-menu-item.is-active {
  background: #263445;
  color: #409eff;
}
.layout-main {
  background: #f0f2f5;
  padding: 20px;
}
</style>
