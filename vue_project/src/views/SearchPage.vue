<template>
  <div class="search-page">
    <!-- 顶部搜索栏 -->
    <div class="search-bar">
      <img src="/images/icons/jiantou.svg" alt="返回" class="back-arrow" @click="goBack" />
      <div class="search-input-container">
        <input type="text" v-model="searchQuery" placeholder="输入搜索内容" class="search-input" />
        <span v-if="searchQuery" class="clear-icon" @click="clearSearch">×</span>
      </div>
      <button class="search-btn" @click="search">搜索</button>
    </div>

    <!-- 历史记录 -->
    <div class="history-record">
      <h3>历史记录</h3>
      <div class="tags-container">
        <button
          v-for="(record, index) in expandHistory ? historyRecords : historyRecords.slice(0, 5)"
          :key="index"
          class="tag"
          @click="addToSearch(record)"
        >
          {{ record }}
        </button>
        <button
          v-if="historyRecords.length > 5"
          @click="expandHistory = !expandHistory"
          class="expand-btn"
        >
          {{ expandHistory ? '收起∧' : '展开∨' }}
        </button>
      </div>
    </div>

    <!-- 关键词搜索 -->
    <div class="keyword-search">
      <h3>关键词搜索</h3>
      <div class="tags-container">
        <button
          v-for="(tag, index) in expandKeywords ? keywordTags : keywordTags.slice(0, 5)"
          :key="index"
          class="tag"
          @click="addToSearch(tag)"
        >
          {{ tag }}
        </button>
        <button
          v-if="keywordTags.length > 5"
          @click="expandKeywords = !expandKeywords"
          class="expand-btn"
        >
          {{ expandKeywords ? '收起∧' : '展开∨' }}
        </button>
      </div>
    </div>

    <!-- 分类菜单与内容区 -->
    <div class="category-content-container">
      <!-- 左侧分类菜单 -->
      <ul class="category-menu">
        <li
          v-for="(category, index) in categories"
          :key="index"
          :class="{ active: currentCategory === category.name }"
          @click="scrollToCategory(category.name)"
        >
          {{ category.name }}
        </li>
      </ul>

      <!-- 右侧内容展示区 -->
      <div class="content-area">
        <div v-for="category in categories" :key="category.name" :id="'category-' + category.name">
          <h4>{{ category.name }}</h4>
          <div v-if="category.subCategories">
            <div v-for="subCat in category.subCategories" :key="subCat.name">
              <h5>{{ subCat.name }}</h5>
              <button
                v-for="(tag, index) in subCat.tags"
                :key="index"
                @click="toggleTag(tag)"
                :class="{ active: selectedTags.includes(tag) }"
              >
                {{ tag }}
              </button>
            </div>
          </div>
          <div v-else>
            <button
              v-for="(tag, index) in category.tags"
              :key="index"
              @click="toggleTag(tag)"
              :class="{ active: selectedTags.includes(tag) }"
            >
              {{ tag }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="bottom-panel">
      <button class="reset-btn" @click="clearSearch">重置</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

// 初始化路由和响应式数据
const router = useRouter()
//const recomresponse = ref([])  // 用来存储推荐的图片

const goBack = () => {
  router.go(-1)
}

// 搜索框内容
const searchQuery = ref('')
// 历史记录展开状态
const expandHistory = ref(false)
// 关键词搜索展开状态
const expandKeywords = ref(false)
// 历史记录数据
const historyRecords = ref(generateHistoryRecords())
// 关键词标签数据
const keywordTags = ref(['常用标签1', '常用标签2', '常用标签3'])
// 当前选中分类
const currentCategory = ref('人数')
// 已选标签
const selectedTags = ref([])

// 分类数据结构
const categories = ref([
  {
    name: '人数',
    tags: ['单人', '双人', '小团体(3-5人)', '大团体(6-10人)', '大群体(10人以上)'],
  },
  {
    name: '关系',
    tags: ['朋友', '情侣', '闺蜜', '亲子', '商务伙伴', '宠物'],
  },
  {
    name: '风格',
    tags: ['国风', '日系', '欧美', '复古', '胶片', '赛博', '搞笑', 'INS', '电影'],
  },
  {
    name: '色系',
    subCategories: [
      {
        name: '暖色',
        tags: ['红', '橙', '黄'],
      },
      {
        name: '冷色',
        tags: ['蓝', '绿', '紫'],
      },
      {
        name: '中性',
        tags: ['黑', '白', '灰'],
      },
      {
        name: '饱和',
        tags: ['高', '低'],
      },
      {
        name: '明度',
        tags: ['明亮', '暗调'],
      },
    ],
  },
  {
    name: '季节',
    tags: ['春季', '夏季', '秋季', '冬季'],
  },
  {
    name: '节日',
    tags: ['春节', '万圣', '圣诞', '情人', '端午', '中秋'],
  },
  {
    name: '活动',
    tags: ['婚礼', '毕业', '生日', '旅行'],
  },
  {
    name: '服饰',
    subCategories: [
      {
        name: '汉服',
        tags: ['旗袍', '战国', '圆领', '清汉'],
      },
      {
        name: '其他',
        tags: ['波西', 'JK', '和风', '美式', '西装', '休闲', 'cos', '森系'],
      },
    ],
  },
  {
    name: '场景',
    subCategories: [
      {
        name: '室内',
        tags: ['家庭', '影棚', '咖啡', '图书馆', '精品', '教室'],
      },
      {
        name: '城市',
        tags: [
          'CBD',
          '历史',
          '天台',
          '地铁',
          '桥梁',
          '街道',
          '园林',
          '公园',
          '湖泊',
          '路牌',
          '动物',
          '迪士',
          '漫展',
        ],
      },
      {
        name: '自然',
        tags: ['樱花', '麦田', '花园', '乡村', '田野', '森林', '草原', '海边', '雪山'],
      },
    ],
  },
  {
    name: '时间',
    tags: ['清晨', '正午', '黄昏', '夜晚', '黄金'],
  },
  {
    name: '天气',
    tags: ['晴', '雾天', '阴天', '小雨', '大雨', '飘雪', '大雪', '极光'],
  },
  {
    name: '道具',
    tags: ['花束', '乐器', '书籍', '泡泡', '粉笔', '气球', '玩偶', '笔'],
  },
  {
    name: '尺寸',
    tags: ['1:1', '3:4', '4:3', '2:3', '3:2', '9:16', '16:9'],
  },
])

// 生成随机历史记录
function generateHistoryRecords() {
  const records = []
  const possibleRecords = [
    '风景', '人像', '美食', '旅行', '宠物', '建筑', '街拍', '夜景',
    '日出', '日落', '婚礼', '毕业', '生日', '节日', '春天', '夏天',
    '秋天', '冬天', '雪景', '海滩', '山脉'
  ]

  for (let i = 0; i < 8; i++) {
    const randomIndex = Math.floor(Math.random() * possibleRecords.length)
    records.push(possibleRecords[randomIndex])
  }

  return records
}

// 切换标签选择状态
function toggleTag(tag) {
  const index = selectedTags.value.indexOf(tag)
  if (index === -1) {
    selectedTags.value.push(tag)
  } else {
    selectedTags.value.splice(index, 1)
  }
  searchQuery.value = selectedTags.value.join(' ')
}

// 重置标签方法
function resetTags() {
  selectedTags.value = []
}

// 开始检索方法
function addToSearch(text) {
  if (!selectedTags.value.includes(text)) {
    selectedTags.value.push(text)
  }
  searchQuery.value = selectedTags.value.join(' ')
}

// 执行搜索并获取推荐图像
const recomresponse = ref([])//定义后面要用的响应式变量
async function search() {
  if (searchQuery.value.trim()) {
    const params = {
      q: searchQuery.value.trim(),
      selectedTags: selectedTags.value.join(',')
    }
    try {
      //将params传输给http://localhost:5001/recommend并将返回结果给response
      const response = await axios.post(
        //这里的5001与python的app.run(port=5001,debug=True)的port一致
        //这里的/recomend和axios.post对应python的@app.route('/recommend', methods=['POST'])
        'http://localhost:5001/recommend', 
        params//params为传输的变量
      );
      //console.log('Full response:', response);
      //console.log('Recommended images:', response.data.recommended_images);

      // 将推荐的图片存入响应式变量，需要先const recomresponse = ref([])
      recomresponse.value = response.data.recommended_images;//将python传回来的变量传入recomresponse
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      alert('Failed to fetch recommendations. Please try again.');
    }

    // 跳转并传递推荐的图片
    router.push({
      name: 'SearchHome',
      //将recomresponse传给SearchHome
      query: { recomresponse: JSON.stringify(recomresponse.value) },
    })
  } else {
    router.push({ name: 'SearchHome'})
  }
}

// 清空搜索框和选中标签
function clearSearch() {
  searchQuery.value = ''
  selectedTags.value = []
}

// 滚动到对应分类
function scrollToCategory(categoryName) {
  currentCategory.value = categoryName
  const element = document.getElementById('category-' + categoryName)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<style scoped>
.search-page {
  padding: 8px;
  font-family: Arial, sans-serif;
  max-width: 600px;
  margin: 0 auto;
}

.search-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 100;
  padding: 4px;
  height: 60px;
  box-sizing: border-box;
}

.back-arrow {
  width: 24px;
  height: 24px;
  cursor: pointer;
}

.search-btn {
  height: 36px;
  padding: 0 8px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
  min-width: 60px;
  box-sizing: border-box;
}

.search-btn:hover {
  background-color: #40a9ff;
}

.back-arrow,
.camera-icon {
  margin-right: 4px;
}

.search-input-container {
  position: relative;
  margin: 0;
  width: 100%;
  max-width: 800px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  padding: 0 12px;
  height: 40px;
  box-sizing: border-box;
}

.search-bar input {
  width: 100%;
  height: 36px;
  padding: 12px;
  border: none;
  background: transparent;
  outline: none;
  box-sizing: border-box;
  font-size: 14px;
  color: #333;
}

@media (min-width: 768px) {
  .search-input-container {
    border-radius: 30px;
  }
}

.clear-icon {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  font-size: 18px;
  color: #999;
  background: white;
  padding: 2px 5px;
  border-radius: 50%;
}

.history-record,
.keyword-search {
  margin-bottom: 20px;
}

.history-record h3,
.keyword-search h3 {
  margin-bottom: 10px;
  font-size: 14px;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.tag {
  padding: 4px 12px;
  border: 1px solid #ccc;
  border-radius: 15px;
  background-color: #f5f5f5;
  font-size: 11px;
  white-space: nowrap;
}

.expand-btn {
  padding: 4px 8px;
  border: none;
  background: none;
  color: #1890ff;
  cursor: pointer;
  font-size: 14px;
}

.category-content-container {
  display: flex;
}

.category-menu {
  width: 20%;
  list-style: none;
  padding: 0;
  margin-right: 20px;
  margin-top: 0;
}

.category-menu li {
  padding: 8px;
  font-size: 14px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
  text-align: center;
}

.category-menu li.active {
  background-color: #f0f0f0;
  font-weight: bold;
}

.content-area {
  width: 70%;
  height: calc(100vh - 410px); /* 350px + 60px底部栏高度 */
  overflow-y: auto;
  padding: 0 10px 0 0;
  margin-top: 0;
}

.tag-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

.bottom-panel {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: white;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding-right: 20px;
  z-index: 100;
}

.content-area h4 {
  margin-bottom: 10px;
  font-size: 14px;
}

.content-area h5 {
  margin: 10px 0 5px 0;
  font-size: 12px;
  color: #666;
}

.content-area button {
  margin: 0 5px 5px 0;
  padding: 4px 12px;
  border: 1px solid #ccc;
  border-radius: 15px;
  background-color: #fff;
  cursor: pointer;
  font-size: 11px;
}

.content-area button.active {
  background-color: #e6f7ff;
  border-color: #1890ff;
  color: #1890ff;
}

.reset-btn {
  padding: 8px 20px;
  background: #f5f5f5;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
