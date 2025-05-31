<template>
  <div class="content-wrapper">
    <div class="user-info">
      <div class="user-header">
        <img class="avatar" src="/images/posts/1.jpg" alt="用户头像">
        <div class="user-details">
          <div class="username">蜡笔小芯</div>
          <div class="user-id">id: 123456789</div>
          <div class="user-ip">ip: 江苏</div>
        </div>
      </div>
      <div class="user-bio">欢迎宝宝们找我约拍📷！！！</div>
      <div class="user-stats">
        <div class="stat-item">
          <span>123</span>
          <span>跟拍</span>
        </div>
        <div class="stat-item">
          <span>123</span>
          <span>关注</span>
        </div>
        <div class="stat-item">
          <span>123</span>
          <span>粉丝</span>
        </div>
        <div class="stat-item">
          <span>123</span>
          <span>获赞与收藏</span>
        </div>
      </div>
      <button class="edit-profile-btn">编辑资料</button>
      <div class="tag-container">
        <span class="tag">萌系宝贝拍摄大师</span>
        <span class="tag">专业日系风格人像摄影</span>
      </div>
    </div>

    <div class="nav-tabs">
      <ul>
        <li class="tab-item" :class="{ active: activeTab === '作品' }" @click="$emit('update:activeTab', '作品')">作品</li>
        <li class="tab-item" :class="{ active: activeTab === '收藏' }" @click="$emit('update:activeTab', '收藏')">收藏</li>
        <li class="tab-item" :class="{ active: activeTab === '足迹' }" @click="$emit('update:activeTab', '足迹')">足迹</li>
        <li class="tab-item search-item">
          <input type="text" placeholder="请输入">
        </li>
      </ul>
    </div>

    <div class="content-container">
      <div v-if="activeTab === '作品'" class="tab-content">
        <div class="media-item" v-for="(media, index) in mediaList" :key="index">
          <img :src="media.imageUrl" alt="媒体内容">
          <div class="media-desc">{{ media.description }}</div>
          <div class="media-interaction">
            <span class="view-count">{{ media.viewCount }}</span>
            <span class="like-count">{{ media.likeCount }}</span>
          </div>
        </div>
      </div>
      <div v-if="activeTab === '收藏'" class="tab-content">
        收藏内容
      </div>
      <div v-if="activeTab === '足迹'" class="tab-content">
        足迹内容
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  activeTab: {
    type: String,
    required: true
  },
  mediaList: {
    type: Array,
    required: true
  }
})

defineEmits(['update:activeTab'])
</script>

<style scoped>
.content-wrapper {
  position: relative;
}

.user-info {
  padding: 16px;
  border-bottom: 1px solid #eee;
}

.user-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 12px;
  object-fit: cover;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-id,
.user-ip {
  font-size: 12px;
  color: #999;
}

.user-bio {
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
}

.user-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 14px;
}

.edit-profile-btn {
  width: 100%;
  padding: 8px;
  background-color: #f4f4f4;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 8px;
}

.tag-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background-color: #e0ffe0;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.nav-tabs {
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 180px;
  background-color: white;
  z-index: 100;
}

.nav-tabs ul {
  list-style: none;
  display: flex;
  padding: 0;
  margin: 0;
}

.tab-item {
  padding: 12px 16px;
  cursor: pointer;
  font-size: 14px;
}

.tab-item.active {
  color: #ff2442;
  border-bottom: 2px solid #ff2442;
}

.search-item input {
  padding: 6px;
  border: 1px solid #eee;
  border-radius: 4px;
  font-size: 12px;
}

.content-container {
  padding: 16px;
}

.tab-content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.media-item {
  display: flex;
  flex-direction: column;
}

.media-item img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 8px;
}

.media-desc {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.media-interaction {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
}
</style>