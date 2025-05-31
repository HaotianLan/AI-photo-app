<template>
  <div class="guide-line-bar" v-if="visible">
    <div class="fixed-item">
      <img :src="guideImages[0]" @click="selectImage(0)" />
    </div>
    <div class="scroll-container">
      <img 
        v-for="(img, index) in guideImages.slice(1)" 
        :key="index+1"
        :src="img"
        @click="selectImage(index+1)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['select']);

const guideImages = [
  '/images/posts/1.jpg?w=80&q=70',
  '/images/posts/2.jpg?w=80&q=70',
  '/images/posts/3.jpg?w=80&q=70',
  '/images/posts/4.jpg?w=80&q=70',
  '/images/posts/5.jpg?w=80&q=70',
  '/images/posts/6.jpg?w=80&q=70',
  '/images/posts/24 (1).jpg?w=80&q=70',
  '/images/posts/50 (1).jpg?w=80&q=70',
  '/images/posts/50 (2).jpg?w=80&q=70',
  '/images/posts/50 (3).jpg?w=80&q=70'
];

const selectImage = (index) => {
  emit('select', guideImages[index]);
};
</script>

<style scoped>
.guide-line-bar {
  position: absolute;
  bottom: 160px;
  left: 0;
  width: 100%;
  height: 60px;
  z-index: 10;
  padding: 10px 0;
  display: flex;
  background-color: transparent;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.fixed-item {
  width: 40px;
  height: 40px;
  margin-left: 20px;
  flex-shrink: 0;
  overflow: hidden;
  border-radius: 8px;
}

.fixed-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.scroll-container {
  display: flex;
  gap: 10px;
  padding: 0 10px;
  height: 100%;
  overflow-x: auto;
  flex-grow: 1;
}

.scroll-container img {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  object-fit: cover;
  flex-shrink: 0;
}
</style>