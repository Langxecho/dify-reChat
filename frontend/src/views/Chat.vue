<template>
  <div class="flex h-screen bg-gray-100">
    <!-- 侧边栏 -->
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

    <!-- 主聊天区域 -->
    <div class="flex-1 flex flex-col">
      <!-- 消息列表 -->
      <div ref="messagesContainer" class="flex-1 overflow-y-auto p-6 space-y-4">
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
import { ref, onMounted, nextTick, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useChatStore } from '@/stores/chat'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const authStore = useAuthStore()
const chatStore = useChatStore()

const message = ref('')
const messagesContainer = ref<HTMLElement | null>(null)

// 渲染Markdown
const renderMarkdown = (content: string) => {
  const html = marked.parse(content)
  return DOMPurify.sanitize(html)
}

// 发送消息
const handleSend = async () => {
  if (!message.value.trim() || chatStore.isStreaming) return

  const content = message.value
  message.value = ''

  await chatStore.sendMessage(content)
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

// 初始化
onMounted(async () => {
  await chatStore.fetchConversations()
})
</script>
