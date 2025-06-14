<template>
  <div class="lifecycle-page">
    <!-- 输入区 -->
    <div class="input-area">
      <div class="input-row">
        <label class="input-label">新闻ID</label>
        <select v-model="newsId" class="input-box">
          <option v-for="option in newsIdOptions" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </div>
      <div class="input-row">
        <label class="input-label">时间范围</label>
        <input type="date" v-model="dateRange[0]" class="input-box" />
        <input type="date" v-model="dateRange[1]" class="input-box" />
      </div>
      <div class="input-row">
        <button class="query-btn" @click="fetchData" :disabled="loading">查询</button>
      </div>
    </div>

    <!-- 结果区 -->
    <div class="result-area">
      <div class="result-label">结果</div>
      <div class="result-card">
        <canvas id="chartCanvas" style="height:320px"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'

const newsId = ref('')
const newsIdOptions = ref([])
const loading = ref(false)
let chart = null

const dateRange = ref(['', ''])

onMounted(async () => {
  await fetchNewsIdOptions()
  nextTick(() => {
    createChart()
  })
})

async function fetchNewsIdOptions() {
  newsIdOptions.value = ['N12345', 'N23456', 'N34567']
}

async function fetchData() {
  if (!newsId.value || dateRange.value[0] === '' || dateRange.value[1] === '') {
    alert('请选择新闻ID和时间范围')
    return
  }
  loading.value = true
  try {
    const data = await getLifecycleData(newsId.value, dateRange.value[0], dateRange.value[1])
    updateChartData(data)
  } catch (error) {
    console.error('获取数据失败', error)
    alert('获取数据失败，请重试')
  } finally {
    loading.value = false
  }
}

function createChart() {
  const ctx = document.getElementById('chartCanvas').getContext('2d')
  chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [],
      datasets: [{
        label: '曝光次数',
        data: [],
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  })
}

function updateChartData(data) {
  if (!chart) return
  chart.data.labels = data.periods
  chart.data.datasets[0].data = data.impressions
  chart.update()
}

async function getLifecycleData(newsId, startDate, endDate) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        periods: ['2023-06-01', '2023-06-02'],
        impressions: [100, 120]
      })
    }, 500)
  })
}
</script>

<style scoped>
.lifecycle-page {
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
</style>