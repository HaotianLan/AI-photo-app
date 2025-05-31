<template>
  <div class="home-content">
    <SidePanel
      :isOpen="showSidePanel"
      @close="showSidePanel = false"
    />
    <!-- 顶部固定区域 -->
    <div class="header-section">
      <SearchBar @openMenu="showSidePanel = true" />
      <TabBar :tabs="tabs" v-model="activeTab" />
    </div>
    
    <!-- 主要内容区域 -->
    <div class="content-wrapper">
      <div class="grid-container">
        <LeftColumn
          :posts="leftColumnPosts"
          @image-loaded="(index, aspectRatio) => handleImageLoaded('left', index, aspectRatio)"
        />
        <RightColumn
          :posts="rightColumnPosts"
          @image-loaded="(index, aspectRatio) => handleImageLoaded('right', index, aspectRatio)"
        />
      </div>
    </div>

    <!-- 底部导航 -->
    <FooterBar />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import SearchBar from '../components/home/SearchBar.vue'
import SidePanel from '../components/SidePanel.vue'

const showSidePanel = ref(false)
import TabBar from '../components/home/TabBar.vue'
import FooterBar from '../components/FooterBar.vue'
import { posts as postData } from '../data/posts'


// 移除重复的tab-bar实现
import LeftColumn from '../components/home/LeftColumn.vue'
import RightColumn from '../components/home/RightColumn.vue'
const tabs = ['精品', '关注', '推荐', '附近']
const activeTab = ref('推荐')

const leftColumnHeight = ref(0)
const rightColumnHeight = ref(0)
const leftColumnPosts = ref([])
const rightColumnPosts = ref([])
const tallPosts = ref([])

// 固定用户数据
const fixedUsers = [
  { avatar: '/images/posts/50.jpg', username: '泡泡盐汽水' },
  { avatar: '/images/posts/50 (2).jpg', username: '芝士奶盖茶' },
  { avatar: '/images/posts/50 (4).jpg', username: '芒果西米露' },
  { avatar: '/images/posts/50 (6).jpg', username: '草莓冰淇淋' },
  { avatar: '/images/posts/50 (8).jpg', username: '抹茶拿铁' }
];

const getFixedUserData = (id) => {
  return fixedUsers[id.charCodeAt(0) % fixedUsers.length];
};
const postList = [
  {
    id: '1',
    postImage: "/images/posts/24 (1).jpg"
  },
  {
    id: '2',
    postImage: "/images/posts/Camera_XHS_17438645653401040g008313li6ju2he505n58nl45sud2l1g4lmo.jpg"
  },
  {
    id: '3',
    postImage: "/images/posts/24 (3).jpg"
  },
  {
    id: '4',
    postImage: "/images/posts/24 (4).jpg"
  },
  {
    id: '5',
    postImage: "/images/posts/24 (5).jpg"
  },
  {
    id: '6',
    postImage: "/images/posts/24 (6).jpg"
  },
  {
    id: '7',
    postImage: "/images/posts/24 (7).jpg"
  },
  {
    id: '8',
    postImage: "/images/posts/24 (8).jpg"
  },
  {
    id: '9',
    postImage: "/images/posts/24 (9).jpg"
  },
  {
    id: '10',
    postImage: "/images/posts/50 (1).jpg"
  },
  {
    id: '11',
    postImage: "/images/posts/50 (2).jpg"
  },
  {
    id: '12',
    postImage: "/images/posts/50 (3).jpg"
  },
  {
    id: '13',
    postImage: "/images/posts/50 (4).jpg"
  },
  {
    id: '14',
    postImage: "/images/posts/50 (5).jpg"
  },
  {
    id: '15',
    postImage: "/images/posts/50 (6).jpg"
  },
  {
    id: '16',
    postImage: "/images/posts/50 (7).jpg"
  },
  {
    id: '17',
    postImage: "/images/posts/50 (8).jpg"
  },
  {
    id: '18',
    postImage: "/images/posts/50 (9).jpg"
  },
  {
    id: '19',
    postImage: "/images/posts/50.jpg"
  },
  {
    id: '20',
    postImage: "/images/posts/69 (1).jpg"
  }
];

// 移除随机头像相关代码

const loadImage = (url) => {
  return new Promise((resolve) => {
    const img = new Image()
    img.onload = () => {
      const aspectRatio = img.naturalHeight / img.naturalWidth
      resolve(aspectRatio)
    }
    img.src = url
  })
}

const handleImageLoaded = (column, index, actualAspectRatio) => {
  if (column === 'left') {
    leftColumnPosts.value[index].aspectRatio = actualAspectRatio
    leftColumnHeight.value = leftColumnPosts.value.reduce((sum, post) => sum + post.aspectRatio, 0)
  } else {
    rightColumnPosts.value[index].aspectRatio = actualAspectRatio
    rightColumnHeight.value = rightColumnPosts.value.reduce((sum, post) => sum + post.aspectRatio, 0)
  }
  
  // 不再自动重新平衡两列高度
  // 保持各自独立的高度计算
}

// 移除自动重新平衡功能
// 两列将保持独立的高度计算

onMounted(async () => {
  // 随机分配帖子给左右栏
  // 左边栏分配前10个帖子
  for (let i = 0; i < 10 && i < postList.length; i++) {
    const post = postList[i]
    const aspectRatio = await loadImage(post.postImage)
    const userData = getFixedUserData(post.id)
    leftColumnPosts.value.push({
      id: post.id,
      postImage: post.postImage,
      avatarImage: userData.avatar,
      aspectRatio: aspectRatio,
      username: userData.username
    })
    leftColumnHeight.value += aspectRatio
  }
  
  // 右边栏分配后10个不同的帖子
  for (let i = 10; i < 20 && i < postList.length; i++) {
    const post = postList[i]
    const aspectRatio = await loadImage(post.postImage)
    const userData = getFixedUserData(post.id)
    rightColumnPosts.value.push({
      id: post.id,
      postImage: post.postImage,
      avatarImage: userData.avatar,
      aspectRatio: aspectRatio,
      username: userData.username
    })
    rightColumnHeight.value += aspectRatio
  }
  
  // 处理剩余图片
  let leftCount = 0
  let rightCount = 0
  
  for (const post of postList) {
    // 跳过已处理的高图片
    if (tallPosts.value.some(tp => tp.post.id === post.id)) continue
    
    const aspectRatio = await loadImage(post.postImage)
    const userData = getFixedUserData(post.id)
    
    // 确保左边第二张是高图片
    if (leftCount === 1 && tallPosts.value[0]) {
      leftColumnPosts.value.splice(1, 0, {
        id: tallPosts.value[0].post.id,
        postImage: tallPosts.value[0].post.postImage,
        avatarImage: userData.avatar,
        aspectRatio: tallPosts.value[0].aspectRatio
      })
      leftColumnHeight.value += tallPosts[0].aspectRatio
      leftCount++
    }
    
    // 确保右边第三张是高图片
    if (rightCount === 2 && tallPosts[1]) {
      rightColumnPosts.value.splice(2, 0, {
        id: tallPosts[1].post.id,
        postImage: tallPosts[1].post.postImage,
        avatarImage: userData.avatar,
        aspectRatio: tallPosts[1].aspectRatio
      })
      rightColumnHeight.value += tallPosts[1].aspectRatio
      rightCount++
    }
    
    if (leftColumnHeight.value <= rightColumnHeight.value) {
      leftColumnPosts.value.push({
        id: post.id,
        postImage: post.postImage,
        avatarImage: userData.avatar,
        aspectRatio
      })
      leftColumnHeight.value += aspectRatio
      leftCount++
    } else {
      rightColumnPosts.value.push({
        id: post.id,
        postImage: post.postImage,
        avatarImage: userData.avatar,
        aspectRatio
      })
      rightColumnHeight.value += aspectRatio
      rightCount++
    }
  }
})
</script>

<style scoped>
.home-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 100%;
  overflow: auto;
}

/* 顶部固定区域 */
.header-section {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.tab-bar {
  display: flex;
  justify-content: space-around;
  padding: 5px 0;
  background: white;
  border-bottom: 1px solid #eee;
}

/* 主要内容区域 */
.content-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 4px 0;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: auto;
  gap: 4px; /* 统一间距为4px */
  margin-bottom: 4px;
  align-items: start; /* 确保项目从顶部对齐 */
}

.left-column {
  grid-column: 1;
  display: flex;
  flex-direction: column;
  row-gap: 4px;
  column-gap: 4px;
  min-height: 0; /* 防止flex容器高度限制 */
}

.right-column {
  grid-column: 2;
  display: flex;
  flex-direction: column;
  row-gap: 4px;
  column-gap: 4px;
  min-height: 0; /* 防止flex容器高度限制 */
}

.first-post {
  width: 100%;
}

.post-container {
  width: 100%;
  margin: 0 !important;
  contain: layout; /* 优化浏览器渲染 */
  overflow: visible; /* 确保内容不会被裁剪 */
}

.post-container img {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
  contain: content; /* 优化图片渲染 */
}

.post-item {
  width: 100%;
}
</style>