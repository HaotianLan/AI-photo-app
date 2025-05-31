·<template>
  <div class="head-bar">
    <div class="head-bar-item" @click="goBack">
      <img src="/images/icons/jiantou.svg" class="head-bar-icon">
    </div>
  </div>
  <div class="nav-bar">
    <div class="nav-item">
      <div class="nav-icon-wrapper">
        <img src="/images/icons/heart-icon.svg" class="nav-icon">
        <span>赞和收藏</span>
      </div>
    </div>
    <div class="nav-item">
      <div class="nav-icon-wrapper">
        <img src="/images/icons/tianjiahaoyou.svg" class="nav-icon">
        <span>新增关注 <span class="badge">{{ newFollowCount }}</span></span>
      </div>
    </div>
    <div class="nav-item">
      <div class="nav-icon-wrapper">
        <img src="/images/icons/pinglun.svg" class="nav-icon">
        <span>评论和@</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const newFollowCount = ref(8);

const goBack = () => {
  router.go(-1);
};
</script>

<style scoped>
.head-bar {
  display: flex;
  align-items: center;
  height: 40px;
  background-color: #f8f8f8;
  padding-left: 10px;
  padding-top: 10px;
}
.nav-bar {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 70px;
  background-color: #f8f8f8;
  padding-bottom: 10px;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.nav-icon-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
}

.nav-icon {
  width: 24px;
  height: 24px;
}

.badge {
  background-color: red;
  color: #fff;
  border-radius: 50%;
  padding: 2px 5px;
  font-size: 12px;
}
</style>