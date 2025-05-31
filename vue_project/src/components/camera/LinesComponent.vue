<template>
  <div class="lines-container" v-show="show" @vue:mounted="console.log('LinesComponent mounted, show:', show)">
    <img
      :src="guideImage"
      alt="参考线图片"
      class="lines-image"
      @load="handleImageLoad"
      @error="handleImageError"
    >
  </div>
</template>

<script>
export default {
  name: 'LinesComponent'
}
</script>

<script setup>
import { ref } from 'vue';

defineProps({
  show: {
    type: Boolean,
    default: false
  },
  guideImage: {
    type: String,
    default: ''
  }
});


const handleImageLoad = () => {
  console.log('参考线图片加载成功');
};

const handleImageError = () => {
  console.error('参考线图片加载失败');
};
</script>

<style scoped>
.lines-container {
  position: absolute;
  top: 60px;
  left: 0;
  right: 0;
  bottom: 180px;
  z-index: 1000;
  pointer-events: none;
  display: flex;
  justify-content: center;
  align-items: center;
}

.lines-image {
  max-width: 100%;
  max-height: 100%;
}
</style>