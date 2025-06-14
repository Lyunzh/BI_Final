<template>
 <div>
    <div class="query-bar">
      <v-card class="query-card" color="primary" dark>
        <v-row align="center" no-gutters>
          <v-col cols="12" md="2">
            <v-text-field v-model="userId" label="用户ID" dense outlined color="white" />
          </v-col>
          <v-col cols="12" md="2">
            <v-text-field v-model="newsId" label="新闻ID" dense outlined color="white" />
          </v-col>
          <v-col cols="12" md="2">
            <v-select v-model="categories" :items="categoryOptions" label="类别" multiple chips dense outlined color="white" />
          </v-col>
          <v-col cols="12" md="2">
            <v-text-field v-model="titleLength" label="标题长度" dense outlined color="white" />
          </v-col>
          <v-col cols="12" md="2">
            <v-text-field v-model="contentLength" label="正文长度" dense outlined color="white" />
          </v-col>
          <v-col cols="12" md="2">
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
const userId = ref('')
const newsId = ref('')
const categories = ref([])
const categoryOptions = ['sports','news','autos','foodanddrink','finance','music','lifestyle','weather','health','video','movies','tv','travel','entertainment','kids','europe','northamerica','adexperience']
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