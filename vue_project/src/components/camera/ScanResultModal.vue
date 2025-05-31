<template>
  <Transition name="modal">
    <div v-show="show" class="modal-mask" @click.self="handleClose">
      <div class="modal-container">
        <div class="modal-header">
          <h3>扫描结果</h3>
        </div>
        <div class="modal-body" style="overflow-y: auto; max-height: 400px;">
          <div class="image-grid">
            <div
              class="image-column"
              v-for="(column, colIndex) in imageColumns"
              :key="colIndex"
            >
              <img
                v-for="(item, index) in column"
                :key="index"
                :src="item.Scanned_image"
                class="result-image"
                alt="扫描结果图像"
                @click="selectImage(item)"
                @error="handleImageError(item.Scanned_image)"
              />
            </div>
          </div>

        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  show: Boolean,
  results: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['close', 'select', 'modal-closed']);

// ✅ 分成左右两列
const imageColumns = computed(() => {
  const left = [];
  const right = [];
  props.results.forEach((item, index) => {
    if (index % 2 === 0) {
      left.push(item);
    } else {
      right.push(item);
    }
  });
  return [left, right];
});

function selectImage(item) {
  console.log('ScanResultModal 选中图片:', item);
  emit('select', item);
  emit('modal-closed');
}

function handleClose() {
  const modal = document.querySelector('.modal-container');
  const mask = document.querySelector('.modal-mask');
  modal.style.transition = 'transform 0.3s ease';
  modal.style.transform = 'translateY(100%)';
  mask.style.transition = 'opacity 0.3s ease, z-index 0s 0.3s';
  mask.style.opacity = '0';
  mask.style.zIndex = '-1';
  setTimeout(() => {
    emit('close');
    emit('modal-closed');
  }, 300);
}

function handleImageError(img) {
  console.error('Failed to load image:', img);
}
</script>


<style scoped>
.modal-mask {
  position: fixed;
  z-index: 1001;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-container {
  width: 360px;
  height: 500px;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 16px 16px 0 0;
  overflow: hidden;
  position: fixed;
  bottom: 0;
  left: 0;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.1);
  z-index: 1003;
  padding: 16px;
}

.modal-header {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 16px;
  color: #333;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.image-column {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 100px;
  flex: 1;
}

.result-image {
  width: 100%;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 8px;
  background-color: #eee;
  cursor: pointer;
  transition: transform 0.2s ease;
}
.result-image:hover {
  transform: scale(1.05);
}


.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  z-index: 999;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
}

.modal-close {
  font-size: 24px;
  background: none;
  border: none;
  cursor: pointer;
}

.modal-body {
  padding: 16px;
  flex: 1;
  overflow-y: auto;
  padding: 8px;
  overflow-y: auto;
}

.image-grid {
  display: flex;
  gap: 8px;
}

.image-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}


.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>