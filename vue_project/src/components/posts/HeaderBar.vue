<template>
  <div class="header">
    <div class="left-section">
      <div class="back-arrow" @click="goBack">
        <img src="/images/icons/jiantou.svg" alt="返回" />
      </div>
      <div class="user-info">
        <img
          :src="props.userAvatar"
          alt="用户头像"
          class="user-avatar"
          @error="handleImageError"
        />
        <span class="username">{{ props.username }}</span>
      </div>
    </div>
    <div class="action-buttons">
      <button v-if="!isFollowing" @click="followUser">关注</button>
      <button v-else @click="unfollowUser">已关注</button>
      <img src="/images/icons/fenxiang.svg" alt="分享" class="share-icon" />
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps({
  userAvatar: {
    type: String,
    default: '/images/icons/guanxi.svg'
  },
  username: {
    type: String,
    default: ''
  },
  isFollowing: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['follow', 'unfollow'])

const followUser = () => {
  emit('follow')
}

const unfollowUser = () => {
  emit('unfollow')
}

const goBack = () => {
  router.push('/')
}

const handleImageError = (e) => {
  e.target.src = '/images/icons/guanxi.svg'
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: #f8f8f8;
  border-bottom: 1px solid #eee;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 15px;
  flex: 1;
}

.back-arrow img {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-right: auto;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: 10px;
}

.action-buttons button {
  padding: 4px 12px;
  border: none;
  border-radius: 15px;
  background-color: #ff2442;
  color: white;
  font-size: 12px;
}

.share-icon {
  width: 20px;
  height: 20px;
}
</style>