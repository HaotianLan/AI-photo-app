<template>
  <div class="top-controls">
    <!-- 返回按钮 -->
    <button class="icon-btn" @click="goBack">
      <img src="/images/icons/jiantou.svg" alt="返回">
    </button>

    <!-- 闪光灯按钮 - 三种状态 -->
    <button class="icon-btn" @click="cycleFlashMode">
      <img :src="flashMode === 'off' ? '/images/icons/sanguangoff.svg' :
            flashMode === 'auto' ? '/images/icons/sanguangauto.svg' :
            '/images/icons/sanguang.svg'" alt="闪光灯">
    </button>

    <!-- 倒计时按钮 -->
    <div class="timer-container">
      <button class="icon-btn" @click="showTimerMenu = !showTimerMenu">
        <img src="/images/icons/daoji.svg" alt="倒计时">
      </button>
      <div v-if="showTimerMenu" class="timer-menu">
        <button @click="setTimer(3)">3秒</button>
        <button @click="setTimer(5)">5秒</button>
        <button @click="setTimer(10)">10秒</button>
      </div>
    </div>

    <!-- Live图按钮 -->
    <button class="icon-btn" @click="liveOn = !liveOn">
      <img :src="liveOn ? '/images/icons/liveon.svg' : '/images/icons/liveoff.svg'" alt="Live">
    </button>

    <!-- 连拍按钮 -->
    <button class="icon-btn" @click="continuousShot = !continuousShot">
      <img :src="continuousShot ? '/images/icons/lianpaion.svg' : '/images/icons/lianpai.svg'" alt="连拍">
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// 顶部功能状态
const flashMode = ref('off'); // 'off'|'auto'|'on'
const showTimerMenu = ref(false);
const timerSeconds = ref(0);
const liveOn = ref(false);
const continuousShot = ref(false);

// 返回上一级
const goBack = () => {
  router.go(-1);
};

// 闪光灯模式循环切换
const cycleFlashMode = () => {
  if (flashMode.value === 'off') {
    flashMode.value = 'auto';
  } else if (flashMode.value === 'auto') {
    flashMode.value = 'on';
  } else {
    flashMode.value = 'off';
  }
  console.log('闪光灯模式:', flashMode.value);
};

// 设置倒计时
const setTimer = (seconds) => {
  timerSeconds.value = seconds;
  showTimerMenu.value = false;
  console.log('设置倒计时:', seconds + '秒');
};
</script>

<style scoped>
.top-controls {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #fff;
  border-bottom: 1px solid #eee;
  z-index: 10;
  box-sizing: border-box;
}

.timer-container {
  position: relative;
}

.timer-menu {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  background-color: #fff;
  border-radius: 8px;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 80px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.timer-menu button {
  background: none;
  border: none;
  color: #333;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  text-align: center;
}

.timer-menu button:hover {
  background-color: #f5f5f5;
}

.icon-btn {
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  padding: 0;
}

.top-controls .icon-btn img {
  width: 24px;
  height: 24px;
}
</style>