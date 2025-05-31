<template>
  <div class="checkin-view">
    <!-- 地图容器 -->
    <div id="map-container" class="map-container">
      <iframe v-if="mapUrl" :src="mapUrl" style="width: 100%; height: 100%; border: none"></iframe>
      <div v-else class="map-placeholder">
        {{ loading ? '正在获取位置信息...' : error ? '无法加载地图' : '地图加载中...' }}
      </div>
    </div>

    <!-- 可拉起的面板 -->
    <PullUpBox
      ref="pullUpBox"
      :initial-open="true"
      :style="{
        top: isExpanded ? '0px' : '460px',
        height: isExpanded ? '890px' : '200px',
      }"
    >
      <template #default>
        <div class="sticky-header">
          <CheckinSearchBar @toggle="toggleExpand()" />
          <FilterBar />
          <div v-if="currentLocation" class="location-status">
            当前位置: {{ formatLocation(currentLocation) }}
            <button @click="refreshLocation" class="refresh-btn">刷新位置</button>
          </div>
        </div>
        <div class="scroll-content">
          <div v-if="loading" class="status-message">
            <p>正在获取附近的打卡点...</p>
          </div>
          <div v-else-if="error" class="status-message error">
            <p>{{ error }}</p>
            <button @click="refreshLocation" class="retry-btn">重试</button>
          </div>
          <LocationItem
            v-else
            v-for="(location, index) in locations"
            :key="index"
            :location="location"
          />
        </div>
      </template>
    </PullUpBox>

    <!-- 底部导航栏 -->
    <FooterBar class="footer-bar" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, provide } from 'vue'
import {
  getCurrentLocation,
  getNearbyPOIs,
  watchLocation,
  clearLocationWatch,
} from '@/services/locationService'
import CheckinSearchBar from '@/components/loca/CheckinSearchBar.vue'
import FilterBar from '@/components/loca/FilterBar.vue'
import LocationItem from '@/components/loca/LocationItem.vue'
import PullUpBox from '@/components/loca/PullUpBox.vue'
import FooterBar from '@/components/FooterBar.vue'

const locations = ref([])
const loading = ref(true)
const error = ref(null)
const mapUrl = ref(null)
const currentLocation = ref(null)
const watchId = ref(null)
const updateTimer = ref(null)

// 格式化位置信息显示
const formatLocation = (location) => {
  if (!location) return '未知'
  return `${location.longitude.toFixed(6)}, ${location.latitude.toFixed(6)}`
}

// 获取位置和附近打卡点
async function fetchNearbyLocations(location = null) {
  try {
    if (!location) {
      loading.value = true
      error.value = null
      location = await getCurrentLocation()
    }

    currentLocation.value = location
    console.log('当前位置:', location)

    // 获取附近打卡点
    const nearbyPOIs = await getNearbyPOIs(location)
    console.log('附近POI:', nearbyPOIs)

    locations.value = nearbyPOIs
    if (nearbyPOIs[0]?.mapUrl) {
      mapUrl.value = nearbyPOIs[0].mapUrl
    }
  } catch (err) {
    error.value = err.message || '获取位置信息失败，请检查位置权限设置'
    console.error('位置获取错误:', err)
  } finally {
    loading.value = false
  }
}

// 处理位置更新
const handleLocationUpdate = async (location) => {
  currentLocation.value = location
  // 使用节流，避免频繁更新
  if (updateTimer.value) {
    clearTimeout(updateTimer.value)
  }
  updateTimer.value = setTimeout(() => {
    fetchNearbyLocations(location)
  }, 10000) // 10秒节流
}

// 开始位置监听
const startLocationWatch = () => {
  if (watchId.value) {
    clearLocationWatch(watchId.value)
  }

  watchId.value = watchLocation(handleLocationUpdate, (error) => {
    console.error('位置监听错误:', error)
    error.value = error.message
  })
}

// 刷新位置信息
const refreshLocation = () => {
  if (watchId.value) {
    clearLocationWatch(watchId.value)
  }
  fetchNearbyLocations()
  startLocationWatch()
}

// 组件挂载时启动位置监听
onMounted(() => {
  fetchNearbyLocations()
  startLocationWatch()
})

// 组件卸载时清理
onUnmounted(() => {
  if (watchId.value) {
    clearLocationWatch(watchId.value)
  }
  if (updateTimer.value) {
    clearTimeout(updateTimer.value)
  }
})

const pullUpBox = ref(null)
const isExpanded = ref(false)

const toggleExpand = (forceState) => {
  if (typeof forceState !== 'undefined') {
    isExpanded.value = forceState
  } else {
    isExpanded.value = !isExpanded.value
  }
}

provide('toggleExpand', toggleExpand)
</script>

<style scoped>
.checkin-view {
  position: relative;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  padding-bottom: 60px;
  box-sizing: border-box;
  background: transparent;
}

.footer-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 200;
}

.pull-up-box {
  z-index: 100;
}

.map-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.content-container {
  position: relative;
  z-index: 2;
  background: transparent;
  pointer-events: none;
}

.pull-up-content {
  pointer-events: auto;
}

/* 确保地图容器可见 */
.map-container {
  z-index: 1;
}

/* 确保内容面板可见 */
/* 删除重复的location-list样式 */

.map-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #e0f7fa;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #333;
  font-size: 18px;
  z-index: 1;
}

.pull-up-content {
  position: relative;
  z-index: 100;
  width: 390px;
  margin-top: 776px;
}

.sticky-header {
  position: sticky;
  top: -20px;
  background: white;
  z-index: 10;
  padding: 10px;
  margin: 0;
  box-shadow: none;
  border: none;
  border-radius: 8px;
  transform: translateY(0);
}

.scroll-content {
  padding: 10px;
  padding-top: 0;
  padding-bottom: 20px;
  overflow-y: auto;
}

.loading-state,
.error-state {
  padding: 20px;
  text-align: center;
  color: #666;
}

.error-state {
  color: #f44336;
}

.status-message {
  padding: 20px;
  text-align: center;
  color: #666;
}

.status-message.error {
  color: #f44336;
}

.location-status {
  padding: 8px 12px;
  font-size: 12px;
  color: #666;
  background-color: #f5f5f5;
  border-radius: 4px;
  margin: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.refresh-btn,
.retry-btn {
  padding: 4px 12px;
  border: none;
  border-radius: 4px;
  background-color: #1976d2;
  color: white;
  cursor: pointer;
  font-size: 12px;
}

.refresh-btn:hover,
.retry-btn:hover {
  background-color: #1565c0;
}

.map-placeholder {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  color: #666;
}
</style>
