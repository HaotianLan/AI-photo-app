<template>
  <div v-if="show" class="scanning-overlay">
    <div class="scanning-content">
      <img src="/dist/images/icons/saomiaozhong.svg" alt="扫描中">
      <p>场景扫描中...</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: Boolean
});
</script>

<style scoped>
.scanning-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 200;
}

.scanning-content {
  text-align: center;
  color: white;
}

.scanning-content img {
  width: 60px;
  height: 60px;
  margin-bottom: 16px;
}

.scanning-content p {
  font-size: 18px;
  margin: 0;
}
</style>