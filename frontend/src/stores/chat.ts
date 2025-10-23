import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as chatApi from '@/api/chat'
import type { Conversation, Message } from '@/api/chat'

export const useChatStore = defineStore('chat', () => {
  // State
  const conversations = ref<Conversation[]>([])
  const currentConversation = ref<Conversation | null>(null)
  const messages = ref<Message[]>([])
  const isStreaming = ref(false)
  const streamingMessage = ref('')

  // Actions
  const fetchConversations = async () => {
    try {
      conversations.value = await chatApi.getConversations()
    } catch (error) {
      console.error('Failed to fetch conversations:', error)
      throw error
    }
  }

  const selectConversation = async (conversationId: number) => {
    try {
      const conversation = conversations.value.find((c) => c.id === conversationId)
      if (conversation) {
        currentConversation.value = conversation
        messages.value = await chatApi.getConversationMessages(conversationId)
      }
    } catch (error) {
      console.error('Failed to load conversation:', error)
      throw error
    }
  }

  const sendMessage = async (content: string) => {
    if (isStreaming.value) return

    isStreaming.value = true
    streamingMessage.value = ''

    // 添加用户消息到界面
    const userMessage: Message = {
      id: Date.now(),
      conversation_id: currentConversation.value?.id ?? 0,
      role: 'user',
      content,
      metadata: null,
      created_at: new Date().toISOString()
    }
    messages.value.push(userMessage)

    // 创建临时助手消息
    const assistantMessage: Message = {
      id: Date.now() + 1,
      conversation_id: currentConversation.value?.id ?? 0,
      role: 'assistant',
      content: '',
      metadata: null,
      created_at: new Date().toISOString()
    }
    messages.value.push(assistantMessage)

    let conversationId = currentConversation.value?.id

    await chatApi.streamChat(
      { message: content, conversation_id: conversationId },
      (chunk) => {
        // 处理SSE数据
        const lines = chunk.split('\n')
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))

              // 获取对话ID
              if (data.event === 'conversation_id' && data.conversation_id) {
                conversationId = data.conversation_id
                assistantMessage.conversation_id = conversationId
                userMessage.conversation_id = conversationId
              }

              // 更新助手消息内容
              if (data.answer) {
                assistantMessage.content += data.answer
              } else if (data.event === 'agent_message' || data.event === 'message') {
                if (data.answer) {
                  assistantMessage.content += data.answer
                }
              }
            } catch (e) {
              // 忽略解析错误
            }
          }
        }
      },
      () => {
        // 流结束
        isStreaming.value = false
        streamingMessage.value = ''

        // 如果是新对话，刷新对话列表
        if (!currentConversation.value || !conversations.value.find(c => c.id === conversationId)) {
          fetchConversations()
        }

        // 设置当前对话
        if (conversationId) {
          const conv = conversations.value.find(c => c.id === conversationId)
          if (conv) {
            currentConversation.value = conv
          }
        }
      },
      (error) => {
        // 错误处理
        console.error('Stream error:', error)
        isStreaming.value = false
        assistantMessage.content = '抱歉，发生了错误，请稍后重试。'
      }
    )
  }

  const deleteConversation = async (conversationId: number) => {
    try {
      await chatApi.deleteConversation(conversationId)
      conversations.value = conversations.value.filter((c) => c.id !== conversationId)

      if (currentConversation.value?.id === conversationId) {
        currentConversation.value = null
        messages.value = []
      }
    } catch (error) {
      console.error('Failed to delete conversation:', error)
      throw error
    }
  }

  const newConversation = () => {
    currentConversation.value = null
    messages.value = []
  }

  return {
    conversations,
    currentConversation,
    messages,
    isStreaming,
    streamingMessage,
    fetchConversations,
    selectConversation,
    sendMessage,
    deleteConversation,
    newConversation
  }
})
