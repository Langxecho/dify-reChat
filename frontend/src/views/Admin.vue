<template>
  <div class="min-h-screen bg-gray-100">
    <div class="max-w-4xl mx-auto py-12 px-4">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-2xl font-bold">管理后台</h1>
          <router-link to="/" class="text-blue-600 hover:underline">返回聊天</router-link>
        </div>

        <h2 class="text-lg font-semibold mb-4">Dify API 配置</h2>

        <form @submit.prevent="handleSave" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">API密钥</label>
            <input
              v-model="apiKey"
              type="text"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
              placeholder="sk-xxx"
            />
            <p class="text-xs text-gray-500 mt-1">请输入Dify工作流的API密钥</p>
          </div>

          <div v-if="message" :class="messageType === 'success' ? 'text-green-600' : 'text-red-600'" class="text-sm">
            {{ message }}
          </div>

          <div class="flex gap-2">
            <button
              type="submit"
              :disabled="loading"
              class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
            >
              {{ loading ? '保存中...' : '保存配置' }}
            </button>

            <button
              v-if="isConfigured"
              type="button"
              @click="handleDelete"
              :disabled="loading"
              class="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition disabled:opacity-50"
            >
              删除配置
            </button>
          </div>
        </form>

        <div v-if="isConfigured" class="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p class="text-green-800 text-sm">✓ API密钥已配置</p>
          <p class="text-green-600 text-xs mt-1">当前密钥: {{ apiKeyPreview }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import apiClient from '@/api/client'

const apiKey = ref('')
const loading = ref(false)
const message = ref('')
const messageType = ref<'success' | 'error'>('success')
const isConfigured = ref(false)
const apiKeyPreview = ref('')

const fetchConfig = async () => {
  try {
    const response = await apiClient.get('/admin/dify/config')
    isConfigured.value = response.data.is_configured
    apiKeyPreview.value = response.data.api_key_preview
  } catch (error) {
    console.error('Failed to fetch config:', error)
  }
}

const handleSave = async () => {
  loading.value = true
  message.value = ''

  try {
    await apiClient.post('/admin/dify/config', { api_key: apiKey.value })
    message.value = '配置保存成功！'
    messageType.value = 'success'
    apiKey.value = ''
    await fetchConfig()
  } catch (err: any) {
    message.value = err.response?.data?.detail || '保存失败'
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}

const handleDelete = async () => {
  if (!confirm('确定要删除API密钥配置吗？')) return

  loading.value = true
  message.value = ''

  try {
    await apiClient.delete('/admin/dify/config')
    message.value = '配置已删除'
    messageType.value = 'success'
    isConfigured.value = false
    apiKeyPreview.value = ''
  } catch (err: any) {
    message.value = err.response?.data?.detail || '删除失败'
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchConfig()
})
</script>
