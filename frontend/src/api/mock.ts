import http from '.'
import type { TargetServer } from './request'

export interface MockPurchaseParams {
  server: TargetServer
  numid: string
  areaid: string
  product_id: number
  event: number
}

export interface MockPurchaseResponse {
  success: boolean
  create_response: Record<string, any>
  delivery_response: Record<string, any>
  pre_order_no: string
  error: string
}

export interface TaskCmdParams {
  server: TargetServer
  numid: string
  areaid: string
  cmd: string
  task_id: number[]
}

export function mockPurchase(params: MockPurchaseParams): Promise<MockPurchaseResponse> {
  return http.post('/mock/purchase', params)
}

export function taskCmd(params: TaskCmdParams): Promise<any> {
  return http.post('/mock/task-cmd', params)
}
