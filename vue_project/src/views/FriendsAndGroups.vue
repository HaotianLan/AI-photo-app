<template>
  <div class="friends-groups-page">
    <NavBar />
    <TabBar />
    <ChatList />
  </div>
</template>

<script setup>
import NavBar from '@/components/groups/NavBar.vue'
import TabBar from '@/components/groups/TabBar.vue'
import ChatList from '@/components/groups/ChatList.vue'
</script>

<style scoped>
.friends-groups-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #fff;
}

.icon {
  width: 20px;
  height: 20px;
  margin-right: 5px;
}
</style>