<template>
  <div class="title-bar">
    <router-link to="/friends-groups" class="message-btn">
      <div class="message-container">
        <img src="/images/icons/pinglun.svg" alt="我的消息" style="width: 16px; height: 16px;">
        <span>我的消息</span>
      </div>
    </router-link>
  </div>
</template>

<style scoped>
.title-bar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 0 16px;
  height: 36px;
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 100;
}

.message-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  text-decoration: none;
  color: inherit;
}

.message-container {
  display: flex;
  align-items: center;
  background-color: #f5f5f5;
  padding: 4px 8px;
  border-radius: 12px;
  gap: 4px;
  height: 24px;
  margin-top: 8px;
  margin-bottom: 8px;
}

.message-container img {
  width: 16px;
  height: 16px;
}
</style>