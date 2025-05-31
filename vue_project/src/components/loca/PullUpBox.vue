<template>
  <div class="pull-up-box" :style="$attrs.style">
    <div class="drag-handle" @pointerdown="handlePointerDown"></div>
    <div class="content">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// 移除本地高度控制，使用外部传入的样式

const props = defineProps({
  initialOpen: {
    type: Boolean,
    default: false
  }
})

const translateY = ref(0)
const startY = ref(0)
const isDragging = ref(false)

onMounted(() => {
  const fixedPosition = 500 // 固定在距离顶部500px处
  translateY.value = props.initialOpen ? 0 : fixedPosition
  // 确保初始状态下能看到部分内容
  if (translateY.value === fixedPosition) {
    document.querySelector('.pull-up-box').style.overflow = 'auto'
  }
})

const handlePointerDown = (e) => {
  isDragging.value = true
  startY.value = e.clientY
  document.addEventListener('pointermove', handlePointerMove)
  document.addEventListener('pointerup', handlePointerUp)
}

const handlePointerMove = (e) => {
  if (!isDragging.value) return
  const deltaY = e.clientY - startY.value
  translateY.value = Math.min(Math.max(deltaY, -500), 0) // 可拉到完全隐藏(translateY=500)或完全展开(translateY=0)
  
  // 防止地图缩放/移动时影响组件位置
  e.preventDefault()
  e.stopPropagation()
}

const handlePointerUp = () => {
  isDragging.value = false
  document.removeEventListener('pointermove', handlePointerMove)
  document.removeEventListener('pointerup', handlePointerUp)
  
  // 自动吸附到顶部或底部
  if (translateY.value > -250) { // 超过一半距离则完全展开
    translateY.value = 0
  } else { // 否则完全隐藏
    translateY.value = 500
  }
}

onMounted(() => {
  translateY.value = -window.innerHeight + 100
})

onUnmounted(() => {
  document.removeEventListener('pointermove', handlePointerMove)
  document.removeEventListener('pointerup', handlePointerUp)
})
</script>

<style scoped>
.pull-up-box {
  position: fixed;
  top: 460px;
  left: 50%;
  transform: translateX(-50%);
  width: 390px;
  max-width: 100vw;
  background-color: rgba(255, 255, 255, 0.95);
  border-radius: 16px 16px 0 0;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  backdrop-filter: blur(5px);
  pointer-events: auto;
  height: 100%;
  min-height: 400px;
  max-height: 100vh;
  overflow: hidden; /* 禁用外层滚动 */
  will-change: transform;
  clip-path: inset(0);
}


.pull-up-box.expanded {
  overflow-y: auto; /* 展开时才显示滚动条 */
}

.drag-handle {
  width: 100px;
  height: 2px;
  background-color: #e4e3e3;
  margin: 8px auto;
  cursor: grab;
  position: sticky;
  top: 0;
  z-index: 1001;
  padding: 2px 0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}

.content {
  padding: 5px 10px 10px; /* 上边距减小 */
  overflow-y: auto; /* 允许内容滚动 */
  height: 100%; /* 填充父容器高度 */
  min-height: 300px; /* 确保最小高度 */
}

.search-bar {
  position: fixed;
  top: 0;
  background: white;
}
</style>