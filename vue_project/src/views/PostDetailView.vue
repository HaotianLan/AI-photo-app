<template>
  <div class="post-detail">
    <HeaderBar
      :user-avatar="userAvatar"
      :username="username"
      :is-following="isFollowing"
      @follow="followUser"
      @unfollow="unfollowUser"
    />

    <div class="post-content">
      <ImageGallery :images="postImages" />
      <PostContent
        :title="postTitle"
        :text="postText"
        :tags="tags"
        :time="postTime"
        :ip="postIp"
      />
      <CommentSection :comments="comments" @reply="handleReply" />
    </div>

    <CommentInput
      @submit="submitComment"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { posts } from '@/data/posts.js' // 假设帖子数据存放在这里
import HeaderBar from '@/components/posts/HeaderBar.vue'
import ImageGallery from '@/components/posts/ImageGallery.vue'
import PostContent from '@/components/posts/PostContent.vue'
import CommentSection from '@/components/posts/CommentSection.vue'
import CommentInput from '@/components/posts/CommentInput.vue'

const router = useRouter()
const route = useRoute()

const userAvatar = ref('')
const username = ref('')
const isFollowing = ref(false)
const postImages = ref([])
const postTitle = ref('')
const postText = ref('')
const tags = ref([])
const postTime = ref('')
const postIp = ref('')
const comments = ref([
  {
    id: 1,
    avatar: '/images/posts/Camera_XHS_17438642307521040g008310av1all6a0g5o8sg4a08d5f1v9j3lg.jpg',
    username: '用户1',
    content: '这个帖子内容很棒！',
    time: '10分钟前',
    ip: 'IP属地：北京',
    replies: [
      {
        avatar: '/images/posts/50 (1).jpg',
        username: '用户3',
        content: '同意，学到了很多',
        time: '8分钟前',
        ip: 'IP属地：广州'
      }
    ]
  },
  {
    id: 2,
    avatar: '/images/posts/Camera_XHS_17438642330241040g008310av1all6a105o8sg4a08d5fn6pktr8.jpg',
    username: '用户2',
    content: '我也觉得不错，点赞！',
    time: '5分钟前',
    ip: 'IP属地：上海',
    replies: [
      {
        avatar: '/images/posts/50 (2).jpg',
        username: '用户4',
        content: '确实很实用',
        time: '3分钟前',
        ip: 'IP属地：北京'
      },
      {
        avatar: '/images/posts/50 (3).jpg',
        username: '用户5',
        content: '已收藏',
        time: '1分钟前',
        ip: 'IP属地：深圳'
      }
    ]
  },
  {
    id: 3,
    avatar: '/images/posts/50 (4).jpg',
    username: '用户6',
    content: '照片拍得真好看',
    time: '15分钟前',
    ip: 'IP属地：杭州'
  },
  {
    id: 4,
    avatar: '/images/posts/50 (5).jpg',
    username: '用户7',
    content: '构图很有创意',
    time: '12分钟前',
    ip: 'IP属地：成都'
  },
  {
    id: 5,
    avatar: '/images/posts/50 (6).jpg',
    username: '用户8',
    content: '光线处理得真好',
    time: '9分钟前',
    ip: 'IP属地：武汉'
  },
  {
    id: 6,
    avatar: '/images/posts/50 (7).jpg',
    username: '用户9',
    content: '求相机型号',
    time: '7分钟前',
    ip: 'IP属地：南京'
  },
  {
    id: 7,
    avatar: '/images/posts/50 (8).jpg',
    username: '用户10',
    content: '后期用什么软件？',
    time: '6分钟前',
    ip: 'IP属地：西安'
  },
  {
    id: 8,
    avatar: '/images/posts/50 (9).jpg',
    username: '用户11',
    content: '这个角度很特别',
    time: '4分钟前',
    ip: 'IP属地：重庆'
  },
  {
    id: 9,
    avatar: '/images/posts/50.jpg',
    username: '用户12',
    content: '能分享拍摄地点吗？',
    time: '2分钟前',
    ip: 'IP属地：天津'
  },
  {
    id: 10,
    avatar: '/images/posts/1.jpg',
    username: '用户13',
    content: '期待更多作品',
    time: '刚刚',
    ip: 'IP属地：苏州'
  }
])

onMounted(() => {
  const postId = route.params.id
  const post = posts.find(p => p.id === postId)
  
  if (post) {
    userAvatar.value = post.avatarImage
    username.value = post.username || '用户名'
    postImages.value = post.postImages || []
    postTitle.value = post.title || ''
    postText.value = post.text || ''
    tags.value = post.tags || []
    postTime.value = post.time || new Date().toLocaleString()
    postIp.value = post.ip || 'IP属地：未知'
  } else {
    // 如果没有找到帖子，返回首页
    router.push('/')
  }
})
const followUser = () => {
  isFollowing.value = true
}

const unfollowUser = () => {
  isFollowing.value = false
}

const handleReply = (index) => {
  console.log('回复评论:', index)
}

const submitComment = (content) => {
  comments.value.unshift({
    avatar: userAvatar.value,
    username: username.value,
    content,
    time: '刚刚',
    ip: postIp.value
  })
}
</script>

<style scoped>
.post-detail {
  width: 100%;
  height: 100%;
  background: white;
  display: flex;
  flex-direction: column;
}


.post-content {
  padding: 15px;
  flex: 1;
  overflow-y: auto;
  scrollbar-gutter: stable;
  margin-bottom: 5px;
}


</style>