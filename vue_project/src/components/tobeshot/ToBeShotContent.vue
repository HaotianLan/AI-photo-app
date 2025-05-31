<template>
  <div class="group-content" style="height: calc(100vh - 200px)">
    <div
      v-for="group in groups"
      :key="group"
      class="group-section"
    >
      <div
        class="group-header"
        :class="{ active: activeGroup === group }"
        @click="toggleGroup(group)"
      >
        <span>{{ group }}</span>
        <img
          class="expand-icon"
          src="/images/icons/jiantou_1.svg"
          :class="{ rotated: expandedGroups[group] }"
        />
      </div>
      
      <div
        class="photo-grid"
        v-show="expandedGroups[group]"
      >
        <div v-for="(photo, index) in photos[group]" :key="index" class="photo-item">
          <img :lazy="true" :src="photo.src" :alt="`${group}照片`" style="width:100%;height:100%;display:block">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  groups: {
    type: Array,
    required: true
  },
  activeGroup: {
    type: String,
    required: true
  },
  expandedGroups: {
    type: Object,
    required: true
  },
  photos: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['toggleGroup'])

const toggleGroup = (group) => {
  emit('toggleGroup', group)
}
</script>

<style scoped>
.group-content {
  flex-grow: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.group-header {
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}

.group-header.active {
  color: #ff2442;
  background-color: #f9f9f9;
}

.group-section {
  margin-bottom: 8px;
}

.photo-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2px;
}

.photo-item {
  aspect-ratio: 1/1;
  overflow: hidden;
  position: relative;
}

.photo-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.expand-icon {
  width: 12px;
  height: 12px;
  margin-left: 4px;
  transition: transform 0.2s;
}

.expand-icon.rotated {
  transform: rotate(180deg);
}
</style>