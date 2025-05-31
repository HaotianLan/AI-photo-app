<template>
  <div class="chat-messages">
    <div class="message-timestamp">{{ messages[0]?.time || '15: 01' }}</div>
    
    <!-- 他人消息：靠左显示 -->
    <div v-for="(msg, index) in messages" :key="index" 
         :class="isSelf(msg.username) ? 'message-self' : 'message-other'">
      
      <!-- 别人的消息 -->
      <template v-if="!isSelf(msg.username)">
        <!-- 头像 -->
        <div class="avatar-container">
          <img class="avatar" :src="getAvatar(msg.username, false)" :alt="msg.username">
        </div>
        
        <!-- 消息内容 -->
        <div class="message-box">
          <div class="user-name">{{ msg.username }}</div>
          
          <!-- 文本消息 -->
          <div v-if="msg.type === 'text'" class="bubble other-bubble">
            {{ msg.text }}
          </div>
          
          <!-- 图片消息 -->
          <div v-else-if="msg.type === 'image'" class="bubble image-bubble other-bubble">
            <img :src="msg.image" :alt="msg.caption">
            <div class="image-caption">{{ msg.caption }}</div>
          </div>
        </div>
      </template>
      
      <!-- 自己的消息 -->
      <template v-else>
        <div class="self-content">
          <!-- 用户名 -->
          <div class="user-name self-name">{{ msg.username }}</div>
          
          <!-- 文本消息 -->
          <div v-if="msg.type === 'text'" class="bubble self-bubble">
            {{ msg.text }}
          </div>
          
          <!-- 图片消息 -->
          <div v-else-if="msg.type === 'image'" class="bubble image-bubble self-bubble">
            <img :src="msg.image" :alt="msg.caption">
            <div class="image-caption">{{ msg.caption }}</div>
          </div>
        </div>
        
        <!-- 头像 -->
        <div class="icons-container">
          <img class="avatar" :src="getAvatar(msg.username, true)" :alt="msg.username">
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import { posts } from '../../data/posts';

const props = defineProps({
  messages: {
    type: Array,
    required: true
  }
});

// 判断消息是否为自己发送的
const isSelf = (username) => {
  return username === '蜡笔小芯' || username === '我';
};

// 获取头像图片
const getAvatar = (username, isSelf) => {
  // 自己的消息使用固定头像
  if (isSelf) {
    return '/images/posts/1.jpg';
  } else {
    // 其他用户使用固定头像
    return '/images/posts/2.jpg';
  }
};
</script>

<style scoped>
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px 16px;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

.message-timestamp {
  text-align: center;
  font-size: 12px;
  color: #999;
  margin: 10px 0;
}

/* 别人的消息样式 */
.message-other {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
  align-self: flex-start;
  max-width: 80%;
}

/* 自己的消息样式 */
.message-self {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
  align-self: flex-end;
}

.avatar-container {
  margin-right: 8px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.send-icon {
  width: 24px;
  height: 24px;
  margin-right: 4px;
}

.icons-container {
  display: flex;
  align-items: flex-start;
  margin-left: 8px;
}

.message-box {
  display: flex;
  flex-direction: column;
}

.self-content {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  max-width: 200px;
  padding-top: 4px;
}

.user-name {
  font-size: 12px;
  color: #999;
  margin-bottom: 4px;
}

.self-name {
  margin-bottom: 4px;
  text-align: right;
}

.bubble {
  padding: 10px 12px;
  border-radius: 16px;
  font-size: 15px;
  word-break: break-word;
  max-width: 100%;
}

.other-bubble {
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
}

.self-bubble {
  background-color: #95ec69;
  border: none;
  align-self: flex-end;
}

.image-bubble {
  padding: 2px;
  overflow: hidden;
}

.image-bubble img {
  width: 100%;
  max-width: 200px;
  border-radius: 8px;
  display: block;
}

.image-caption {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
  padding: 0 4px;
}
</style>