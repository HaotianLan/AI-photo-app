<template>
  <div class="middle-controls">
    <ScanResultModal
      v-if="scanResultVisible"
      :show="scanResultVisible"
      :results="scanResultImages"
      @select="handleSelectImage"
      @modal-closed="$emit('modal-closed')"
      ref="scanResultModal"
    />
    <!-- 扫描中遮罩层 -->
    <ScanningOverlay :show="isScanning" />
    <!-- 左下角功能组 -->
    <div class="left-bottom-group">
      <div class="selected-guide" v-if="selectedGuide">
        <img :src="selectedGuide" alt="选中参考图">
      </div>
      <button class="icon-btn" @click="handleScanAndUpload">
        <img :src="scanOn ? '/images/icons/scanon.svg' : '/images/icons/scan.svg'" alt="场景扫描">
      </button>
      <button class="icon-btn" @click="toggleGuide">
        <img :src="lineOn ? '/images/icons/cankaoon.svg' : '/images/icons/cankaoxian.svg'" alt="参考线">
      </button>
      <button class="icon-btn" @click="toggleAIGuide">
        <img :src="aiGuideOn ? '/images/icons/aion.svg' : '/images/icons/aiyindao.svg'" alt="AI引导词">
      </button>
    </div>

    <!-- 右侧功能组 -->
    <div class="right-group">
      <button class="icon-btn" @click="toggleFilter">
        <img :src="filterOn ? '/images/icons/lvjinon.svg' : '/images/icons/lvjin.svg'" alt="滤镜">
      </button>
      <button class="icon-btn" @click="toggleBeauty">
        <img :src="beautyOn ? '/images/icons/meiyanon.svg' : '/images/icons/meiyan.svg'" alt="美颜">
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ScanResultModal from './ScanResultModal.vue';
import ScanningOverlay from './ScanningOverlay.vue';



const emit = defineEmits(['toggle-guide', 'select-guide', 'toggle-ai-guide', 'scan-and-upload', 'modal-closed', 'select']);

const handleScanAndUpload = () => {
  if (!scanOn.value) {
    isScanning.value = true;
    scanOn.value = true;

    // 通知父组件进行拍照 + 上传
    emit('scan-and-upload');

    setTimeout(() => {
      isScanning.value = false;
      console.log('场景扫描完成');
    }, 2000);
  } else {
    scanOn.value = false;
    isScanning.value = false;
  }
};

const props = defineProps({
  aiGuideOn: {
    type: Boolean,
    default: false
  },
  lineOn: {
    type: Boolean,
    default: false
  },
  scanResultVisible: {
    type: Boolean,
    default: false
  },
  scanResultImages: {
    type: Array,
    default: () => []
  }
});

const filterOn = ref(false);
const beautyOn = ref(false);
const scanOn = ref(false);
const isScanning = ref(false);
const lineOn = ref(false);
const selectedGuide = ref(null);

const toggleAIGuide = () => {
  const newState = !props.aiGuideOn;
  emit('toggle-ai-guide', newState);
  console.log(`AI引导状态: ${newState ? '开启' : '关闭'}`);
  // 这里可以对接AI提示词API
};

const toggleFilter = () => {
  filterOn.value = !filterOn.value;
  console.log('切换滤镜');
};

const toggleBeauty = () => {
  beautyOn.value = !beautyOn.value;
  console.log('切换美颜');
};

const toggleScan = () => {
  if (!scanOn.value) {
    isScanning.value = true;
    scanOn.value = true;
    
    // 模拟扫描过程
    setTimeout(() => {
      isScanning.value = false;
      console.log('场景扫描完成');
    }, 2000);
  } else {
    scanOn.value = false;
    isScanning.value = false;
  }
};

const toggleGuide = () => {
  lineOn.value = !lineOn.value;
  emit('toggle-guide', lineOn.value);
  console.log(`参考线状态: ${lineOn.value ? '开启' : '关闭'}`);
  console.log('触发toggle-guide事件，参数:', lineOn.value);
};

const selectGuide = (img) => {
  console.log('选择参考图片:', img);
  selectedGuide.value = img;
  emit('select-guide', img);
};

const handleSelectImage = (img) => {
  console.log('CameraMiddleControls 收到选中图片:', img);
  emit('select', img);
};

defineExpose({ selectGuide });
</script>

<style scoped>
.middle-controls {
  position: absolute;
  bottom: 240px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  z-index: 10;
}
.selected-guide {
  width: 40px;
  height: 40px;
  margin-right: 10px;
  border-radius: 8px;
  overflow: hidden;
}

.selected-guide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.left-bottom-group {
  position: absolute;
  left: 20px;
  bottom: 0;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.right-group {
  position: absolute;
  right: 20px;
  bottom: 0;
  display: flex;
  flex-direction: column;
  gap: 15px;
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

.icon-btn img {
  width: 24px;
  height: 24px;
}

.icon-btn.active {
  background-color: rgba(0, 122, 255, 0.2);
}

.icon-btn.active img {
  filter: sepia(1) saturate(5) hue-rotate(30deg);
}
</style>