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
          style="max-width: 180px"
        />
        <label class="input-label">新闻ID</label>
        <v-select
          v-model="newsId"
          :items="newsIdOptions"
          class="input-box"
          dense
          outlined
          placeholder="请选择新闻ID"
          :loading="loadingNewsId"
          style="max-width: 180px"
        />
      </div>
      <div class="input-row">
        <label class="input-label">类别</label>
        <v-select
          v-model="categories"
          :items="categoryOptions"
          multiple
          chips
          class="input-box"
          dense
          outlined
          placeholder="请选择类别"
          :loading="loadingCategory"
          style="max-width: 220px"
        />
        <label class="input-label">标题长度</label>
        <v-text-field
          v-model="titleLength"
          class="input-box"
          dense
          outlined
          placeholder="标题长度"
          style="max-width: 120px"
        />
        <label class="input-label">正文长度</label>
        <v-text-field
          v-model="contentLength"
          class="input-box"
          dense
          outlined
          placeholder="正文长度"
          style="max-width: 120px"
        />
      </div>
      <div class="input-row">
        <label class="input-label">时间范围</label>
        <v-menu v-model="menu" :close-on-content-click="false" transition="scale-transition" offset-y>
          <template #activator="{ on, attrs }">
            <v-text-field
              v-model="dateRangeText"
              class="input-box"
              label="请选择时间范围"
              readonly
              v-bind="attrs"
              v-on="on"
              dense
              outlined
              style="max-width: 260px"
            />
          </template>
          <v-date-picker v-model="dateRange" range @change="menu = false" />
        </v-menu>
        <v-btn class="query-btn" color="primary" @click="query" :loading="loading">查询</v-btn>
      </div>
    </div>
    <div class="result-area">
      <div class="result-label">结果</div>
      <v-card class="result-card">
        <v-row>
          <v-col cols="12" md="7">
            <v-chart :option="chartOption" autoresize style="height:320px" />
          </v-col>
          <v-col cols="12" md="5">
            <v-data-table :headers="tableHeaders" :items="tableData" dense />
          </v-col>
        </v-row>
      </v-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
const userId = ref('')
const userIdOptions = ref([])
const loadingUserId = ref(false)
const newsId = ref('')
const newsIdOptions = ref([])
const loadingNewsId = ref(false)
const categories = ref([])
const categoryOptions = ref([])
const loadingCategory = ref(false)
const titleLength = ref('')
const contentLength = ref('')
const dateRange = ref([])
const menu = ref(false)
const loading = ref(false)
const chartOption = ref({})
const tableData = ref([])
const tableHeaders = [
  { text: '新闻ID', value: 'news_id' },
  { text: '标题', value: 'title' },
  { text: '类别', value: 'category' },
  { text: '曝光', value: 'impressions' },
  { text: '点击', value: 'clicks' }
]
const dateRangeText = computed(() =>
  dateRange.value.length === 2 ? `${dateRange.value[0]} ~ ${dateRange.value[1]}` : ''
)

onMounted(() => {
  fetchUserIdOptions()
  fetchNewsIdOptions()
  fetchCategoryOptions()
})
async function fetchUserIdOptions() {
  loadingUserId.value = true
  userIdOptions.value = ['U123', 'U234', 'U345']
  loadingUserId.value = false
}
async function fetchNewsIdOptions() {
  loadingNewsId.value = true
  newsIdOptions.value = ['N12345', 'N23456', 'N34567']
  loadingNewsId.value = false
}
async function fetchCategoryOptions() {
  loadingCategory.value = true
  categoryOptions.value = [
    'sports','news','autos','foodanddrink','finance','music','lifestyle','weather','health','video','movies','tv','travel','entertainment','kids','europe','northamerica','adexperience'
  ]
  loadingCategory.value = false
}
async function query() {
  loading.value = true
  setTimeout(() => {
    tableData.value = [
      { news_id: 'N1', title: 'Title1', category: 'sports', impressions: 100, clicks: 20 },
      { news_id: 'N2', title: 'Title2', category: 'news', impressions: 120, clicks: 30 }
    ]
    chartOption.value = {
      title: { text: '高级查询结果' },
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: tableData.value.map(i => i.title) },
      yAxis: { type: 'value' },
      series: [
        { name: '曝光', type: 'bar', data: tableData.value.map(i => i.impressions) },
        { name: '点击', type: 'bar', data: tableData.value.map(i => i.clicks) }
      ]
    }
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