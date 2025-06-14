<template>
  <div class="advanced-query-page">
    <!-- 输入区 -->
    <div class="input-area">
      <div class="input-row">
        <label class="input-label">开始日期</label>
        <input type="date" v-model="startDate" class="input-box" />
      </div>
      <div class="input-row">
        <label class="input-label">结束日期</label>
        <input type="date" v-model="endDate" class="input-box" />
      </div>
      <div class="input-row">
        <label class="input-label">新闻分类</label>
        <input type="text" v-model="category" class="input-box" placeholder="请输入新闻分类" />
      </div>
      <div class="input-row">
        <label class="input-label">新闻主题</label>
        <input type="text" v-model="topic" class="input-box" placeholder="请输入新闻主题" />
      </div>
      <div class="input-row">
        <label class="input-label">新闻标题长度</label>
        <input type="number" v-model="minTitleLength" class="input-box" placeholder="最小长度" style="width: 150px;" />
        至
        <input type="number" v-model="maxTitleLength" class="input-box" placeholder="最大长度" style="width: 150px;" />
      </div>
      <div class="input-row">
        <label class="input-label">新闻内容长度</label>
        <input type="number" v-model="minContentLength" class="input-box" placeholder="最小长度" style="width: 150px;" />
        至
        <input type="number" v-model="maxContentLength" class="input-box" placeholder="最大长度" style="width: 150px;" />
      </div>
      <div class="input-row">
        <label class="input-label">用户ID</label>
        <input type="text" v-model="userId" class="input-box" placeholder="请输入用户ID" />
      </div>
      <div class="input-row">
        <button class="query-btn" @click="fetchData" :disabled="loading">查询</button>
      </div>
    </div>

    <!-- 结果区 -->
    <div class="result-area">
      <div class="result-label">查询结果</div>
      <div class="result-card">
        <table v-if="queryResults.length">
          <thead>
            <tr>
              <th>ID</th>
              <th>用户ID</th>
              <th>新闻ID</th>
              <th>事件类型</th>
              <th>事件时间</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="result in queryResults" :key="result.id">
              <td>{{ result.id }}</td>
              <td>{{ result.user_id }}</td>
              <td>{{ result.news_id }}</td>
              <td>{{ result.event_type }}</td>
              <td>{{ result.event_time }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else>没有查询结果</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const startDate = ref('')
const endDate = ref('')
const category = ref('')
const topic = ref('')
const minTitleLength = ref(null)
const maxTitleLength = ref(null)
const minContentLength = ref(null)
const maxContentLength = ref(null)
const userId = ref('')
const loading = ref(false)
const queryResults = ref([])

const fetchData = async () => {
  if (!startDate.value || !endDate.value) {
    alert('请选择开始和结束日期')
    return
  }
  loading.value = true
  try {
    const data = await getAdvancedQueryData({
      startDate,
      endDate,
      category,
      topic,
      minTitleLength,
      maxTitleLength,
      minContentLength,
      maxContentLength,
      userId
    })
    queryResults.value = data
  } catch (error) {
    console.error('查询失败', error)
    alert('查询失败，请重试')
  } finally {
    loading.value = false
  }
}

async function getAdvancedQueryData(params) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { id: 1, user_id: 'U1', news_id: 'N1', event_type: 'CLICK', event_time: '2023-06-01 12:00:00' },
        // 模拟更多查询结果...
      ])
    }, 500)
  })
}
</script>

<style scoped>
.advanced-query-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 32px 0 0 0;
}
.input-area {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px; /* 减小间距 */
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
  gap: 8px; /* 减小内部元素间距 */
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
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.query-btn {
  padding: 8px 16px;
  font-size: 1.1rem;
  font-weight: bold;
  background-color: rgb(20, 112, 203);
  color: rgb(255, 255, 255);
  border-radius: 8px;
  cursor: pointer;
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
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
th {
  background-color: #f2f2f2;
}
</style>