<template>
  <div class="post-content">
    <h2 class="post-title">{{ title }}</h2>
    <p class="post-text">{{ text }}</p>
    <div class="post-tags">
      <span v-for="(tag, index) in tags" :key="index">#{{ tag }}</span>
    </div>
    <div class="post-meta">
      <span class="post-time">{{ time }}</span>
      <span class="post-ip">{{ ip }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: ''
  },
  text: {
    type: String,
    default: ''
  },
  tags: {
    type: Array,
    default: () => []
  },
  time: {
    type: String,
    default: ''
  },
  ip: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.post-content {
  padding: 15px;
  flex: 1;
  overflow-y: auto;
  scrollbar-gutter: stable;
  padding-bottom: 5px;
}

.post-title {
  font-size: 18px;
  margin-bottom: 10px;
}

.post-text {
  font-size: 15px;
  line-height: 1.6;
  margin-bottom: 15px;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 15px;
}

.post-tags span {
  color: #98bec7;
  font-size: 14px;
}

.post-meta {
  display: flex;
  gap: 10px;
  font-size: 12px;
  color: #999;
}
</style>