import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as authApi from '@/api/auth'
import type { User } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('access_token'))

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_admin ?? false)

  // Actions
  const login = async (email: string, password: string) => {
    try {
      const response = await authApi.login({ email, password })
      token.value = response.access_token
      localStorage.setItem('access_token', response.access_token)

      // 获取用户信息
      await fetchUser()

      return true
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }

  const register = async (email: string, password: string, fullName?: string) => {
    try {
      await authApi.register({ email, password, full_name: fullName })
      // 注册成功后自动登录
      await login(email, password)
      return true
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
  }

  const fetchUser = async () => {
    try {
      user.value = await authApi.getCurrentUser()
    } catch (error) {
      console.error('Failed to fetch user:', error)
      logout()
      throw error
    }
  }

  // 初始化时获取用户信息
  if (token.value) {
    fetchUser().catch(() => {
      // 如果获取失败，清除token
      logout()
    })
  }

  return {
    user,
    token,
    isAuthenticated,
    isAdmin,
    login,
    register,
    logout,
    fetchUser
  }
})
