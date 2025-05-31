<template>
  <div class="chat-input">
    <div class="voice-btn">
      <img src="/images/icons/yuyin.svg" alt="语音">
    </div>
    <input 
      type="text" 
      placeholder="发送消息..." 
      class="message-input"
      v-model="inputMessage"
      @keyup.enter="send"
    >
    <div class="input-actions">
      <span class="emoji-btn">😊</span>
      <span class="add-btn">+</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const inputMessage = ref('');
const emit = defineEmits(['send']);

const send = () => {
  if (inputMessage.value.trim()) {
    emit('send', inputMessage.value);
    inputMessage.value = '';
  }
};
</script>

<style scoped>
.chat-input {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  padding: 8px 10px;
  background-color: #f9f9f9;
  border-top: 1px solid #e0e0e0;
  z-index: 1000;
}

.voice-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
  font-size: 20px;
}

.message-input {
  flex: 1;
  border: none;
  border-radius: 20px;
  padding: 8px 12px;
  outline: none;
  font-size: 15px;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
}

.input-actions {
  display: flex;
  margin-left: 8px;
}

.emoji-btn, .add-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin-left: 4px;
  cursor: pointer;
}
</style>