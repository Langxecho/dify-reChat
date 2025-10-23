import apiClient from './client'

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  full_name?: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export interface User {
  id: number
  email: string
  full_name: string | null
  is_active: boolean
  is_admin: boolean
  created_at: string
  updated_at: string
}

// 登录
export const login = async (data: LoginRequest): Promise<AuthResponse> => {
  const response = await apiClient.post<AuthResponse>('/auth/login', data)
  return response.data
}

// 注册
export const register = async (data: RegisterRequest): Promise<User> => {
  const response = await apiClient.post<User>('/auth/register', data)
  return response.data
}

// 获取当前用户信息
export const getCurrentUser = async (): Promise<User> => {
  const response = await apiClient.get<User>('/auth/me')
  return response.data
}
