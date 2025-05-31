<template>
  <div class="to-be-shot-view">
    <ToBeShotHeader @batchImport="handleBatchImport" />
    <ToBeShotContent
      :groups="groups"
      :activeGroup="activeGroup"
      :expandedGroups="expandedGroups"
      :photos="photos"
      @toggleGroup="toggleGroup"
      @photoClick="handlePhotoClick"
    />
    <FooterBar />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import FooterBar from '@/components/FooterBar.vue'
import ToBeShotHeader from '@/components/tobeshot/ToBeShotHeader.vue'
import ToBeShotContent from '@/components/tobeshot/ToBeShotContent.vue'

// 群组列表
const groups = ref(['无分组', '校园拍摄', '日系拍摄', '情侣拍摄', '古风拍摄'])
const activeGroup = ref('无分组')
const expandedGroups = ref({
  '无分组': true,
  '校园拍摄': false,
  '日系拍摄': false,
  '情侣拍摄': false,
  '古风拍摄': false
})

// 模拟照片数据
const photos = {
  '无分组': [
    { id: 1, src: './images/posts/1.jpg' },
    { id: 2, src: './images/posts/2.jpg' },
    { id: 3, src: './images/posts/3.jpg' },
    { id: 4, src: './images/posts/4.jpg' },
    { id: 5, src: './images/posts/5.jpg' },
    { id: 6, src: './images/posts/6.jpg' }
  ],
  '校园拍摄': [
    { id: 24, src: './images/posts/24 (1).jpg' },
    { id: 25, src: './images/posts/24 (2).jpg' },
    { id: 26, src: './images/posts/24 (3).jpg' },
    { id: 27, src: './images/posts/24 (4).jpg' },
    { id: 28, src: './images/posts/24 (5).jpg' },
    { id: 29, src: './images/posts/24 (6).jpg' }
  ],
  '日系拍摄': [
    { id: 50, src: './images/posts/50 (1).jpg' },
    { id: 51, src: './images/posts/50 (2).jpg' },
    { id: 52, src: './images/posts/50 (3).jpg' },
    { id: 53, src: './images/posts/50 (4).jpg' },
    { id: 54, src: './images/posts/50 (5).jpg' },
    { id: 55, src: './images/posts/50 (6).jpg' }
  ],
  '情侣拍摄': [
    { id: 69, src: './images/posts/69 (1).jpg' },
    { id: 70, src: './images/posts/Camera_XHS_17438642158901040g008318eebmdkk63g48ei1rp1kqlbmle1g7o.jpg' },
    { id: 71, src: './images/posts/Camera_XHS_17438642307521040g008310av1all6a0g5o8sg4a08d5f1v9j3lg.jpg' },
    { id: 72, src: './images/posts/Camera_XHS_17438642330241040g008310av1all6a105o8sg4a08d5fn6pktr8.jpg' },
    { id: 73, src: './images/posts/Camera_XHS_17438645475811040g008313li6ju2he0g5n58nl45sud2o305l6g.jpg' },
    { id: 74, src: './images/posts/Camera_XHS_17438645653401040g008313li6ju2he505n58nl45sud2l1g4lmo.jpg' }
  ],
  '古风拍摄': [
    { id: 75, src: './images/posts/Camera_XHS_17438645475811040g008313li6ju2he0g5n58nl45sud2o305l6g.jpg' },
    { id: 76, src: './images/posts/Camera_XHS_17438645616841040g008313li6ju2he405n58nl45sud2plovqk8.jpg' },
    { id: 77, src: './images/posts/Camera_XHS_17438645653401040g008313li6ju2he505n58nl45sud2l1g4lmo.jpg' },
    { id: 78, src: './images/posts/Camera_XHS_17438645843841040g2sg31b3kmqrpmu204a6op6cdsulq3k7big0.jpg' }
  ]
}

// 切换分组展开状态
const toggleGroup = (group) => {
  activeGroup.value = group
  expandedGroups.value[group] = !expandedGroups.value[group]
}

// 批量导入功能
const handleBatchImport = () => {
  console.log('执行批量导入功能')
}


const router = useRouter()

// 处理照片点击
const handlePhotoClick = (id) => {
  router.push(`/spot/${id}`)
}
</script>

<style scoped>
.to-be-shot-view {
  max-width: 390px; 
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}

.to-be-shot-view {
  max-width: 390px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  height: 100vh - 300px;
}
</style>