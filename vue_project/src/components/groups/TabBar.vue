<template>
  <div class="tab-bar">
    <div class="tab-item" :class="{ active: currentTab === 'group' }" @click="currentTab = 'group'">
      消息列表
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const currentTab = ref('friend');
const friendBadgeCount = ref(2);
</script>

<style scoped>
.tab-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 40px;
  background-color: #f0f0f0;
}

.tab-item {
  padding: 5px 10px;
  cursor: pointer;
}

.tab-item.active {
  color: #000000;
  border-radius: 5px;
}

</style>