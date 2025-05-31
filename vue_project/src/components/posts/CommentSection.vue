<template>
  <div class="comment-section">
    <!-- 评论列表 -->
    <div v-for="(comment, index) in visibleComments" :key="comment.id || index" class="comment-item">
      <div class="user-info">
        <img :src="comment.avatar" class="avatar" alt="用户头像">
        <span class="username">{{ comment.username }}</span>
      </div>
      <div class="comment-content">
        <p>{{ comment.content }}</p>
      </div>
      <div class="comment-meta">
        <span>{{ comment.time }}</span>
        <span>{{ comment.ip }}</span>
        <span @click="replyComment(index)">回复</span>
      </div>
      
      <!-- 回复列表 -->
      <div v-if="comment.replies && comment.replies.length" class="replies">
        <div v-for="(reply, replyIndex) in comment.replies" :key="replyIndex" class="reply-item">
          <div class="user-info">
            <img :src="reply.avatar" class="avatar" alt="用户头像">
            <span class="username">{{ reply.username }}</span>
          </div>
          <div class="comment-content">
            <p>{{ reply.content }}</p>
          </div>
          <div class="comment-meta">
            <span>{{ reply.time }}</span>
            <span>{{ reply.ip }}</span>
          </div>
        </div>
      </div>
    </div>
    <div v-if="hasMore" class="load-more" @click="loadMore">
      加载更多
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  comments: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['reply'])

const pageSize = 10
const currentPage = ref(1)

const visibleComments = computed(() => {
  return props.comments.slice(0, pageSize * currentPage.value)
})

const hasMore = computed(() => {
  return props.comments.length > visibleComments.value.length
})

const loadMore = () => {
  currentPage.value += 1
}

const replyComment = (index) => {
  emit('reply', index)
}
</script>

<style scoped>
.comment-section {
  border-top: 1px solid #eee;
  padding: 10px;
  will-change: transform;
}

.comment-item {
  border-bottom: 1px solid #eee;
  padding: 10px 0;
  margin-bottom: 10px;
  contain: content;
}

.replies {
  margin-left: 20px;
  padding-left: 15px;
  border-left: 2px solid #f0f0f0;
}

.reply-item {
  padding: 8px 0;
  margin-top: 8px;
  contain: content;
}

.reply-item .avatar {
  width: 24px;
  height: 24px;
}

.reply-item .username {
  font-size: 13px;
}

.reply-item .comment-content p {
  font-size: 13px;
  color: #666;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-bottom: 5px;
}

.avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: cover;
}

.username {
  font-size: 14px;
  color: #000;
}

.comment-content p {
  margin: 0;
  font-size: 14px;
  line-height: 1.4em;
}

.comment-meta {
  font-size: 12px;
  color: #666;
  margin-top: 5px;
  display: flex;
  gap: 10px;
}

.comment-meta span:last-child {
  color: #98bec7;
  cursor: pointer;
}

.load-more {
  text-align: center;
  padding: 10px;
  color: #666;
  cursor: pointer;
}
</style>