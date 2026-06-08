import http from '.'

export interface UserConfig {
  server_host: string
  server_port: number
  areaid: string
  user_ids: string[]
}

export function loadConfig(): Promise<UserConfig> {
  return http.get('/config/load')
}

export function saveConfig(config: UserConfig): Promise<any> {
  return http.post('/config/save', config)
}

export interface HealthCheckResult {
  reachable: boolean
  detail: string
}

export function healthCheck(host: string, port: number): Promise<HealthCheckResult> {
  return http.post('/config/health-check', { host, port })
}
