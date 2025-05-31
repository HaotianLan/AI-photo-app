<template>
  <div class="tab-bar">
    <div
      v-for="tab in tabs"
      :key="tab.id"
      :class="['tab-item', { active: activeTab === tab.id }]"
      @click="activeTab = tab.id"
    >
      {{ tab.label }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const tabs = [
  { id: 1, label: '精品' },
  { id: 2, label: '关注' },
  { id: 3, label: '推荐' },
  { id: 4, label: '附近' }
]

const activeTab = ref(1)
</script>

<style scoped>
.tab-bar {
  display: flex;
  justify-content: center;
  background: white;
  padding: 10px 0;
  gap: 20px;
}

.tab-item {
  font-size: 16px;
  color: #333;
  cursor: pointer;
  padding: 5px 10px;
  transition: all 0.2s;
}

.tab-item.active {
  color: #FF69B4;
  font-weight: bold;
}

.tab-item:hover {
  transform: scale(1.05);
}

@media (min-width: 768px) {
  .tab-bar {
    gap: 40px;
  }
}
</style>