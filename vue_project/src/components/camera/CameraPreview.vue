<template>
  <div class="camera-preview">
    <video ref="videoRef" autoplay playsinline class="video-element"></video>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Camera } from '@capacitor/camera';
import { Filesystem, Directory } from '@capacitor/filesystem';
import { Capacitor } from '@capacitor/core';

const videoRef = ref(null);
const photoUrl = ref(null);

const checkPermissions = async () => {
  if (Capacitor.isNativePlatform()) {
    const permissions = await Filesystem.checkPermissions();
    if (permissions.publicStorage !== 'granted') {
      const result = await Filesystem.requestPermissions();
      if (result.publicStorage !== 'granted') {
        throw new Error('存储权限被拒绝');
      }
    }
  }
};

const takePhoto = async () => {
  try {
    await checkPermissions();
    
    // 捕获390x723px的显示画面
    const video = videoRef.value;
    const canvas = document.createElement('canvas');
    
    // 设置canvas为显示区域尺寸
    canvas.width = 390;
    canvas.height = 723;
    
    const ctx = canvas.getContext('2d');
    
    // 计算缩放比例以填充显示区域
    const scale = Math.max(
      390 / video.videoWidth,
      723 / video.videoHeight
    );
    
    // 计算居中绘制位置
    const scaledWidth = video.videoWidth * scale;
    const scaledHeight = video.videoHeight * scale;
    const offsetX = (390 - scaledWidth) / 2;
    const offsetY = (723 - scaledHeight) / 2;
    
    // 绘制填充显示区域的画面
    ctx.drawImage(
      video,
      offsetX, offsetY, scaledWidth, scaledHeight
    );
    
    // 保存到相册
    const fileName = `IMG_${new Date().getTime()}.jpg`;
    const imageData = canvas.toDataURL('image/jpeg', 0.9);
    
    if (Capacitor.isNativePlatform()) {
      const savedFile = await Filesystem.writeFile({
        path: `Pictures/My3Photos/${fileName}`,
        data: imageData.split(',')[1],
        directory: Directory.ExternalStorage,
        recursive: true
      });
      
      console.log('照片已保存至相册:', savedFile.uri);
      return { success: true, path: savedFile.uri };
    } else {
      // Web端下载
      const link = document.createElement('a');
      link.href = imageData;
      link.download = fileName;
      link.click();
      return { success: true, path: fileName ,img:imageData};
    }
  } catch (error) {
    console.error('拍照失败:', error);
    return null;
  }
};

const startCamera = async () => {
  if (Capacitor.isNativePlatform()) {
    // 原生平台使用Capacitor相机
    return;
  }
  
  // Web平台回退到浏览器API
  if (navigator.mediaDevices?.getUserMedia) {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.value.srcObject = stream;
    } catch (error) {
      console.error('无法访问相机:', error);
    }
  }
};

const stopCamera = () => {
  if (!Capacitor.isNativePlatform() && videoRef.value?.srcObject) {
    videoRef.value.srcObject.getTracks().forEach(track => track.stop());
  }
};

defineExpose({
  startCamera,
  stopCamera,
  takePhoto
});

onMounted(() => {
  startCamera();
});
</script>

<style scoped>
.camera-preview {
  width: 100%;
  height: calc(100vh - 160px);
  background-color: #000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.video-element {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-preview {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>