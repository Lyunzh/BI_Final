<template>
  <div class="query-log-page">
    <!-- 查询按钮 -->
    <div class="input-area">
      <div class="input-row">
        <button class="query-btn" @click="fetchLogs" :disabled="loading">获取查询日志</button>
      </div>
    </div>

    <!-- 结果区 -->
    <div class="result-area">
      <div class="result-label">查询日志</div>
      <div class="result-card">
        <table v-if="logs.length">
          <thead>
            <tr>
              <th>ID</th>
              <th>查询语句</th>
              <th>查询时间</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in logs" :key="log.id">
              <td>{{ log.id }}</td>
              <td>{{ log.query_text }}</td>
              <td>{{ log.query_time }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else>没有查询日志</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const loading = ref(false)
const logs = ref([])

const fetchLogs = async () => {
  loading.value = true
  try {
    const data = await getQueryLogs()
    logs.value = data
  } catch (error) {
    console.error('获取查询日志失败', error)
    alert('获取查询日志失败，请重试')
  } finally {
    loading.value = false
  }
}

async function getQueryLogs() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { id: 1, query_text: 'SELECT * FROM news', query_time: '2023-06-01 12:00:00' },
        { id: 2, query_text: 'INSERT INTO query_log', query_time: '2023-06-01 12:05:00' },
        // 模拟更多日志数据...
      ])
    }, 500)
  })
}
</script>

<style scoped>
.query-log-page {
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