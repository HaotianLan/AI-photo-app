<template>
  <div class="transparent-bar">
    <div class="fixed-square"></div>
    <div class="scroll-container">
      <div
        v-for="i in 9"
        :key="i"
        class="square"
      ></div>
    </div>
  </div>
</template>

<script setup>
// 可以在这里添加交互逻辑
</script>

<style scoped>
.transparent-bar {
  position: absolute;
  bottom: 160px;
  left: 0;
  width: 100%;
  height: 60px;
  z-index: 10;
  padding: 10px 0;
  display: flex;
}

.fixed-square {
  width: 40px;
  height: 40px;
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  margin-left: 20px;
  flex-shrink: 0;
}

.scroll-container {
  display: flex;
  gap: 10px;
  padding: 0 10px;
  height: 100%;
  overflow-x: auto;
  flex-grow: 1;
}

.square {
  min-width: 40px;
  height: 40px;
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  flex-shrink: 0;
}
</style>