<template>
  <div class="chat-list">
    <div class="chat-item" v-for="(item, index) in chatList" :key="index" @click="goToChatDetail(item.id)">
      <div class="chat-item-avatar">
        <div class="avatar-placeholder"></div>
      </div>
      <div class="chat-item-content">
        <div class="chat-item-username">{{ item.username }}</div>
        <div class="chat-item-message">{{ item.message }}</div>
      </div>
      <div class="chat-item-time">{{ item.time }}</div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const chatList = [
  { id: 1, username: '爱吃椰子（2）', message: '博主，你这个怎么拍的？', time: '10:30' },
  { id: 2, username: '香菜', message: '哈喽哈喽', time: '昨天' },
  { id: 3, username: '梅梅香', message: '约拍怎么算价格呢？', time: '周二' },
  { id: 4, username: '余弦定理', message: '已发送，请查收', time: '周一' },
  { id: 5, username: '我要暴富', message: '可以改到下午3点', time: '4/15' },
  { id: 6, username: '快乐一家人（10）', message: '谢谢你的帮助！', time: '4/10' }
];

const goToChatDetail = (id) => {
  router.push({ name: 'chat-detail', params: { id } });
};
</script>

<style scoped>
.chat-list {
  flex: 1;
  overflow-y: auto;
  padding: 4px;
}

.chat-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 4px;
  padding: 10px;
  border-radius: 5px;
  background-color: #f8f8f8;
}

.chat-item-avatar {
  width: 40px;
  height: 40px;
  margin-right: 12px;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: #eee;
  border: 1px solid #ddd;
}

.chat-item-content {
  flex: 1;
}

.chat-item-username {
  font-weight: bold;
}

.chat-item-message {
  font-size: 14px;
  color: #666;
}

.chat-item-time {
  font-size: 12px;
  color: #999;
}

.action-icons {
  display: flex;
  justify-content: space-around;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #eee;
}

.icon-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  font-size: 12px;
}

.icon-item img {
  width: 20px;
  height: 20px;
}
</style>