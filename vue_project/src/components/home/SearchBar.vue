<template>
  <div class="search-container">
    <img
      src="/images/icons/caidan_1.svg"
      alt="菜单图标"
      class="menu-icon"
      @click="emit('openMenu')"
    />
    <div class="search-bar">
      <div class="search-icon-container">
        <img
          src="/images/icons/search-icon.svg"
          alt="搜索图标"
          class="search-icon"
        />
      </div>
      <input
        type="text"
        placeholder="请输入搜索内容"
        class="search-input"
        @click="goToSearchPage"
      />
    </div>
    <img
      src="/images/icons/wuguan.svg"
      alt="AI小助手"
      class="menu-icon right-icon"
      @click="openAIAssistant"
    />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();
const emit = defineEmits(['openMenu']);

const goToSearchPage = () => {
  router.push('/search');
};

const openAIAssistant = () => {
  // 使用时间戳作为聊天ID
  const chatId = Date.now();
  router.push({
    name: 'ai-chat',
    params: { id: chatId }
  });
};
</script>

<style scoped>
.search-container {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  gap: 10px;
  height: 60px;
  box-sizing: border-box;
}

.menu-icon {
  width: 28px;
  height: 28px;
  cursor: pointer;
}

.search-bar {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 800px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  position: relative;
}

.search-icon-container {
  padding: 0 12px;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  padding: 12px 12px 12px 0;
  font-size: 14px;
  color: #333;
}

.search-input::placeholder {
  color: #999;
  opacity: 1;
}

.search-icon {
  width: 20px;
  height: 20px;
}

.right-icon {
  margin-left: 10px;
}

@media (min-width: 768px) {
  .search-bar {
    border-radius: 30px;
  }
}
</style>