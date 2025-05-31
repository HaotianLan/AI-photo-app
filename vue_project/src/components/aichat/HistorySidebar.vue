<template>
  <transition name="sidebar">
    <div v-if="visible" class="history-sidebar">
      <div class="sidebar-overlay" @click="$emit('close')"></div>
      
      <div class="sidebar-panel">
        <!-- 顶部标题栏 -->
        <div class="sidebar-header">
          <h2 class="sidebar-title">对话历史</h2>
          <button class="close-btn" @click="$emit('close')">
            <svg viewBox="0 0 24 24" width="24" height="24">
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" fill="currentColor"/>
            </svg>
          </button>
        </div>
        
        <!-- 历史记录列表 -->
        <div class="history-list">
          <div 
            v-for="item in history" 
            :key="item.id" 
            class="history-item"
            :class="{ 'active': activeChatId === item.id }"
            @click="handleItemClick(item.id)"
          >
            
            <div class="item-content" @click.stop>
              <template v-if="editingId === item.id">
                <input 
                  v-model="editingTitle" 
                  class="edit-input" 
                  @keyup.enter="saveTitle(item)" 
                  @blur="saveTitle(item)" 
                  autofocus
                />
              </template>
              <template v-else>
                <h3 class="item-title">{{ item.title || '未命名对话' }}</h3>
                <p class="item-preview">{{ truncatePreview(item.preview) }}</p>
                <p class="item-date">{{ formatDate(item.date) }}</p>
              </template>
            </div>

            <button 
              class="rename-btn" 
              @click.stop="startEditing(item)"
              title="重命名"
            >
              ✏️
            </button>
          </div>
          
          <div v-if="history.length === 0" class="empty-state">
            <svg viewBox="0 0 24 24" width="48" height="48" class="empty-icon">
              <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14z" fill="#ccc"/>
              <path d="M12 7c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 5c-.55 0-1 .45-1 1v4c0 .55.45 1 1 1s1-.45 1-1v-4c0-.55-.45-1-1-1z" fill="#ccc"/>
            </svg>
            <p class="empty-text">暂无历史记录</p>
          </div>
        </div>
        
        <!-- 底部操作按钮 -->
        <div class="sidebar-footer">
          <button class="clear-btn" @click="confirmClear">
            <svg viewBox="0 0 24 24" width="18" height="18" class="clear-icon">
              <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" fill="currentColor"/>
            </svg>
            清空历史
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  visible: Boolean,
  history: {
    type: Array,
    default: () => []
  },
  activeChatId: [String, Number]
})

const emit = defineEmits(['close', 'load-chat', 'clear-history', 'rename-chat'])

const editingId = ref(null)
const editingTitle = ref('')

// 格式化日期显示
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()

  if (date.toDateString() === now.toDateString()) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  const yesterday = new Date(now)
  yesterday.setDate(yesterday.getDate() - 1)
  if (date.toDateString() === yesterday.toDateString()) {
    return '昨天'
  }

  const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24))
  if (diffDays < 7) {
    const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
    return weekdays[date.getDay()]
  }

  return date.toLocaleDateString([], { month: 'numeric', day: 'numeric' })
}

// 截断预览文本
const truncatePreview = (text) => {
  if (!text) return '...'
  return text.length > 30 ? text.substring(0, 30) + '...' : text
}

const handleItemClick = (chatId) => {
  emit('load-chat', chatId)
  emit('close')
}

const confirmClear = () => {
  if (confirm('确定要清空所有历史记录吗？此操作不可撤销。')) {
    emit('clear-history')
  }
}

// 重命名聊天记录
const startEditing = (item) => {
  editingId.value = item.id
  editingTitle.value = item.title || ''
}

const saveTitle = (item) => {
  if (editingId.value === item.id && editingTitle.value.trim() !== item.title) {
    emit('rename-chat', { id: item.id, newTitle: editingTitle.value.trim() })
  }
  editingId.value = null
  editingTitle.value = ''
}
</script>

<style scoped>
.history-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
  display: flex;
}

.sidebar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(2px);
}

.sidebar-panel {
  position: relative;
  width: 85%;
  max-width: 320px;
  height: 100%;
  background-color: #fff;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  z-index: 1;
}

.sidebar-header {
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #f0f0f0;
}

.sidebar-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  padding: 8px;
  color: #666;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.history-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px 0;
}

.history-item {
  display: flex;
  padding: 12px 16px;
  gap: 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.history-item:hover {
  background-color: #f9f9f9;
}

.history-item.active {
  background-color: #f0f7ff;
}

.item-avatar {
  width: 44px;
  height: 44px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
}

.item-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-content {
  flex: 1;
  min-width: 0;
}

.item-title {
  margin: 0 0 4px;
  font-size: 15px;
  font-weight: 500;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-preview {
  margin: 0 0 4px;
  font-size: 13px;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-date {
  margin: 0;
  font-size: 12px;
  color: #999;
}

.empty-state {
  padding: 40px 20px;
  text-align: center;
  color: #999;
}

.empty-icon {
  opacity: 0.6;
  margin-bottom: 12px;
}

.empty-text {
  margin: 0;
  font-size: 14px;
}

.sidebar-footer {
  padding: 12px 16px;
  border-top: 1px solid #f0f0f0;
}

.clear-btn {
  width: 100%;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #ff4d4f;
  border-radius: 6px;
  color: #ff4d4f;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.clear-btn:hover {
  background-color: #fff2f0;
}

.clear-icon {
  color: #ff4d4f;
}

/* 过渡动画 */
.sidebar-enter-active,
.sidebar-leave-active {
  transition: opacity 0.3s ease;
}

.sidebar-enter-from,
.sidebar-leave-to {
  opacity: 0;
}

.sidebar-enter-active .sidebar-panel,
.sidebar-leave-active .sidebar-panel {
  transition: transform 0.3s ease;
}

.sidebar-enter-from .sidebar-panel,
.sidebar-leave-to .sidebar-panel {
  transform: translateX(-100%);
}
/* 历史记录重命名 */
.rename-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #888;
  padding: 0 8px;
  font-size: 16px;
  flex-shrink: 0;
}
.rename-btn:hover {
  color: #333;
}

.edit-input {
  width: 100%;
  padding: 4px 6px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>