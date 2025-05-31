<template>
  <div class="location-item" @click="handleClick">
    <div class="item-image"></div>
    <div class="item-info">
      <h3>{{ location.name }}</h3>
      <p>距离{{ location.distance }}，步行{{ location.walkTime }}min</p>
      <p>{{ location.takenCount }}拍过，{{ location.viewedCount }}人浏览过</p>
      <p>"{{ location.tagline }}"</p>
    </div>
    <img class="heart-icon" src="/images/icons/heart-icon.svg" alt="爱心图标" />
  </div>
</template>

<script setup>

import { useRouter } from 'vue-router'

const router = useRouter()
const props = defineProps({
  location: {
    type: Object,
    required: true,
  },
})

const handleClick = () => {
  console.log('Location clicked:', props.location)
  console.log('Location clicked:', props.location.images)

  // 将整个 location 对象传入路由状态中
  router.push({
    name: 'spot-detail',
    params: { id: props.location.id },
    query: {
      name: props.location.name,
      distance: props.location.distance,
      walkTime: props.location.walkTime,
      takenCount: props.location.takenCount,
      viewedCount: props.location.viewedCount,
      tagline: props.location.tagline,
      avatarImage: props.location.avatarImage,
      mapUrl: props.location.mapUrl,
      images: JSON.stringify(props.location.images),
    },
  })
}
</script>


<style scoped>
.location-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
}

.item-image {
  width: 80px;
  height: 80px;
}

.item-info {
  flex: 1;
}

.item-info h3 {
  margin: 0;
  font-size: 16px;
}

.item-info p {
  margin: 5px 0;
  font-size: 14px;
}

.heart-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
}
</style>
