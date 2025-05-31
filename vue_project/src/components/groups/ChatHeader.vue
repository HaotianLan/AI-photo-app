<template>
  <div class="chat-header">
    <div class="header-left" @click="goBack">
      <img src="/images/icons/jiantou.svg" class="back-icon" alt="返回">
    </div>
    <div class="group-info">
      <img class="group-avatar" src="/images/posts/3.jpg" alt="群聊头像">
      <span class="group-name">{{ name }}</span>
    </div>
    <div class="header-right" @click="openSettings">
      <img src="/images/icons/shezhi.svg" class="settings-icon" alt="设置">
    </div>
  </div>
</template>

<script setup>
defineProps({
  avatar: String,
  name: String
});

const emit = defineEmits(['back', 'settings']);

const goBack = () => emit('back');
const openSettings = () => emit('settings');
</script>

<style scoped>
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  background-color: #ffffff;
  border-bottom: 1px solid #e6e6e6;
  height: 44px;
  position: sticky;
  top: 0;
  z-index: 10;
}

.header-left {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.group-info {
  display: flex;
  align-items: center;
  flex: 1;
  margin-left: 10px;
}

.group-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  margin-right: 8px;
}

.group-name {
  font-size: 16px;
  font-weight: 500;
}

.header-right {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.back-icon, .settings-icon {
  width: 20px;
  height: 20px;
  object-fit: contain;
}
</style>