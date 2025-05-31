<template>
  <div class="image-gallery-wrapper">
    <div class="image-gallery" :style="{ height: `${galleryHeight}px` }">
      <div v-if="images.length > 0" class="gallery-container" ref="gallery">
        <div
          v-for="(image, index) in images"
          :key="index"
          class="gallery-item"
          :style="{ transform: `translateX(${currentIndex * -100}%)` }"
          ref="items"
        >
          <img
            :src="image"
            :alt="'图片' + (index + 1)"
            class="gallery-image"
          />
        </div>
      </div>
    </div>
    <div v-if="images.length > 1" class="indicators">
      <div
        v-for="(_, index) in images"
        :key="index"
        class="indicator"
        :class="{ active: currentIndex === index }"
        @click="goToImage(index)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'

const props = defineProps({
  images: {
    type: Array,
    required: true,
    default: () => []
  }
})

const gallery = ref(null)
const items = ref([])
const currentIndex = ref(0)
const galleryHeight = ref(300)
const resizeObserver = ref(null)
let startX = 0
let isDragging = false

const updateHeight = () => {
  const activeItem = items.value[currentIndex.value]
  if (activeItem) {
    const img = activeItem.querySelector('img')
    if (img) {
      galleryHeight.value = Math.max(300, Math.min(img.clientHeight, 500))
    }
  }
}

const handleTouchStart = (e) => {
  startX = e.touches[0].clientX
  isDragging = true
}

const handleTouchMove = (e) => {
  if (!isDragging) return
  const currentX = e.touches[0].clientX
  const diff = startX - currentX
  
  if (diff > 50 && currentIndex.value < props.images.length - 1) {
    currentIndex.value++
    isDragging = false
  } else if (diff < -50 && currentIndex.value > 0) {
    currentIndex.value--
    isDragging = false
  }
}

const handleTouchEnd = () => {
  isDragging = false
}

const goToImage = (index) => {
  currentIndex.value = index
  nextTick(updateHeight)
}

onMounted(() => {
  resizeObserver.value = new ResizeObserver(updateHeight)
  items.value.forEach(item => {
    const img = item.querySelector('img')
    if (img) {
      resizeObserver.value.observe(img)
    }
  })

  if (gallery.value) {
    gallery.value.addEventListener('touchstart', handleTouchStart)
    gallery.value.addEventListener('touchmove', handleTouchMove)
    gallery.value.addEventListener('touchend', handleTouchEnd)
  }
})

onBeforeUnmount(() => {
  if (resizeObserver.value) {
    resizeObserver.value.disconnect()
  }
})
</script>

<style scoped>
.image-gallery-wrapper {
  position: relative;
  width: 320px;
  margin: 0 auto;
}

.image-gallery {
  position: relative;
  width: 100%;
  min-height: 300px;
  overflow: hidden;
  transition: height 0.3s ease;
  margin-bottom: 40px;
}

.gallery-container {
  display: flex;
  height: 100%;
  transition: transform 0.3s ease;
  overflow: hidden;
}

.gallery-item {
  flex: 0 0 320px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.gallery-image {
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
}

.indicators {
  position: absolute;
  bottom: -25px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  gap: 8px;
  z-index: 10;
  padding: 5px 0;
}

.indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #ccc;
  cursor: pointer;
  transition: background-color 0.3s;
}

.indicator.active {
  background-color: #ff2442;
  transform: scale(1.2);
}

.indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #ccc;
  cursor: pointer;
}

.indicator.active {
  background-color: #ff2442;
}
</style>