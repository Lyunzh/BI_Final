<template>
   <div>
    <div class="query-bar">
      <v-card class="query-card" color="primary" dark>
        <v-row align="center" no-gutters>
          <v-col cols="12" md="4">
            <v-text-field v-model="userId" label="用户ID" dense outlined color="white" />
          </v-col>
          <v-col cols="12" md="2">
            <v-btn class="query-btn" color="white" text @click="query" :loading="loading">
              查询
            </v-btn>
          </v-col>
        </v-row>
      </v-card>
    </div>
    <v-card class="mt-4 content-card">
      <v-card-title>查询结果</v-card-title>
      <v-row>
        <v-col cols="12" md="8">
          <v-chart :option="chartOption" autoresize style="height:400px" />
        </v-col>
        <v-col cols="12" md="4">
          <v-data-table :headers="tableHeaders" :items="tableData" dense />
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const userId = ref('')
const loading = ref(false)
const chartOption = ref({})
const tableData = ref([])
const tableHeaders = [
  { text: '兴趣类别', value: 'category' },
  { text: '兴趣度', value: 'score' }
]

async function query() {
  loading.value = true
  setTimeout(() => {
    tableData.value = [
      { category: 'sports', score: 10 },
      { category: 'news', score: 5 }
    ]
    chartOption.value = {
      title: { text: '用户兴趣分布' },
      tooltip: { trigger: 'item' },
      series: [
        {
          type: 'pie',
          radius: '50%',
          data: tableData.value.map(i => ({ name: i.category, value: i.score }))
        }
      ]
    }
    loading.value = false
  }, 500)
}
</script>

<style scoped>
.query-bar {
  margin-top: 24px;
  margin-bottom: 16px;
}
.query-card {
  padding: 16px 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.08);
}
.query-btn {
  width: 100%;
  font-weight: bold;
  font-size: 16px;
  background: #1976d2 !important;
  color: #fff !important;
  border-radius: 8px;
}
.content-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.08);
}
</style>