<template>
  <div class="phone-frame">
    <div class="screen-area">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.phone-frame {
  width: 390px;
  height: 844px;
  margin: 0 auto;
  position: relative;
  border: 2px solid #333;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 0 20px rgba(0,0,0,0.2);
  contain: strict;
  clip-path: inset(0);
}

.screen-area {
  position: absolute;
  top: 40px;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  overflow: hidden;
  contain: strict;
  clip-path: inset(0);
}

</style>