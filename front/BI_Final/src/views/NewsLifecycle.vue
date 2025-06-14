<template>
 <div>
    <!-- 查询区 -->
    <div class="query-bar">
      <v-card class="query-card" color="primary" dark>
        <v-row align="center" no-gutters>
          <v-col cols="12" md="3">
            <v-text-field v-model="newsId" label="新闻ID" dense outlined color="white" />
          </v-col>
          <v-col cols="12" md="4">
            <v-menu v-model="menu" :close-on-content-click="false" transition="scale-transition" offset-y>
              <template #activator="{ on, attrs }">
                <v-text-field
                  v-model="dateRangeText"
                  label="时间范围"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                  dense
                  outlined
                  color="white"
                />
              </template>
              <v-date-picker v-model="dateRange" range @change="menu = false" />
            </v-menu>
          </v-col>
          <v-col cols="12" md="2">
            <v-btn class="query-btn" color="white" text @click="query" :loading="loading">
              查询
            </v-btn>
          </v-col>
        </v-row>
      </v-card>
    </div>
    <!-- 输出区 -->
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
import { ref, computed } from 'vue'
const newsId = ref('')
const dateRange = ref([])
const menu = ref(false)
const loading = ref(false)
const chartOption = ref({})
const tableData = ref([])
const tableHeaders = [
  { text: '时间', value: 'period' },
  { text: '曝光', value: 'impressions' },
  { text: '点击', value: 'clicks' },
  { text: '点击率', value: 'ctr' }
]
const dateRangeText = computed(() =>
  dateRange.value.length === 2 ? `${dateRange.value[0]} ~ ${dateRange.value[1]}` : ''
)

async function query() {
  loading.value = true
  setTimeout(() => {
    tableData.value = [
      { period: '2023-06-01', impressions: 100, clicks: 20, ctr: 0.2 },
      { period: '2023-06-02', impressions: 120, clicks: 30, ctr: 0.25 }
    ]
    chartOption.value = {
      title: { text: '新闻生命周期趋势' },
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: tableData.value.map(i => i.period) },
      yAxis: { type: 'value' },
      series: [
        { name: '曝光', type: 'bar', data: tableData.value.map(i => i.impressions) },
        { name: '点击', type: 'bar', data: tableData.value.map(i => i.clicks) },
        { name: '点击率', type: 'line', data: tableData.value.map(i => i.ctr * 100) }
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