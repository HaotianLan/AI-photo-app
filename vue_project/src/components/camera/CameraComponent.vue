<template> 
  <div class="camera-container" ref="container">
    <!-- 相机预览组件 -->
    <CameraPreview ref="cameraPreview" />
    
    <!-- 顶部功能区组件 -->
    <CameraTopControls />
    <PromptComponent v-if="aiGuideOn" :prompt="currentPrompt" />
    <LinesComponent
      v-show="lineOn"
      :show="lineOn"
      :guide-image="selectedGuideImage"
      @mounted="console.log('LinesComponent已挂载, lineOn:', lineOn)"
    />

    <!-- 参考线栏组件 -->
    <GuideLineBar
      :visible="showGuideLine"
      @select="handleSelectGuide"
    />

    <!-- 中间功能开关区组件 -->
    <CameraMiddleControls
      :guide-on="lineOn"
      :ai-guide-on="aiGuideOn"
      :scan-result-visible="scanResultVisible"
      :scan-result-images="scanResultImages"
      @toggle-guide="handleToggleGuide"
      @select-guide="handleSelectGuide"
      @toggle-ai-guide="toggleAIGuide"
      @scan-and-upload="handleScanAndUpload"
      @modal-closed="scanResultVisible = false"
      @select="handleSelectImage"
      ref="cameraMiddleControls"
    />
    
    <!-- 底部操作区组件 -->
    <CameraBottomControls
      @takePhoto="handleTakePhoto"
      @openAlbum="handleOpenAlbum"
      ref="cameraBottomControls"
    />
    
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import CameraPreview from './CameraPreview.vue';
import CameraTopControls from './CameraTopControls.vue';
import PromptComponent from './PromptComponent.vue';
import LinesComponent from './LinesComponent.vue';
import CameraMiddleControls from './CameraMiddleControls.vue';
import CameraBottomControls from './CameraBottomControls.vue';
import CameraTransparentBar from './CameraTransparentBar.vue';
import GuideLineBar from './GuideLineBar.vue';
import axios from 'axios';

const cameraPreview = ref(null);
const cameraBottomControls = ref(null);
const cameraMiddleControls = ref(null);
const showGuideLine = ref(false);
const selectedGuideImage = ref(null);
const aiGuideOn = ref(false);

const lineOn = ref(false);
const container = ref(null);

const scanResultImages = ref([]);
const scanResultVisible = ref(false);

// 定义 currentPrompt 变量
const currentPrompt = ref('');

// 添加 watch 以跟踪 currentPrompt 的变化
watch(currentPrompt, (newValue, oldValue) => {
  console.log('currentPrompt 变化:', oldValue, '->', newValue);
});

// 添加 watch 以跟踪 aiGuideOn 的变化
watch(aiGuideOn, (newValue) => {
  console.log('aiGuideOn 状态:', newValue);
});

const handleToggleGuide = (visible) => {
  try {
    console.log('收到toggle-guide事件，新状态:', visible);
    lineOn.value = visible;
    console.log('更新后的lineOn状态:', lineOn.value);
    console.log('LinesComponent显示状态:', lineOn.value);
  } catch (error) {
    console.error('切换参考线失败:', error);
  }
};

const handleSelectGuide = (img) => {
  try {
    if (!img) {
      throw new Error('无效的图片路径');
    }
    selectedGuideImage.value = img;
    console.log('已选择参考图片:', img);
  } catch (error) {
    console.error('选择参考图片失败:', error);
  }
};

const handleTakePhoto = async () => {
  try {
    await cameraPreview.value.takePhoto();
  } catch (error) {
    console.error('拍照失败:', error);
  }
};

const handleOpenAlbum = () => {
  // 这里可以添加打开相册的逻辑
  console.log('打开相册查看已保存照片');
};

const toggleAIGuide = () => {
  aiGuideOn.value = !aiGuideOn.value;
  console.log('AI引导词状态:', aiGuideOn.value);
  console.log('PromptComponent显示状态:', aiGuideOn.value);
};

const handleScanAndUpload = async () => {
  try {
    const imageData = await cameraPreview.value.takePhoto();
    console.log('imageData:', imageData);
    const base64Data = imageData.img.split(',')[1]
    console.log('base64Data:', base64Data);
    const response = await axios.post('http://localhost:5001/ScanImage', {
      image: base64Data
    });

    const result = response.data;
    console.log('服务器返回的整体结果:', result);
    console.log('是否为数组:', Array.isArray(result));

    if (Array.isArray(result)) {
      scanResultImages.value = result;
      scanResultVisible.value = true;
      console.log('设置scanResultVisible为true');
      console.log('处理后scanResultImages:', scanResultImages.value);
    } else {
      console.error('服务器返回的数据不是数组:', result);
      // 使用默认测试图片
      scanResultImages.value = [
        {
          "Scanned_image": "/images/posts/1.jpg",
          "GuideLine_image": "/images/guides/1.jpg",
          "prompt": "这是示例提示词1"
        },
        {
          "Scanned_image": "/images/posts/2.jpg",
          "GuideLine_image": "/images/guides/2.jpg",
          "prompt": "这是示例提示词2"
        },
        {
          "Scanned_image": "/images/posts/3.jpg",
          "GuideLine_image": "/images/guides/3.jpg",
          "prompt": "这是示例提示词3"
        },
        {
          "Scanned_image": "/images/posts/4.jpg",
          "GuideLine_image": "/images/guides/4.jpg",
          "prompt": "这是示例提示词4"
        }
      ];
      scanResultVisible.value = true;
    }

    console.log('上传成功，服务器返回：', result);
  } catch (error) {
    console.error('拍照或上传失败:', error);
    // 使用默认测试图片
    scanResultImages.value = [
      {
        "Scanned_image": "/images/posts/1.jpg",
        "GuideLine_image": "/images/guides/1.jpg",
        "prompt": "这是示例提示词1"
      },
      {
        "Scanned_image": "/images/posts/2.jpg",
        "GuideLine_image": "/images/guides/2.jpg",
        "prompt": "这是示例提示词2"
      },
      {
        "Scanned_image": "/images/posts/3.jpg",
        "GuideLine_image": "/images/guides/3.jpg",
        "prompt": "这是示例提示词3"
      },
      {
        "Scanned_image": "/images/posts/4.jpg",
        "GuideLine_image": "/images/guides/4.jpg",
        "prompt": "这是示例提示词4"
      }
    ];
    scanResultVisible.value = true;
    console.log('网络错误时强制显示模态框');
    scanResultVisible.value = true;
  }
};
  
const handleSelectImage = (item) => {
  console.log('handleSelectImage - 接收到的项目:', item);
  
  // 检查 item 是否有效
  if (!item) {
    console.error('handleSelectImage - 接收到的项目为空');
    return;
  }
  
  // 检查 prompt 是否存在
  if (!item.prompt) {
    console.error('handleSelectImage - 项目中不存在 prompt 字段');
    console.log('项目内容:', item);
  } else {
    console.log('handleSelectImage - 项目中的 prompt:', item.prompt);
  }
  
  currentPrompt.value = item.prompt || '未找到提示词';
  console.log('handleSelectImage - 当前提示词:', currentPrompt.value);
  console.log('handleSelectImage - AI引导状态:', aiGuideOn.value);
  
  selectedGuideImage.value = item.GuideLine_image;

  let img = item.Scanned_image;
  if (typeof img === 'string' && !img.startsWith('http') && !img.startsWith('/')) {
    img = '/' + img;
  }

  if (cameraBottomControls.value) {
    cameraBottomControls.value.handleSelectImage(img);
  }
};
  
</script>

<style scoped>
.camera-container {
  position: relative;
  height: 100%;
  background-color: #fff;
  overflow: hidden;
}

.top-controls {
  margin-bottom: 0 !important;
}

.camera-container {
  position: relative;
  height: 100%;
  width: 100%;
  background-color: #fff;
  overflow: visible;
}

.prompt-container {
  position: absolute;
  margin-top: 0;
  top: 56px;
  left: 0;
  right: 0;
  z-index: 1000;
  display: block;
  opacity: 1;
  visibility: visible;
  height: 100px ;
}
</style>
