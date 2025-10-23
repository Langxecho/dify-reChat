<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
    <div class="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
      <h1 class="text-3xl font-bold text-center mb-8 text-gray-800">注册账号</h1>

      <form @submit.prevent="handleRegister" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">邮箱</label>
          <input
            v-model="email"
            type="email"
            required
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
            placeholder="your@email.com"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">姓名（可选）</label>
          <input
            v-model="fullName"
            type="text"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
            placeholder="张三"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">密码</label>
          <input
            v-model="password"
            type="password"
            required
            minlength="6"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
            placeholder="至少6位"
          />
        </div>

        <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
        >
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>

      <p class="mt-6 text-center text-gray-600">
        已有账号？
        <router-link to="/login" class="text-blue-600 hover:underline">立即登录</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const fullName = ref('')
const loading = ref(false)
const error = ref('')

const handleRegister = async () => {
  loading.value = true
  error.value = ''

  try {
    await authStore.register(email.value, password.value, fullName.value || undefined)
    router.push('/')
  } catch (err: any) {
    error.value = err.response?.data?.detail || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>
