<template>
  <div class="header">
    <h1>我的待拍</h1>
    <div class="header-actions">
      <button class="batch-import-btn" @click="handleBatchImport">
        批量导入
      </button>
      <img class="settings-icon" src="/images/icons/shezhi.svg" alt="设置">
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['batchImport'])

const handleBatchImport = () => {
  emit('batchImport')
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 0;
  background: white;
  z-index: 100;
}

.header h1 {
  margin: 0;
  font-size: 18px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-right: -8px;
}

.batch-import-btn {
  padding: 6px 12px;
  background-color: #f4f4f4;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.settings-icon {
  width: 20px;
  height: 20px;
  cursor: pointer;
}
</style>