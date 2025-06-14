<template>
  <div class="recommendation-page">
    <!-- 输入区 -->
    <div class="input-area">
      <div class="input-row">
        <label class="input-label">用户ID</label>
        <input type="text" v-model="userId" class="input-box" placeholder="请输入用户ID" />
      </div>
      <div class="input-row">
        <button class="query-btn" @click="fetchRecommendations" :disabled="loading">获取推荐</button>
      </div>
    </div>

    <!-- 结果区 -->
    <div class="result-area">
      <div class="result-label">推荐新闻</div>
      <div class="result-card">
        <ul v-if="recommendations.length">
          <li v-for="news in recommendations" :key="news.news_id">
            <strong>{{ news.title }}</strong><br />
            <small>{{ news.news_id }}</small>
          </li>
        </ul>
        <p v-else>没有推荐新闻</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const userId = ref('')
const loading = ref(false)
const recommendations = ref([])

const fetchRecommendations = async () => {
  if (!userId.value) {
    alert('请输入用户ID')
    return
  }
  loading.value = true
  try {
    const data = await getRecommendationData(userId.value)
    recommendations.value = data
  } catch (error) {
    console.error('获取推荐新闻失败', error)
    alert('获取推荐新闻失败，请重试')
  } finally {
    loading.value = false
  }
}

async function getRecommendationData(userId) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { news_id: 'N1', title: '新闻标题1' },
        { news_id: 'N2', title: '新闻标题2' },
        { news_id: 'N3', title: '新闻标题3' }
      ])
    }, 500)
  })
}
</script>

<style scoped>
.recommendation-page {
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
ul {
  list-style-type: none;
  padding: 0;
}
li {
  margin-bottom: 10px;
}
</style>