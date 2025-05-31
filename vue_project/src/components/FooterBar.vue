2<template>
  <div class="footer-bar">
    <div class="nav-item" @click="navigate('home')">
      <img src="/images/icons/shouye.svg" alt="首页" class="nav-icon" />
      <span class="nav-text">首页</span>
    </div>
    <div class="nav-item" @click="navigate('checkin')">
      <img src="/images/icons/weizhi.svg" alt="打卡点" class="nav-icon" />
      <span class="nav-text">打卡点</span>
    </div>
    <div class="nav-item camera-item" @click="navigate('camera')">
      <div class="camera-circle">
        <img src="/images/icons/xiangji.svg" alt="发布" class="camera-icon" />
      </div>
    </div>
    <div class="nav-item" @click="navigate('toBeShot')">
      <img src="/images/icons/rukudengji.svg" alt="待拍" class="nav-icon" />
      <span class="nav-text">待拍</span>
    </div>
    <div class="nav-item" @click="navigate('profile')">
      <img src="/images/icons/xiazai.svg" alt="我的" class="nav-icon" />
      <span class="nav-text">我的</span>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const navigate = (path) => {
  router.push({ name: path })
}
</script>

<style scoped>
.footer-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  max-width: 390px;
  margin: 0 auto;
  display: flex;
  justify-content: space-around;
  align-items: center;
  background-color: white;
  padding: 0;
  height: 70px;
  z-index: 200;
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 20px;
  transition: all 0.2s;
  width: 20%;
}

.nav-item:hover {
  background-color: #f5f5f5;
}

.nav-icon {
  width: 24px;
  height: 24px;
}

.nav-text {
  font-size: 12px;
  margin-top: 6px;
  color: #666;
}

.camera-item {
  position: relative;
  width: 92px;
  height: 92px;
  margin-top: -46px;
}

.camera-circle {
  width: 85px;
  height: 85px;
  border-radius: 50%;
  background-color: white;
  border: 5px solid #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 -6px 15px rgba(0,0,0,0.15);
}

.camera-icon {
  width: 40px;
  height: 40px;
}
</style>
