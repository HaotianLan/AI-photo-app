<template>
  <transition name="slide">
    <div
      v-if="isOpen"
      class="side-panel"
      @click.stop
    >
      <div class="panel-content">
        <!-- 用户信息部分 -->
        <div class="user-section">
          <div class="user-header">
            <img class="avatar" src="/images/posts/1.jpg" alt="用户头像">
            <div class="user-details">
              <div class="username">蜡笔小芯</div>
              <div class="user-id">id: 123456789</div>
            </div>
          </div>
        </div>

        <!-- 数据统计部分 -->
        <div class="stats-section">
          <div class="stats-container">
            <div class="stat-item">
              <div class="stat-value">123</div>
              <div class="stat-label">我的关注</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">456</div>
              <div class="stat-label">获得的赞</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">78</div>
              <div class="stat-label">我的评论</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">90</div>
              <div class="stat-label">我的收藏</div>
            </div>
          </div>
        </div>

        <!-- 功能列表部分 -->
        <div class="menu-section">
          <div class="menu-item">
            <img src="/images/icons/tianjiahaoyou.svg" alt="添加好友">
            <span>添加好友</span>
          </div>
          <div class="menu-item">
            <img src="/images/icons/zu.svg" alt="我的协作组">
            <span>我的协作组</span>
          </div>
          <div class="menu-item">
            <img src="/images/icons/fabu.svg" alt="发布作品">
            <span>发布作品</span>
          </div>
        </div>

        <!-- 底部按钮部分 -->
        <div class="bottom-section">
          <div class="bottom-item">
            <img src="/images/icons/saoyisao.svg" alt="扫一扫">
            <span>扫一扫</span>
          </div>
          <div class="bottom-item">
            <img src="/images/icons/pinglun.svg" alt="客服">
            <span>客服</span>
          </div>
          <div class="bottom-item">
            <img src="/images/icons/shezhi.svg" alt="设置">
            <span>设置</span>
          </div>
        </div>
      </div>
    </div>
  </transition>
  <div
    v-if="isOpen"
    class="overlay"
    @click="closePanel"
  />
</template>

<script setup>
defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close'])

const closePanel = () => {
  emit('close')
}
</script>

<style scoped>
.side-panel {
  position: absolute;
  top: 0;
  left: 0;
  width: 300px;
  height: 804px;
  background: white;
  z-index: 9999;
  box-shadow: 2px 0 10px rgba(0,0,0,0.1);
  border-right: 1px solid #eee;
  display: flex;
  flex-direction: column;
}

.panel-content {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.user-section {
  margin-bottom: 20px;
}

.user-header {
  display: flex;
  align-items: center;
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
  margin-bottom: 4px;
}

.user-id {
  font-size: 12px;
  color: #999;
}

.stats-section {
  margin-bottom: 20px;
}

.stats-container {
  display: flex;
  justify-content: space-between;
  background: #f5f5f5;
  border-radius: 12px;
  padding: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-weight: bold;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

.menu-section {
  flex: 1;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}

.menu-item img {
  width: 20px;
  height: 20px;
  margin-right: 12px;
}

.bottom-section {
  margin-top: auto;
  padding-top: 16px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-around;
}

.bottom-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 12px;
}

.bottom-item img {
  width: 24px;
  height: 24px;
  margin-bottom: 4px;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  z-index: 9998;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}
</style>