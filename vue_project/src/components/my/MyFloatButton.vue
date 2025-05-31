<template>
  <img 
    class="fab-image" 
    src="/images/icons/fabutie.svg" 
    alt="发布帖子" 
    @click="$emit('click')"
  >
</template>

<style scoped>
.fab-image {
  position: fixed;
  bottom: 80px;
  right: 20px;
  width: 56px;
  height: 56px;
  cursor: pointer;
  z-index: 1000;
}
</style>