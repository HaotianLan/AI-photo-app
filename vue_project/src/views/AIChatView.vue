<template>
  <div class="chat-container">
    <ChatHeader 
      @back="handleBack"
      @toggle-history="toggleHistory"
      @open-settings="openSettings"
    />
    
    <ChatMessages 
      :messages="messages" 
      :loading="loading"
    />
    
    <InputArea 
      @send-message="sendMessage"
      @upload-image="handleImageUpload"
    />
    
    <HistorySidebar 
      :visible="showHistory"
      :history="chatHistory"
      :activeChatId="currentChatId"
      @close="showHistory = false"
      @load-chat="loadChat"
      @clear-history="clearHistory"
      @rename-chat="handleRename"
      
    />
  </div>
</template>

import { ref, onMounted } from 'vue'
<script setup>
import { useRoute, useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
const route = useRoute()
import ChatHeader from '@/components/aichat/ChatHeader.vue'
import ChatMessages from '@/components/aichat/ChatMessages.vue'
import InputArea from '@/components/aichat/InputArea.vue'
import HistorySidebar from '@/components/aichat/HistorySidebar.vue'

// 当前聊天ID (从路由参数获取)
const currentChatId = ref(Number(route.params.id) || Date.now())

// 当前聊天消息
const messages = ref([
  {
    id: currentChatId.value,
    sender: 'ai',
    content: '你好！我是你的AI相机助手，有什么可以帮你的吗？',
    timestamp: new Date().toLocaleTimeString(),
    avatar: 'https://picsum.photos/30/31'
  }
])

// 加载状态
const loading = ref(false)

// 历史记录侧边栏可见性
const showHistory = ref(false)

// 聊天历史记录（从 localStorage 加载）
const chatHistory = ref([])

// 保存当前聊天到历史记录
const saveChatToHistory = () => {
  const title = messages.value[0]?.content?.slice(0, 10) || '新对话'
  const preview = messages.value.find(msg => msg.sender === 'ai')?.content || ''
  const date = new Date().toISOString().split('T')[0]

  const newHistoryItem = {
    id: Date.now(),
    title,
    preview,
    date,
    messages: JSON.parse(JSON.stringify(messages.value)) // 深拷贝
  }

  const existing = JSON.parse(localStorage.getItem('chat-history') || '[]')
  existing.push(newHistoryItem)
  localStorage.setItem('chat-history', JSON.stringify(existing))
  chatHistory.value = existing
}

//  当前聊天 ID
const handleRename = ({ id, newTitle }) => {
  const chat = chatList.value.find(c => c.id === id)
  if (chat) chat.title = newTitle
}
// 加载历史聊天记录
const loadChat = (chatId) => {
  const existing = JSON.parse(localStorage.getItem('chat-history') || '[]')
  const selectedChat = existing.find(chat => chat.id === chatId)
  if (selectedChat) {
    messages.value = selectedChat.messages
    showHistory.value = false
  }
}

// 清空历史记录
const clearHistory = () => {
  localStorage.removeItem('chat-history')
  chatHistory.value = []
}

// 页面挂载时加载历史记录
onMounted(() => {
  const existing = JSON.parse(localStorage.getItem('chat-history') || '[]')
  chatHistory.value = existing
})

// 发送消息
const sendMessage = async (message) => {
  if (!message.trim()) return

  messages.value.push({
    id: Date.now(),
    sender: 'user',
    content: message,
    timestamp: new Date().toLocaleTimeString(),
    avatar: 'https://picsum.photos/30/30'
  })

  loading.value = true
  try {
    const response = await simulateAIResponse(message)

    messages.value.push({
      id: Date.now() + 1,
      sender: 'ai',
      content: response,
      timestamp: new Date().toLocaleTimeString(),
      avatar: 'https://picsum.photos/30/31'
    })

    saveChatToHistory() // 保存到历史记录
  } catch (error) {
    console.error('API调用失败:', error)
  } finally {
    loading.value = false
  }
}

// 处理图片上传，AI回复图片
const handleImageUpload = async (file) => {
  messages.value.push({
    id: Date.now(),
    sender: 'user',
    content: '',
    image: URL.createObjectURL(file),
    timestamp: new Date().toLocaleTimeString(),
    avatar: 'https://picsum.photos/30/30'
  });

  loading.value = true;

  const formData = new FormData();
  formData.append('file', file);
  formData.append('text', '请帮我分析这张图片');  // 加载后端prompt

  try {
    const res = await fetch('http://localhost:3001/chat/image', {
      method: 'POST',
      body: formData
    });

    const data = await res.json();

    messages.value.push({
      id: Date.now() + 1,
      sender: 'ai',
      content: data.response || 'AI无响应',  // 处理无响应情况
      timestamp: new Date().toLocaleTimeString(),
      avatar: 'https://picsum.photos/30/31'
    });

  } catch (err) {
    console.error('图片接口出错:', err);
    messages.value.push({
      id: Date.now() + 1,
      sender: 'ai',
      content: '图片处理失败',
      timestamp: new Date().toLocaleTimeString(),
      avatar: 'https://picsum.photos/30/31'
    });
  }

  loading.value = false;
  saveChatToHistory();
};

// 模拟AI响应文本
const simulateAIResponse = async (message) => {
try {
  const res = await fetch('http://localhost:3001/chat/text', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });

  const data = await res.json();
  return data.reply;
} catch (error) {
  console.error('文本接口出错:', error);
  return 'AI服务出错';
}
}


// 切换历史记录侧边栏
const toggleHistory = () => {
  showHistory.value = !showHistory.value
}

const router = useRouter()

// 返回按钮
const handleBack = () => {
  router.go(-1)
}

// 打开设置
const openSettings = () => {
  console.log('打开设置')
  alert('打开设置')
}
</script>

<style scoped>
.chat-container {
  position: relative;
  width: 100%;
  height: 100vh;
  max-width: 390px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
  overflow: hidden;
}

/* 确保InputArea可见 */
.chat-container > :nth-child(3) {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  max-width: 390px;
  margin: 0 auto;
  background: white;
  z-index: 10;
}
</style>
