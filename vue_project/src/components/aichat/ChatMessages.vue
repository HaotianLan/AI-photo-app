<template>
  <div class="messages-container" ref="messagesContainer">
    <div class="messages-list">
      <MessageBubble 
        v-for="message in messages" 
        :key="message.id"
        :message="message"
      />
      
      <div v-if="loading" class="loading-indicator">
        <div class="typing-indicator">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import MessageBubble from './MessageBubble.vue'

const props = defineProps({
  messages: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const messagesContainer = ref(null)

// 当消息更新时自动滚动到底部
watch(() => props.messages, async () => {
  await nextTick()
  scrollToBottom()
}, { deep: true })

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}
</script>

<style scoped>
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 12px 16px;
  background-color: #f5f5f5;
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.loading-indicator {
  display: flex;
  justify-content: flex-start;
  padding: 8px 12px;
}

.typing-indicator {
  display: flex;
  align-items: center;
  height: 17px;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  margin: 0 2px;
  background-color: #9E9E9E;
  border-radius: 50%;
  display: inline-block;
  opacity: 0.4;
}

.typing-indicator span:nth-child(1) {
  animation: typing 1s infinite;
}

.typing-indicator span:nth-child(2) {
  animation: typing 1s infinite 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation: typing 1s infinite 0.4s;
}

@keyframes typing {
  0% {
    opacity: 0.4;
    transform: translateY(0);
  }
  50% {
    opacity: 1;
    transform: translateY(-3px);
  }
  100% {
    opacity: 0.4;
    transform: translateY(0);
  }
}
</style>