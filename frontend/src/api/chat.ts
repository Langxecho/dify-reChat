import apiClient from './client'

export interface ChatRequest {
  message: string
  conversation_id?: number
}

export interface Conversation {
  id: number
  user_id: number
  title: string
  is_archived: boolean
  created_at: string
  updated_at: string
  message_count?: number
}

export interface Message {
  id: number
  conversation_id: number
  role: 'user' | 'assistant'
  content: string
  metadata: string | null
  created_at: string
}

// 流式聊天
export const streamChat = async (
  data: ChatRequest,
  onMessage: (chunk: string) => void,
  onEnd: () => void,
  onError: (error: Error) => void
) => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch('/api/v1/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(data)
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body?.getReader()
    const decoder = new TextDecoder()

    if (!reader) {
      throw new Error('No reader available')
    }

    while (true) {
      const { done, value } = await reader.read()
      if (done) {
        onEnd()
        break
      }

      const chunk = decoder.decode(value)
      onMessage(chunk)
    }
  } catch (error) {
    onError(error as Error)
  }
}

// 获取对话列表
export const getConversations = async (): Promise<Conversation[]> => {
  const response = await apiClient.get<Conversation[]>('/conversations')
  return response.data
}

// 获取对话消息
export const getConversationMessages = async (
  conversationId: number
): Promise<Message[]> => {
  const response = await apiClient.get<Message[]>(
    `/conversations/${conversationId}/messages`
  )
  return response.data
}

// 更新对话
export const updateConversation = async (
  conversationId: number,
  data: { title?: string; is_archived?: boolean }
): Promise<Conversation> => {
  const response = await apiClient.patch<Conversation>(
    `/conversations/${conversationId}`,
    data
  )
  return response.data
}

// 删除对话
export const deleteConversation = async (conversationId: number): Promise<void> => {
  await apiClient.delete(`/conversations/${conversationId}`)
}
