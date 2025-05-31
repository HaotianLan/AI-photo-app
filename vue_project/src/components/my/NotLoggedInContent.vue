<template>
  <div class="content-wrapper">
    <div class="user-info">
      <div class="user-header">
        <img class="avatar" src="/images/posts/1.jpg" alt="用户头像" />
        <div class="user-details">
          <div class="username">未登录</div>
          <div class="user-id">id: 未登录</div>
          <div class="user-ip">ip: 未登录</div>
        </div>
      </div>
      <div class="user-bio">请登录后查看完整功能</div>
      <div class="user-stats">
        <div class="stat-item">
          <span>0</span>
          <span>跟拍</span>
        </div>
        <div class="stat-item">
          <span>0</span>
          <span>关注</span>
        </div>
        <div class="stat-item">
          <span>0</span>
          <span>粉丝</span>
        </div>
        <div class="stat-item">
          <span>0</span>
          <span>获赞与收藏</span>
        </div>
      </div>
      <button class="login-btn" @click="handleLogin">登录</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const handleLogin = () => {
  router.push('/login')
}
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

.username {
  font-weight: bold;
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

.login-btn {
  width: 100%;
  padding: 8px;
  background-color: #f4f4f4;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 8px;
}
</style>
