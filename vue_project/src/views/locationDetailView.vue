<template>
  <div class="spot-detail-view">
    <!-- 标题栏 -->
    <div class="header">
      <button class="back-button" @click="goBack">
        <img src="/images/icons/jiantou.svg" alt="返回">
      </button>
      <div class="action-buttons">
        <button class="favorite-button">
          <img src="/images/icons/heart-icon.svg" alt="收藏" />
        </button>
        <button class="share-button">
          <img src="/images/icons/fenxiang.svg" alt="分享" />
        </button>
      </div>
    </div>

    <!-- 地点信息 -->
    <div class="spot-info">
      <h1 class="spot-name">{{ location.name }}</h1>
      <div class="spot-meta">
        <span>距离 {{ location.distance }}</span>
        <span>步行 {{ location.walkTime }}min</span>
        <span>{{ location.takenCount }} 拍过</span>
        <span>{{ location.viewedCount }} 人浏览过</span>
      </div>
    </div>

    <!-- 描述文本 -->
    <div class="spot-description">
      <p>{{ location.tagline }}</p>
    </div>

    <!-- 图片网格 -->
    <div class="photo-grid">
      <div
        v-for="(photo, index) in location.images"
        :key="index"
        class="photo-item"
      >
        <img :src="photo" :alt="'打卡点照片' + index" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { computed } from 'vue'

const router = useRouter()
const route = useRoute()

// 将 query 中的信息组装为 location 对象
const location = computed(() => ({
  name: route.query.name || '未知地点',
  distance: route.query.distance || '--',
  walkTime: route.query.walkTime || '--',
  takenCount: route.query.takenCount || '--',
  viewedCount: route.query.viewedCount || '--',
  tagline: route.query.tagline || '暂无介绍',
  images: Array.isArray(route.query.images)
    ? route.query.images
    : route.query.images
      ? [route.query.images]  // 兼容单图
      : ['/images/posts/1.jpg']  // 默认图
}))
console.log('route.query.images',route.query.images)
const goBack = () => {
  router.go(-1)
}
</script>


<style scoped>
.back-button,
.favorite-button,
.share-button {
  background: none;
  border: none;
  padding: 0;
  margin: 0;
  cursor: pointer;
}

.spot-detail-view {
  max-width: 390px;
  margin: 0 auto;
  padding: 16px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.back-button img {
  width: 24px;
  height: 24px;
}

.action-buttons {
  display: flex;
  gap: 16px;
}

.action-buttons img {
  width: 24px;
  height: 24px;
}

.spot-info {
  margin-bottom: 20px;
}

.spot-name {
  font-size: 24px;
  margin-bottom: 8px;
}

.spot-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 12px;
  color: #666;
}

.spot-description {
  margin-bottom: 20px;
  font-size: 14px;
  line-height: 1.5;
}

.photo-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.photo-item {
  aspect-ratio: 1;
  overflow: hidden;
  border-radius: 8px;
}

.photo-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>