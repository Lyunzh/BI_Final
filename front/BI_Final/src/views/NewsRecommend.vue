<template>
  <div>
    <div class="query-bar">
      <v-card class="query-card" color="primary" dark>
        <v-row align="center" no-gutters>
          <v-col cols="12" md="3">
            <v-text-field v-model="userId" label="用户ID" dense outlined color="white" />
          </v-col>
          <v-col cols="12" md="3">
            <v-select v-model="category" :items="categoryOptions" label="主题/类别" dense outlined color="white" />
          </v-col>
          <v-col cols="12" md="2">
            <v-btn class="query-btn" color="white" text @click="query" :loading="loading">
              推荐
            </v-btn>
          </v-col>
        </v-row>
      </v-card>
    </div>
    <v-card class="mt-4 content-card">
      <v-card-title>查询结果</v-card-title>
      <v-data-table :headers="tableHeaders" :items="tableData" dense />
    </v-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const userId = ref('')
const category = ref('')
const categoryOptions = ['sports','news','autos','foodanddrink','finance','music','lifestyle','weather','health','video','movies','tv','travel','entertainment','kids','europe','northamerica','adexperience']
const loading = ref(false)
const tableData = ref([])
const tableHeaders = [
  { text: '新闻ID', value: 'news_id' },
  { text: '标题', value: 'title' },
  { text: '类别', value: 'category' },
  { text: '发布时间', value: 'create_time' }
]

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