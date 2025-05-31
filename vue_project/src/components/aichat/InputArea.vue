<template>
  <div class="input-area">
    <button class="input-button" @click="handleImageUpload">
      <svg viewBox="0 0 24 24" width="24" height="24">
        <path d="M19 5v14H5V5h14m0-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-4.86 8.86l-3 3.87L9 13.14 6 17h12l-3.86-5.14z" fill="currentColor"/>
      </svg>
      <input 
        type="file" 
        ref="fileInput"
        accept="image/*"
        style="display: none"
        @change="onFileChange"
      >
    </button>
    
    <textarea 
      v-model="message" 
      type="text" 
      class="message-input" 
      placeholder="输入消息..."
      @input="adjustHeight"
      @keydown.enter.exact.prevent="sendMessage"
      @keydown.enter.shift=""
      rows="1"
    >
    </textarea>
    
    <button 
      class="send-button" 
      :disabled="!message.trim()"
      @click="sendMessage"
    >
      <svg viewBox="0 0 24 24" width="24" height="24">
        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" fill="currentColor"/>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const message = ref('')
const fileInput = ref(null)

const emit = defineEmits(['send-message', 'upload-image'])

const adjustHeight = (e) => {
  e.target.style.height = 'auto'
  e.target.style.height = `${e.target.scrollHeight}px`
}

const sendMessage = () => {
  if (message.value.trim()) {
    emit('send-message', message.value)
    message.value = ''
  }
}

const handleImageUpload = () => {
  fileInput.value.click()
}

const onFileChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    emit('upload-image', file)
    fileInput.value.value = '' // 重置input，允许重复选择同一文件
  }
}
</script>

<style scoped>
.input-area {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  background-color: #ffffff;
  border-top: 1px solid #eaeaea;
}

.message-input {
  flex: 1;
  border: none;
  border-radius: 18px;
  padding: 10px 16px;
  background-color: #f5f5f5;
  font-size: 16px;
  outline: none;
  margin: 0 8px;
}

.input-button, .send-button {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>