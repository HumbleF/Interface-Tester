import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      redirect: '/debug',
      children: [
        { path: 'debug', name: 'debug', component: () => import('@/views/DebugView.vue'), meta: { title: '接口调试' } },
        { path: 'concurrent', name: 'concurrent', component: () => import('@/views/ConcurrentView.vue'), meta: { title: '并发测试' } },
        { path: 'mock-purchase', name: 'mockPurchase', component: () => import('@/views/MockPurchaseView.vue'), meta: { title: '模拟充值' } },
        { path: 'task-cmd', name: 'taskCmd', component: () => import('@/views/TaskCmdView.vue'), meta: { title: '任务推进' } },
        { path: 'config', name: 'config', component: () => import('@/views/ConfigView.vue'), meta: { title: '系统配置' } },
      ],
    },
  ],
})

export default router
