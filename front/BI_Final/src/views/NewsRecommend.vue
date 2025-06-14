<template>
  <div class="page">
    <div class="input-area">
      <div class="input-row">
        <label class="input-label">用户ID</label>
        <v-select
          v-model="userId"
          :items="userIdOptions"
          class="input-box"
          dense
          outlined
          placeholder="请选择用户ID"
          :loading="loadingUserId"
          style="max-width: 260px"
        />
      </div>
      <div class="input-row">
        <label class="input-label">主题/类别</label>
        <v-select
          v-model="category"
          :items="categoryOptions"
          class="input-box"
          dense
          outlined
          placeholder="请选择主题/类别"
          :loading="loadingCategory"
          style="max-width: 260px"
        />
      </div>
      <div class="input-row">
        <v-btn class="query-btn" color="primary" @click="query" :loading="loading">推荐</v-btn>
      </div>
    </div>
    <div class="result-area">
      <div class="result-label">结果</div>
      <v-card class="result-card">
        <v-data-table :headers="tableHeaders" :items="tableData" dense />
      </v-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const userId = ref('')
const userIdOptions = ref([])
const loadingUserId = ref(false)
const category = ref('')
const categoryOptions = ref([])
const loadingCategory = ref(false)
const loading = ref(false)
const tableData = ref([])
const tableHeaders = [
  { text: '新闻ID', value: 'news_id' },
  { text: '标题', value: 'title' },
  { text: '类别', value: 'category' },
  { text: '发布时间', value: 'create_time' }
]

onMounted(() => {
  fetchUserIdOptions()
  fetchCategoryOptions()
})
async function fetchUserIdOptions() {
  loadingUserId.value = true
  // const res = await axios.get('/api/user-id-list')
  // userIdOptions.value = res.data
  userIdOptions.value = ['U123', 'U234', 'U345']
  loadingUserId.value = false
}
async function fetchCategoryOptions() {
  loadingCategory.value = true
  // const res = await axios.get('/api/category-list')
  // categoryOptions.value = res.data
  categoryOptions.value = [
    'sports','news','autos','foodanddrink','finance','music','lifestyle','weather','health','video','movies','tv','travel','entertainment','kids','europe','northamerica','adexperience'
  ]
  loadingCategory.value = false
}
async function query() {
  loading.value = true
  setTimeout(() => {
    tableData.value = [
      { news_id: 'N1', title: 'Title1', category: 'sports', create_time: '2023-06-01' },
      { news_id: 'N2', title: 'Title2', category: 'news', create_time: '2023-06-02' }
    ]
    loading.value = false
  }, 500)
}
</script>

<style scoped>
.page {
  max-width: 900px;
  margin: 0 auto;
  padding: 32px 0 0 0;
}
.input-area {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 22px;
  margin-bottom: 32px;
  background: #f5faff;
  border-radius: 12px;
  padding: 32px 32px 24px 32px;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.06);
}
.input-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 18px;
  margin-bottom: 0;
}
.input-label {
  font-size: 1.15rem;
  font-weight: 500;
  color: #1976d2;
  min-width: 90px;
}
.input-box {
  min-width: 220px;
}
.query-btn {
  min-width: 120px; /* 最小宽度 */
  height: 48px; /* 设置按钮高度 */
  font-size: 1.1rem; /* 字体大小 */
  font-weight: bold; /* 字体加粗 */
  background-color: rgb(20, 112, 203); /* 蓝色背景 */
  color: rgb(255, 255, 255); /* 白色文字 */
  border-radius: 8px; /* 圆角边框 */
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.08); /* 阴影效果 */
  text-align: center; /* 文字居中 */
  display: flex; /* 使用 Flexbox 布局 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  padding: 0 16px; /* 内边距，可根据需要调整 */
  border: none; /* 移除边框 */
  cursor: pointer; /* 鼠标悬停时显示指针 */
  transition: all 0.3s ease; /* 添加过渡效果 */
}

.query-btn:hover {
  background-color: rgb(10, 70, 130); /* 鼠标悬停时的背景颜色 */
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.16); /* 鼠标悬停时的阴影效果 */
}
.result-area {
  margin-top: 18px;
}
.result-label {
  font-size: 1.1rem;
  font-weight: 500;
  color: #1976d2;
  margin-bottom: 10px;
}
.result-card {
  padding: 18px 18px 8px 18px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.08);
}
</style>