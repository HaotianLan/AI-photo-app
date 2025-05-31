<template>
  <div class="checkin-search-container">
    <img
      src="/images/icons/kuoda.svg"
      alt="位置"
      class="left-icon"
      @click="$emit('toggle')"
    />
    <div class="search-bar">
      <input
        type="text"
        placeholder="搜索打卡点"
        class="search-input"
      />
    </div>
    <img
      src="/images/icons/heart-icon.svg"
      alt="收藏"
      class="right-icon"
    />
  </div>
</template>

<script setup>
defineEmits(['toggle'])
// 打卡点页面搜索框组件
</script>

<style scoped>
.checkin-search-container {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 15px;
  background: white;
  box-sizing: border-box;
}

.left-icon, .right-icon {
  width: 24px;
  height: 24px;
  cursor: pointer;
}

.search-bar {
  flex: 1;
  margin: 0 10px;
  position: relative;
  max-width: calc(100% - 80px);
}

.search-input {
  width: 100%;
  padding: 8px 12px;
  border-radius: 20px;
  border: none;
  background: #f5f5f5;
  outline: none;
  font-size: 14px;
  box-sizing: border-box;
}

.search-input::placeholder {
  color: #999;
}
</style>