<template>
  <div class="filter-bar">
    <div class="select-wrapper">
      <select v-model="distanceFilter">
        <option value="1km内">1km内</option>
        <option value="5km内">5km内</option>
        <option value="10km内">10km内</option>
      </select>
      <img src="/images/icons/jiantou_1.svg" class="arrow-icon">
    </div>
    <div class="select-wrapper">
      <select v-model="sortFilter">
        <option value="按距离排序">按距离排序</option>
        <option value="按人气排序">按人气排序</option>
      </select>
      <img src="/images/icons/jiantou_1.svg" class="arrow-icon">
    </div>
    <div class="select-wrapper">
      <select v-model="typeFilter">
        <option value="人气地点">人气地点</option>
        <option value="景点">景点</option>
      </select>
      <img src="/images/icons/jiantou_1.svg" class="arrow-icon">
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const distanceFilter = ref('1km内')
const sortFilter = ref('按距离排序')
const typeFilter = ref('人气地点')
</script>

<style scoped>
.filter-bar {
  display: flex;
  justify-content: space-between;
  background-color: white;
  padding: 10px;
  border: none;
  box-shadow: none;
}

.select-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.filter-bar select {
  padding: 8px 25px 8px 12px;
  border: none;
  outline: none;
  background: transparent;
  appearance: none;
  -webkit-appearance: none;
  font-size: 14px;
}

.arrow-icon {
  position: absolute;
  right: 8px;
  width: 12px;
  height: 12px;
  pointer-events: none;
}

.expand-icon {
  width: 20px;
  height: 20px;
  margin-left: 10px;
  cursor: pointer;
}
</style>