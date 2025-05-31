<template>
  <div class="bottom-actions">
    <button class="album-btn" @click="$event.preventDefault()">
      <transition name="fade">
        <img
          v-if="selectedImage"
          :src="selectedImage"
          class="selected-image"
          @click="handleSelectImage(null)"
        />
      </transition>
    </button>
    
    <!-- 拍摄按钮 -->
    <button
      class="shoot-circle"
      @click="handleTakePhoto"
      :class="{
        'taking-photo': isTakingPhoto
      }"
    />
    
    <button class="flip-btn" @click="flipCamera">
      <img src="/images/icons/fanzhuan.svg" alt="翻转">
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const emit = defineEmits(['takePhoto', 'selectImage']);

const selectedImage = ref(null);

// 接收并显示选中的图片
const handleSelectImage = (img) => {
  console.log('CameraBottomControls 收到图片:', img);
  selectedImage.value = img;
  emit('selectImage', img);
  console.log('CameraBottomControls 已更新selectedImage和触发selectImage事件');
  
  // 更新album-btn显示的图片
  const albumBtn = document.querySelector('.album-btn');
  if (albumBtn) {
    console.log('CameraBottomControls 找到album-btn元素');
    const imgElement = albumBtn.querySelector('img');
    if (imgElement) {
      console.log('CameraBottomControls 找到img元素，准备更新src');
      imgElement.src = img;
      imgElement.style.display = 'block';
      console.log('CameraBottomControls 已更新img元素src:', img);
    } else {
      console.error('CameraBottomControls 未找到img元素');
    }
  } else {
    console.error('CameraBottomControls 未找到album-btn元素');
  }
};

// 暴露方法给父组件
defineExpose({
  handleSelectImage
});

// 镜头翻转逻辑
const flipCamera = () => {
  console.log('执行镜头翻转操作');
  // 对接镜头翻转API
};

// 拍摄状态
const isTakingPhoto = ref(false);

// 拍照逻辑
const handleTakePhoto = async () => {
  isTakingPhoto.value = true;
  try {
    emit('takePhoto');
  } finally {
    isTakingPhoto.value = false;
  }
};
</script>

<style scoped>
.bottom-actions {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px;
  height: 160px;
  background-color: #fff;
  z-index: 5;
  box-sizing: border-box;
  border-top: 1px solid #eee;
}

.shoot-circle {
  position: absolute;
  left: 50%;
  bottom: 40px;
  transform: translate(-50%, 0);
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: #fffefe;
  border: 4px solid #ff8400;
  cursor: pointer;
  z-index: 100;
  margin: 0 auto;
}

.shoot-circle.taking-photo {
  background-color: #e7e7e7;
}


.shoot-circle:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.album-btn {
  width: 60px;
  height: 60px;
  border: none;
  border-radius: 8px;
  background-color: rgba(0, 0, 0, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  padding: 0;
}

.flip-btn {
  background: transparent;
  border: none;
  padding: 0;
  cursor: pointer;
  right:20px;
}

.flip-btn img {
  width: 48px;
  height: 48px;
}

.selected-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>