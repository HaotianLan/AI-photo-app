<template>
  <div 
    class="message" 
    :class="{
      'message-ai': message.sender === 'ai',
      'message-user': message.sender === 'user'
    }"
  >
    <img 
      v-if="message.avatar" 
      :src="message.avatar" 
      class="message-avatar" 
      alt="avatar"
    >
    
    <div class="message-content">
      <div 
        v-if="message.content" 
        class="message-text"
      >
        {{ message.content }}
      </div>
      
      <img 
        v-if="message.image" 
        :src="message.image" 
        class="message-image" 
        alt="uploaded"
      >
      
      <div class="message-time">
        {{ message.timestamp }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.message {
  display: flex;
  gap: 8px;
  max-width: 80%;
}

.message-ai {
  align-self: flex-start;
}

.message-user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 4px;
  object-fit: cover;
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.message-text {
  padding: 10px 14px;
  border-radius: 18px;
  font-size: 16px;
  line-height: 1.4;
  word-wrap: break-word;
}

.message-ai .message-text {
  background-color: #ffffff;
  border-top-left-radius: 0;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.message-user .message-text {
  background-color: #95ec69;
  border-top-right-radius: 0;
  color: #000000;
}

.message-image {
  max-width: 200px;
  max-height: 200px;
  border-radius: 8px;
  object-fit: cover;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.message-time {
  font-size: 11px;
  color: #999;
  padding: 0 8px;
}

.message-user .message-time {
  text-align: right;
}
</style>