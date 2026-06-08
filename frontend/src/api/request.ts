import http from '.'

export interface TargetServer {
  host: string
  port: number
}

export interface SingleRequestParams {
  server: TargetServer
  service: string
  method: string
  headers: Record<string, string>
  body: Record<string, any>
}

export interface SingleResponse {
  status_code: number
  body: Record<string, any>
  elapsed_ms: number
}

export interface ConcurrentRequestParams {
  server: TargetServer
  service: string
  method: string
  user_ids: string[]
  areaid: string
  body: Record<string, any>
}

export interface ConcurrentResponseItem {
  numid: string
  status_code: number
  body: Record<string, any>
  elapsed_ms: number
  error: string
}

export interface ConcurrentResponse {
  total: number
  results: ConcurrentResponseItem[]
  total_elapsed_ms: number
}

export function sendSingle(params: SingleRequestParams): Promise<SingleResponse> {
  return http.post('/request/send', params)
}

export function sendConcurrent(params: ConcurrentRequestParams): Promise<ConcurrentResponse> {
  return http.post('/request/concurrent', params)
}
