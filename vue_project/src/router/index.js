import AIChatView from '../views/AIChatView.vue'
import NotLoggedInView from '../views/NotLoggedInView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CheckinView from '../views/CheckinView.vue'
import MyView from '../views/MyView.vue'
import PostDetailView from '../views/PostDetailView.vue'
import ToBeShotView from '../views/ToBeShotView.vue'
import FriendsAndGroups from '../views/FriendsAndGroups.vue'
import CreatePostView from '../views/CreatePostView.vue'
import CameraView from '../views/CameraView.vue'
import ChatDetailView from '../views/ChatDetailView.vue'
import SpotDetailView from '../views/locationDetailView.vue'
import SearchHomeView from '../views/SearchHomeView.vue'
import Login from '../views/LoginIndex.vue';
import Register from '../views/TryRegister.vue';
import tryerror from '../views/TryError.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/checkin',
      name: 'checkin',
      component: CheckinView,
    },
    {
      path: '/my',
      name: 'profile',
      component: NotLoggedInView,
      meta: { requiresAuth: true }
    },
    {
      path: '/authenticated',
      name: 'authenticated-profile',
      component: MyView,
    },
    {
      path: '/post/:id',
      name: 'post',
      component: PostDetailView,
    },
    {
      path: '/to-be-shot',
      name: 'toBeShot',
      component: ToBeShotView,
    },
    {
      path: '/friends-groups',
      name: 'friends-groups',
      component: FriendsAndGroups,
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/SearchPage.vue'),
    },
    {
      path: '/create-post',
      name: 'create-post',
      component: CreatePostView,
    },
    {
      path: '/camera',
      name: 'camera',
      component: CameraView,
    },
    {
      path: '/chat/:id',
      name: 'chat-detail',
      component: ChatDetailView,
    },
    {
      path: '/ai-chat/:id',
      name: 'ai-chat',
      component: AIChatView,
    },
    {
      path: '/spot/:id',
      name: 'spot-detail',
      component: SpotDetailView,
    },
    {
      path: '/search-home',
      name: 'SearchHome',
      component: SearchHomeView,
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/tryerror',
      name: 'tryerror',
      component: tryerror
    },
  ],
});

router.beforeEach((to, from, next) => {
  // 检查是否需要登录
  if (to.meta.requiresAuth) {
    const isAuthenticated = localStorage.getItem('isAuthenticated'); // 从localStorage读取登录状态
    if (isAuthenticated) {
      next(); // 如果已登录，允许访问
    } else {
      next('/login'); // 如果未登录，跳转到登录页面
    }
  } else {
    next(); // 无需登录的页面，直接访问
  }
});

export default router
