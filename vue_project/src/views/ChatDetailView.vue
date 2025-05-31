<template>
  <div class="chat-detail-container">
    <ChatHeader 
      :avatar="groupAvatar"
      :name="groupName"
      @back="goBack"
      @settings="openSettings"
    />
    <ChatMessages :messages="messages" />
    <ChatInput @send="sendMessage" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import ChatHeader from '@/components/groups/ChatHeader.vue';
import ChatMessages from '@/components/groups/ChatMessages.vue';
import ChatInput from '@/components/groups/ChatInput.vue';

const router = useRouter();

// 群聊头像
const groupAvatar = ref('/images/icons/xiangji.svg');
// 群聊名称
const groupName = ref('爱吃椰子（2）');
// 模拟消息列表
const messages = ref([
  {
    username: '椰子',
    avatar: '/images/icons/jiantou.svg',
    time: '15: 01',
    type: 'text',
    text: '消息消息消息消息消息消息'
  },
  {
    username: '椰子',
    avatar: '/images/icons/jiantou.svg',
    time: '15: 01',
    type: 'image',
    image: '/images/posts/1.jpg',
    caption: '用户名1 在《校园》拍摄集中添加了一张照片'
  },
  {
    username: '蜡笔小芯',
    avatar: '/images/icons/fasong.svg',
    time: '15: 01',
    type: 'text',
    text: '博主，你这个怎么拍的？'
  }
]);

// 返回按钮点击事件
const goBack = () => {
  router.back();
};

// 打开设置按钮点击事件
const openSettings = () => {
  console.log('打开设置');
};

// 发送消息
const sendMessage = (message) => {
  messages.value.push({
    username: '用户名2',
    avatar: '/images/icons/fasong.svg',
    time: new Date().toLocaleTimeString().slice(0, 5),
    type: 'text',
    text: message
  });
};
</script>

<style scoped>
.chat-detail-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
}

.chat-input {
  flex-shrink: 0;
}
</style>