<template>
  <PhoneFrame>
    <router-view />
  </PhoneFrame>
</template>

<script setup>
import PhoneFrame from './components/PhoneFrame.vue';
</script>

<style>
#app {
  height: 100vh;
}
body {
  margin: 0;
  padding: 0;
  background: #f5f5f5;
}
</style>
