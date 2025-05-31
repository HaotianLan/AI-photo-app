<template>
  <div class="my-view">
    <MyHeader />
    <MyContent
      :activeTab="activeTab"
      :mediaList="mediaList"
      @update:activeTab="activeTab = $event"
    />
    <FooterBar />
    <MyFloatButton @click="goToCreatePost" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import FooterBar from '@/components/FooterBar.vue'
import MyHeader from '@/components/my/MyHeader.vue'
import MyContent from '@/components/my/MyContent.vue'
import MyFloatButton from '@/components/my/MyFloatButton.vue'

const router = useRouter()

const activeTab = ref('作品')

const mediaList = ref([
  {
    imageUrl: '/images/posts/1.jpg',
    description: '萌萌宝贝这样拍',
    viewCount: '浏览量：999+',
    likeCount: '点赞数：123'
  },
  {
    imageUrl: '/images/posts/2.jpg',
    description: '草地 鲜花 阳光',
    viewCount: '浏览量：123',
    likeCount: '点赞数：13'
  },
])
const goToCreatePost = () => {
  router.push('/create-post')
}
</script>

<style scoped>
.my-view {
  position: relative;
  max-width: 390px;
  margin: 0 auto;
  height: 100vh;
  overflow-y: auto;
  padding-bottom: 70px; /* 为底部导航栏留出空间 */
  background-color: white;
}
</style>