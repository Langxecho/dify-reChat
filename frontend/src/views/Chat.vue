<template>
  <div class="flex h-screen bg-gray-100">
    <!-- 左侧对话列表 -->
    <div class="w-64 bg-gray-900 text-white flex flex-col">
      <div class="p-4 border-b border-gray-700">
        <button
          @click="chatStore.newConversation()"
          class="w-full bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition"
        >
          + 新对话
        </button>
      </div>

      <!-- 对话列表 -->
      <div class="flex-1 overflow-y-auto">
        <div
          v-for="conv in chatStore.conversations"
          :key="conv.id"
          @click="chatStore.selectConversation(conv.id)"
          class="p-4 hover:bg-gray-800 cursor-pointer transition"
          :class="{ 'bg-gray-800': chatStore.currentConversation?.id === conv.id }"
        >
          <div class="text-sm truncate">{{ conv.title }}</div>
          <div class="text-xs text-gray-400 mt-1">
            {{ new Date(conv.updated_at).toLocaleDateString() }}
          </div>
        </div>
      </div>

      <!-- 用户信息 -->
      <div class="p-4 border-t border-gray-700">
        <div class="text-sm mb-2">{{ authStore.user?.email }}</div>
        <div class="flex gap-2">
          <router-link
            v-if="authStore.isAdmin"
            to="/admin"
            class="text-xs text-blue-400 hover:underline"
          >
            管理
          </router-link>
          <button @click="authStore.logout(); $router.push('/login')" class="text-xs text-red-400 hover:underline">
            退出
          </button>
        </div>
      </div>
    </div>

    <!-- 工作区侧边栏 -->
    <div class="w-80 bg-white border-r border-gray-200 flex flex-col">
      <div class="p-4 border-b border-gray-200">
        <h2 class="text-lg font-semibold text-gray-900">工作区</h2>
        <p class="text-sm text-gray-500 mt-1">选择一个工作流开始对话</p>
      </div>

      <!-- 工作流分类标签 -->
      <div class="p-3 border-b border-gray-200">
        <div class="flex gap-2 overflow-x-auto">
          <button
            v-for="category in workflowCategories"
            :key="category.name"
            @click="selectedCategory = category.name"
            class="px-3 py-1 text-sm rounded-full whitespace-nowrap transition"
            :class="selectedCategory === category.name ? 'bg-blue-100 text-blue-700 border border-blue-300' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
          >
            {{ category.name }}
          </button>
        </div>
      </div>

      <!-- 工作流列表 -->
      <div class="flex-1 overflow-y-auto">
        <div
          v-for="workflow in filteredWorkflows"
          :key="workflow.id"
          @click="selectWorkflow(workflow)"
          class="p-4 border-b border-gray-100 hover:bg-gray-50 cursor-pointer transition"
          :class="{ 'bg-blue-50 border-blue-200': selectedWorkflow?.id === workflow.id }"
        >
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0">
              <div v-if="workflow.icon" class="w-8 h-8 bg-gray-200 rounded-md flex items-center justify-center">
                <span class="text-xs">{{ workflow.icon }}</span>
              </div>
              <div v-else class="w-8 h-8 bg-gray-200 rounded-md flex items-center justify-center">
                <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
                </svg>
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2">
                <h3 class="text-sm font-medium text-gray-900 truncate">{{ workflow.name }}</h3>
                <span v-if="workflow.isDefault" class="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800">
                  默认
                </span>
              </div>
              <p v-if="workflow.description" class="text-xs text-gray-500 mt-1 line-clamp-2">{{ workflow.description }}</p>
              <div class="flex items-center gap-2 mt-2">
                <span class="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-700">
                  {{ workflow.category }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 当前选择的工作流提示 -->
      <div v-if="selectedWorkflow" class="p-3 bg-blue-50 border-t border-blue-200">
        <div class="flex items-center gap-2 text-sm text-blue-700">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
          </svg>
          <span>当前选择: {{ selectedWorkflow.name }}</span>
        </div>
      </div>
    </div>

    <!-- 主聊天区域 -->
    <div class="flex-1 flex flex-col">
      <!-- 聊天标题栏 -->
      <div class="p-4 border-b border-gray-200 bg-white">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <h1 class="text-xl font-semibold text-gray-900">
              {{ selectedWorkflow ? selectedWorkflow.name : '新对话' }}
            </h1>
            <span v-if="selectedWorkflow" class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              {{ selectedWorkflow.category }}
            </span>
          </div>
          <div v-if="selectedWorkflow" class="flex items-center gap-2 text-sm text-gray-500">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span>工作流模式</span>
          </div>
        </div>
      </div>

      <!-- 消息列表 -->
      <div ref="messagesContainer" class="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
        <div
          v-for="msg in chatStore.messages"
          :key="msg.id"
          class="flex"
          :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div
            class="max-w-2xl px-4 py-2 rounded-lg"
            :class="
              msg.role === 'user'
                ? 'bg-blue-600 text-white'
                : 'bg-white shadow border border-gray-200'
            "
          >
            <div v-if="msg.role === 'assistant'" class="markdown-content prose" v-html="renderMarkdown(msg.content)"></div>
            <div v-else>{{ msg.content }}</div>
          </div>
        </div>

        <div v-if="chatStore.isStreaming" class="flex justify-start">
          <div class="max-w-2xl px-4 py-2 rounded-lg bg-white shadow border border-gray-200">
            <div class="flex items-center gap-2">
              <div class="animate-pulse">正在思考...</div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="!chatStore.messages.length && !chatStore.isStreaming" class="flex flex-col items-center justify-center h-full text-gray-400">
          <svg class="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
          </svg>
          <p class="text-lg mb-2">选择一个工作流开始对话</p>
          <p class="text-sm">从左侧工作区选择一个工作流，然后输入您的消息</p>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="border-t border-gray-200 p-4 bg-white">
        <form @submit.prevent="handleSend" class="flex gap-2">
          <input
            v-model="message"
            type="text"
            :disabled="chatStore.isStreaming"
            placeholder="输入消息..."
            class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none disabled:opacity-50"
          />
          <button
            type="submit"
            :disabled="!message.trim() || chatStore.isStreaming"
            class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
          >
            发送
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useChatStore } from '@/stores/chat'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const authStore = useAuthStore()
const chatStore = useChatStore()

// 工作流相关状态
const workflows = ref<any[]>([])
const selectedWorkflow = ref<any>(null)
const selectedCategory = ref('全部')
const loading = ref(false)

const message = ref('')
const messagesContainer = ref<HTMLElement | null>(null)

// 获取所有分类
const workflowCategories = computed(() => {
  const categories = [...new Set(workflows.value.map(w => w.category))]
  return [
    { name: '全部', count: workflows.value.length },
    ...categories.map(cat => ({
      name: cat,
      count: workflows.value.filter(w => w.category === cat).length
    }))
  ]
})

// 根据分类筛选工作流
const filteredWorkflows = computed(() => {
  if (selectedCategory.value === '全部') {
    return workflows.value
  }
  return workflows.value.filter(w => w.category === selectedCategory.value)
})

// 获取工作流列表
const fetchWorkflows = async () => {
  try {
    loading.value = true
    // 这里需要实现获取工作流的API调用
    const response = await fetch('/api/v1/workflows/select-options')
    if (response.ok) {
      workflows.value = await response.json()

      // 自动选择默认工作流
      const defaultWorkflow = workflows.value.find(w => w.isDefault)
      if (defaultWorkflow) {
        selectWorkflow(defaultWorkflow)
      }
    }
  } catch (error) {
    console.error('Failed to fetch workflows:', error)
    workflows.value = []
  } finally {
    loading.value = false
  }
}

// 选择工作流
const selectWorkflow = (workflow: any) => {
  selectedWorkflow.value = workflow
  // 重置消息，准备开始新对话
  if (chatStore.messages.length > 0) {
    chatStore.newConversation()
  }
}

// 发送消息
const handleSend = async () => {
  if (!message.value.trim() || chatStore.isStreaming) return

  const content = message.value
  message.value = ''

  // 添加工作流ID到发送请求
  await chatStore.sendMessage(content, selectedWorkflow.value?.id)
  scrollToBottom()
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// 监听消息变化，自动滚动
watch(() => chatStore.messages.length, scrollToBottom)

// 监听选择的工作流变化
watch(selectedWorkflow, (newWorkflow) => {
  if (newWorkflow) {
    // 可以在这里添加工作流切换的逻辑
    console.log('Selected workflow:', newWorkflow.name)
  }
})

// 初始化
onMounted(async () => {
  await chatStore.fetchConversations()
  await fetchWorkflows()
})
</script>
