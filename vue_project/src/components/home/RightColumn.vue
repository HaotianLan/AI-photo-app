<template>
  <div class="right-column">
    <div v-for="(post, index) in posts" :key="'right-'+index" class="post-container">
      <img
        :src="post.postImage"
        class="post-image"
        alt="Post image"
        @load="handleImageLoaded(index, post.aspectRatio)"
        @click="handlePostClick(post)"
      >
      <div class="post-footer">
        <div class="user-info">
          <img
            :src="post.avatarImage"
            class="avatar"
            alt="User avatar"
            @load="handleImageLoaded(index, post.aspectRatio)"
          >
          <span class="username">{{ post.username }}</span>
        </div>
        <button class="like-button">
          <img src="/images/icons/good.svg" class="like-icon">
          <span class="like-count">0</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  posts: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['image-loaded'])
const router = useRouter()

const handleImageLoaded = (index, aspectRatio) => {
  emit('image-loaded', index, aspectRatio)
}

const handlePostClick = (post) => {
  router.push({ name: 'post', params: { id: post.id } })
}
</script>

<style scoped>
.right-column {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-height: 0;
}

.post-container {
  display: flex;
  flex-direction: column;
  margin-bottom: 4px;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.user-info {
  display: flex;
  align-items: center;
}

.avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  margin-right: 8px;
}

.username {
  font-size: 12px;
  font-weight: 500;
}

.post-image {
  width: 100%;
  height: auto;
  display: block;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
}

.like-button {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  padding: 4px;
}

.like-icon {
  width: 16px;
  height: 16px;
  margin-right: 4px;
}
</style>