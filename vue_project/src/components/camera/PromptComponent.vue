<template>
  <div class="prompt-container">
    <p>{{ prompt || '选择一张图片查看提示词...' }}</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineOptions({
  name: 'PromptComponent'
})

const props = defineProps({
  prompt: {
    type: String,
    default: ''
  }
});

// 添加调试日志
console.log('PromptComponent 渲染中，prompt:', props.prompt);
</script>

<style scoped>
.prompt-container {
  position: absolute;
  top: 56px; /* CameraTopControls高度 */
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 8px;
  text-align: center;
  z-index: 100;
  border-radius: 8px;
  margin: 0 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  word-wrap: break-word;
}

.prompt-container p {
  margin: 0;
  font-size: 14px;
  line-height: 1.4;
}
</style>
