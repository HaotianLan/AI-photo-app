<template>
  <div class="not-logged-in-view">
    <MyHeader />
    <NotLoggedInContent />
    <FooterBar />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import MyHeader from '@/components/my/MyHeader.vue'
import NotLoggedInContent from '@/components/my/NotLoggedInContent.vue'
import FooterBar from '@/components/FooterBar.vue'

const router = useRouter()
</script>

<style scoped>
.not-logged-in-view {
  position: relative;
  max-width: 390px;
  margin: 0 auto;
  height: 100vh;
  overflow-y: auto;
  padding-bottom: 70px;
  background-color: white;
}
</style>
