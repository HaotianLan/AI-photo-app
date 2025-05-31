<template>
  <div class="comment-input-container">
    <input 
      type="text" 
      v-model="content" 
      placeholder="评论..." 
      class="comment-input"
      @keyup.enter="submitComment"
    >
    <div class="interaction-icons">
      <div class="icon-wrapper" @click="like">
        <img src="/images/icons/good.svg" alt="点赞" class="icon">
        <span>{{ likeCount }}</span>
      </div>
      <div class="icon-wrapper" @click="collect">
        <img src="/images/icons/huaban9.svg" alt="收藏" class="icon">
        <span>{{ collectCount }}</span>
      </div>
      <div class="icon-wrapper" @click="takePhoto">
        <img src="/images/icons/xiangji.svg" alt="即拍" class="icon">
        <span>{{ cameraCount }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const content = ref('')
const likeCount = ref(0)
const collectCount = ref(0)
const cameraCount = ref(0)

const emit = defineEmits(['submit'])

const submitComment = () => {
  if (content.value.trim()) {
    emit('submit', content.value)
    content.value = ''
  }
}

const like = () => {
  likeCount.value++
}

const collect = () => {
  collectCount.value++
}

const takePhoto = () => {
  cameraCount.value++
}
</script>

<style scoped>
.comment-input-container {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-top: 1px solid #eee;
  background: white;
  position: absolute;
  top: 750px;
  left: 0;
  right: 0;
  z-index: 100;
}

.comment-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #eee;
  border-radius: 18px;
  outline: none;
}

.interaction-icons {
  display: flex;
  align-items: center;
  gap: 12px;
}

.icon-wrapper {
  display: flex;
  align-items: center;
  gap: 2px;
  cursor: pointer;
}

.icon {
  width: 20px;
  height: 20px;
}

.icon-wrapper span {
  font-size: 12px;
  color: #666;
}
</style>