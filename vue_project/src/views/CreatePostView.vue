<template>
  <div class="create-post-view">
    <div class="top-icons">
      <button class="close-icon" @click="closePage">
        <img src="/images/icons/jiantou.svg" alt="返回" class="back-icon">
      </button>
      <div class="right-section">
        <button class="draft-icon" @click="showDrafts">
          <img src="/images/icons/caogaoxiang.svg" alt="草稿箱" class="draft-icon-img">
          <span class="draft-text">我的草稿</span>
        </button>
      </div>
    </div>
    
    <div class="content-container">
      <button class="add-icon" @click="triggerFileInput">
            ＋
            <input
              type="file"
              ref="fileInput"
              accept="image/*"
              multiple
              @change="handleFileUpload"
              style="display: none"
            >
      </button>
      
      <!-- 图片预览区域 -->
      <div class="image-preview" v-if="uploadedImages.length > 0">
        <div class="preview-item" v-for="(image, index) in uploadedImages" :key="index">
          <img :src="image.preview" alt="上传的图片">
          <button class="remove-image" @click="removeImage(index)">×</button>
        </div>
      </div>

      <div class="input-section">
        <input type="text" v-model="title" placeholder="添加标题">
        <textarea v-model="content" placeholder="添加正文"></textarea>
      </div>
      
      <div class="tag-section">
        <div class="tag-label" @click="handleTagClick">#添加标签</div>
        <div class="location-input">
          <input
            type="text"
            v-model="tags"
            placeholder="标记位置（打卡点）"
          >
          <button class="location-btn" @click="handleLocationClick">📍</button>
        </div>
      </div>
    </div>
    
    <div class="visibility-section">
      <span>🔒是否公开可见</span>
      <label class="switch">
        <input type="checkbox" v-model="isPublic">
        <span class="slider round"></span>
      </label>
    </div>
    
    <div class="button-section">
      <button class="save-draft" @click="saveDraft">存草稿</button>
      <button class="publish" @click="publishWork" :disabled="!title || !content">
        发布作品
      </button>
    </div>
    
    <!-- 上传状态提示 -->
    <div class="upload-status" v-if="uploadStatus">
      {{ uploadStatus }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const title = ref('');
const content = ref('');
const tags = ref('');
const isPublic = ref(true);
const uploadedImages = ref([]);
const uploadStatus = ref('');
const fileInput = ref(null);

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileUpload = (e) => {
  const files = e.target.files;
  if (!files.length) return;

  uploadStatus.value = '正在上传图片...';
  
  // 模拟上传过程
  setTimeout(() => {
    Array.from(files).forEach(file => {
      const reader = new FileReader();
      reader.onload = (event) => {
        uploadedImages.value.push({
          file,
          preview: event.target.result
        });
      };
      reader.readAsDataURL(file);
    });
    uploadStatus.value = '上传完成!';
    setTimeout(() => uploadStatus.value = '', 2000);
  }, 1000);
};

const removeImage = (index) => {
  uploadedImages.value.splice(index, 1);
};

const saveDraft = () => {
  console.log('保存草稿', { 
    title: title.value, 
    content: content.value, 
    tags: tags.value,
    images: uploadedImages.value 
  });
};

const handleLocationClick = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        tags.value = `${tags.value ? tags.value + ' ' : ''}定位:${latitude.toFixed(6)},${longitude.toFixed(6)}`;
      },
      (error) => {
        console.error('获取位置失败:', error);
        tags.value = `${tags.value ? tags.value + ' ' : ''}定位失败`;
      }
    );
  } else {
    tags.value = `${tags.value ? tags.value + ' ' : ''}浏览器不支持定位`;
  }
};

const handleTagClick = () => {
  if (content.value && !content.value.endsWith('#')) {
    content.value += ' #';
  } else if (!content.value) {
    content.value = '#';
  }
};

const publishWork = () => {
  console.log('发布作品', {
    title: title.value,
    content: content.value,
    tags: tags.value,
    images: uploadedImages.value,
    isPublic: isPublic.value
  });
};

const closePage = () => {
  router.go(-1);
};
</script>

<style scoped>
.create-post-view {
  padding: 0;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  max-width: 100%;
  height: 100vh;
  margin: 0 auto;
  background-color: white;
  font-size: 16px;
  box-sizing: border-box;
  position: relative;
}

.create-post-view * {
  font-family: inherit;
  font-size: inherit;
}

.content-container {
  width: 100%;
  padding: 0;
  box-sizing: border-box;
}

.top-icons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  margin: 0;
}

.right-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.input-section {
  position: relative;
  padding: 0;
  margin: 16px 0;
  background: white;
  width: 100%;
  box-sizing: border-box;
}

.input-section .add-icon {
  position: absolute;
  left: 16px;
  top: 16px;
  margin: 0;
  z-index: 1;
}

.input-section input,
.input-section textarea {
  margin: 0;
  width: 100%;
  box-sizing: border-box;
  padding: 12px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  font: inherit;
}

.draft-icon {
  display: flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
}

.draft-icon-img {
  width: 18px;
  height: 18px;
}


.close-icon,
.add-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
  background-color: #f0f0f0;
  transition: all 0.2s;
  margin-top: 12px;
  margin-bottom: 12px;
}

.close-icon:hover {
  background-color: #ff6b6b;
  color: white;
}

.add-icon {
  width: 48px;
  height: 48px;
  border-radius: 4px;
  font-size: 24px;
  background-color: #f0f0f0;
  margin-left: 5%;
}

.add-icon:hover {
  background-color: #4dabf7;
  color: white;
}

.input-section {
  margin-bottom: 30px;
  background: white;
  border-radius: 8px;
  padding: 0 16px;
}

.input-section input {
  width: 100%;
  padding: 12px;
  border: none;
  border-bottom: 1px solid #f0f0f0;
  font-size: 16px;
  outline: none;
}

.input-section textarea {
  width: 100%;
  padding: 12px;
  border: none;
  font-size: 16px;
  min-height: 120px;
  resize: vertical;
  outline: none;
}

.input-section input:focus,
.input-section textarea:focus {
  border-color: #4dabf7;
  outline: none;
}

.input-section textarea {
  min-height: 120px;
  resize: vertical;
}

.tag-section {
  margin: 16px 0;
  width: 100%;
  box-sizing: border-box;
  padding: 0;
  font-size: 14px;
}

.tag-label {
  display: inline-block;
  padding: 6px 12px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 8px;
  cursor: pointer;
  color: #4dabf7;
  font-weight: bold;
}

.tag-label:hover {
  background-color: #e0e0e0;
}

.tag-section {
  padding: 0 16px;
  margin-bottom: 30px;
}

.tag-label {
  display: inline-block;
  padding: 6px 12px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 8px;
  cursor: pointer;
  color: #4dabf7;
  font-weight: bold;
}

.tag-section {
  padding: 0 16px;
  margin-bottom: 30px;
  width: calc(100%);
}

.location-input {
  position: relative;
  width: 100%;
}

.location-input input {
  width: 100%;
  padding: 12px 40px 12px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  box-sizing: border-box;
}

.location-input input:focus {
  outline: none;
  border-color: #4dabf7;
}

.location-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  padding: 0;
}

.location-btn:hover {
  color: #4dabf7;
}

.input-section input,
.input-section textarea {
  width: calc(100%);
  margin-bottom: 4px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  box-sizing: border-box;
}

.visibility-section {
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  background: white;
  border-radius: 8px;
  height: 48px;
}

.visibility-section span {
  color: #666;
  font-size: 14px;
  margin-right: 0px;
}

.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 26px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #4dabf7;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.button-section {
  display: flex;
  justify-content: flex-end;
  padding: 0 16px;
}

.save-draft,
.publish {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  margin-left: 15px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.2s;
}

.save-draft {
  background-color: #f0f0f0;
  color: #666;
}

.save-draft:hover {
  background-color: #e0e0e0;
}

.publish {
  background-color: #4dabf7;
  color: white;
}

.publish:hover:not(:disabled) {
  background-color: #339af0;
}

.publish:disabled {
  background-color: #e9ecef;
  color: #adb5bd;
  cursor: not-allowed;
}

.image-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 30px;
  padding: 0;
}

.preview-item {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 8px;
  overflow: hidden;
}

.preview-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 20px;
  height: 20px;
  border: none;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
}

.back-icon {
  width: 18px;
  height: 18px;
}

.upload-status {
  margin-top: 10px;
  color: #4dabf7;
  font-size: 14px;
  text-align: center;
}
</style>